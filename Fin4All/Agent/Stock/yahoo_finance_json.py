import yfinance as yf
import pandas as pd
import json
from fetch_apewisdom import fetch_top_stocks
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

    # Create the final data structure
    data = {
        "ticker": ticker_symbol,
        "income_statement_quarter": income_stmt_dict,
        "balance_sheet": balance_sheet_dict,
        "cashflow": cashflow_dict
    }

    # Save to a JSON file
    with open(f'{ticker_symbol}_financials.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"Data for {ticker_symbol} has been saved to JSON file.")

if __name__ == "__main__":
    # Test the function with different tickers
    # tickers = [
    #     "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "BRK-B", "JPM", "JNJ", "V",
    #     "WMT", "PG", "NVDA", "DIS", "PYPL", "MA", "HD", "VZ", "NFLX", "ADBE",
    #     "INTC", "PFE", "T", "MRK", "KO", "PEP", "CMCSA", "ABT", "CSCO", "XOM",
    #     "NKE", "ABBV", "CVX", "ORCL", "ACN", "AVGO", "LLY", "COST", "DHR", "QCOM",
    #     "MCD", "NEE", "BMY", "TXN", "HON", "LOW", "UNH", "MDT", "LIN", "PM"
    # ]
    tickers = fetch_top_stocks()
    for ticker in tickers:
        fetch_and_filter_data(ticker)
