import yfinance as yf
import pandas as pd
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
from fetch_ticker_price import fetch_price_data
import os

# Load environment variables from the .env file
load_dotenv()

MONGO_DB_USER = os.getenv('MONGO_DB_USER')
MONGO_DB_PWD = os.getenv('MONGO_DB_PWD')

# Connect to MongoDB
def get_database():
    try:
        connect_string = f"mongodb+srv://{MONGO_DB_USER}:{MONGO_DB_PWD}@fin4all.r3ihnkl.mongodb.net/?retryWrites=true&w=majority&appName=Fin4All"
        client = MongoClient(connect_string)
        return client['Fin4All']
    except ConnectionFailure as e:
        print(f"Could not connect to MongoDB: {e}")
        return None

def create_collection_if_not_exists(db, collection_name):
    try:
        collection_names = db.list_collection_names()
        if collection_name not in collection_names:
            db.create_collection(collection_name)
            print(f"Created the '{collection_name}' collection.")
    except Exception as e:
        print(f"Error creating collection: {e}")


def clear_collection(db, collection_name):
    try:
        # Check if the collection exists
        if collection_name in db.list_collection_names():
            # Clear the collection by deleting all documents
            result = db[collection_name].delete_many({})
            print(f"Cleared {result.deleted_count} documents from the '{collection_name}' collection.")
        else:
            print(f"The collection '{collection_name}' does not exist in the database.")
    except Exception as e:
        print(f"Error clearing the collection: {e}")
        

def fetch_and_filter_data(ticker_symbol):
    # Initialize the Ticker object
    ticker = yf.Ticker(ticker_symbol)

    # Define the fields to keep
    income_stmt_fields = [
        'Net Income From Continuing Operation Net Minority Interest',
        'Normalized EBITDA',
        'Reconciled Depreciation'
    ]

    balance_sheet_fields = [
        'Total Debt',
        'Net Debt',
        'Ordinary Shares Number',
        'Share Issued'
    ]

    cashflow_fields = [
        'Free Cash Flow',
        'Repurchase Of Capital Stock',
        'Repayment Of Debt',
        'Issuance Of Debt'
    ]

    # Fetch the data
    income_stmt = ticker.quarterly_financials
    balance_sheet = ticker.quarterly_balance_sheet
    cashflow = ticker.quarterly_cashflow

    # Filter the data to keep only the required fields and the latest two quarters
    income_stmt = income_stmt.loc[[field for field in income_stmt_fields if field in income_stmt.index]].iloc[:, :2]
    balance_sheet = balance_sheet.loc[[field for field in balance_sheet_fields if field in balance_sheet.index]].iloc[:, :2]
    cashflow = cashflow.loc[[field for field in cashflow_fields if field in cashflow.index]].iloc[:, :2]

    # Fill missing fields with the mean value of that field
    for df in [income_stmt, balance_sheet, cashflow]:
        df.fillna(df.mean(), inplace=True)

    # Convert DataFrames to dictionaries
    income_stmt_dict = income_stmt.transpose().to_dict(orient='index')
    balance_sheet_dict = balance_sheet.transpose().to_dict(orient='index')
    cashflow_dict = cashflow.transpose().to_dict(orient='index')

    # Convert Timestamp keys to string (date only)
    income_stmt_dict = {str(k).split(" ")[0]: v for k, v in income_stmt_dict.items()}
    balance_sheet_dict = {str(k).split(" ")[0]: v for k, v in balance_sheet_dict.items()}
    cashflow_dict = {str(k).split(" ")[0]: v for k, v in cashflow_dict.items()}

    # Fetch price data
    price_data = fetch_price_data(ticker_symbol)

    # Create the final data structure
    data = {
        "ticker": ticker_symbol,
        "price": price_data,
        "income_statement_quarter": income_stmt_dict,
        "balance_sheet": balance_sheet_dict,
        "cashflow": cashflow_dict
    }

    return data

def update_ticker_statement(db, ticker, data):
    try:
        collection_name = "TickersStatement"
        create_collection_if_not_exists(db, collection_name)
        db[collection_name].update_one(
            {"ticker": ticker},
            {"$set": data},
            upsert=True
        )
        print(f"Data for {ticker} has been updated in the database.")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    db = get_database()
    if db is not None:
        # clear_collection(db, "TickersStatement")
        # Call top 50 tickers from fetch_apewisdom (top_stocks.json)
        # For demonstration, we show them below
        tickers = [
            "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "BRK-B", "JPM", "JNJ", "V",
            "WMT", "PG", "NVDA", "DIS", "PYPL", "MA", "HD", "VZ", "NFLX", "ADBE",
            "INTC", "PFE", "T", "MRK", "KO", "PEP", "CMCSA", "ABT", "CSCO", "XOM",
            "NKE", "ABBV", "CVX", "ORCL", "ACN", "AVGO", "LLY", "COST", "DHR", "QCOM",
            "MCD", "NEE", "BMY", "TXN", "HON", "LOW", "UNH", "MDT", "LIN", "PM", 
            "ISRG", "SQ", "AMD", "ENPH", "SEDG", "FSLR", "RUN", "BE", "PLUG", "SPWR",
            "NOVA", "BLDP", "CWEN", "HASI", "BIIB", "AMGN", "GILD", "MRNA", "VRTX",
            "FLNC", "RNW"
        ]
        for ticker in tickers:
            data = fetch_and_filter_data(ticker)
            update_ticker_statement(db, ticker, data)
