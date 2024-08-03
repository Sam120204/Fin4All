import yfinance as yf
import pandas as pd
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
from fetch_ticker_price import fetch_price_data
import json

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


if __name__ == "__main__":
    ticker = "AAPL"
    financial_data = fetch_and_filter_data(ticker)
    print(json.dumps(financial_data, indent=4))
