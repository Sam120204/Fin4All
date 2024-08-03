import yfinance as yf
import pandas as pd

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

    # Filter the data to keep only the required fields and the latest two years
    income_stmt = income_stmt.loc[[field for field in income_stmt_fields if field in income_stmt.index]].iloc[:, :2]
    balance_sheet = balance_sheet.loc[[field for field in balance_sheet_fields if field in balance_sheet.index]].iloc[:, :2]
    cashflow = cashflow.loc[[field for field in cashflow_fields if field in cashflow.index]].iloc[:, :2]

    # Fill missing fields with the mean value of that field
    for df in [income_stmt, balance_sheet, cashflow]:
        df.fillna(df.mean(), inplace=True)

    # Transpose the data for a better CSV format
    income_stmt = income_stmt.transpose()
    balance_sheet = balance_sheet.transpose()
    cashflow = cashflow.transpose()

    # Save to CSV files
    income_stmt.to_csv(f'{ticker_symbol}_filtered_income_stmt.csv')
    balance_sheet.to_csv(f'{ticker_symbol}_filtered_balance_sheet.csv')
    cashflow.to_csv(f'{ticker_symbol}_filtered_cashflow.csv')

    print(f"Data for {ticker_symbol} has been saved to CSV files.")

if __name__ == "__main__":
    # Test the function with different tickers
    tickers = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "FB", "TSLA", "BRK-B", "JPM", "JNJ", "V",
        "WMT", "PG", "NVDA", "DIS", "PYPL", "MA", "HD", "VZ", "NFLX", "ADBE",
        "INTC", "PFE", "T", "MRK", "KO", "PEP", "CMCSA", "ABT", "CSCO", "XOM",
        "NKE", "ABBV", "CVX", "ORCL", "ACN", "AVGO", "LLY", "COST", "DHR", "QCOM",
        "MCD", "NEE", "BMY", "TXN", "HON", "LOW", "UNH", "MDT", "LIN", "PM"
    ]
    # Renewable Energy or Environmental Protection Tickers, Tech Tickers (AI, Fintech, Cloud Computing, Robotics), Biotechnology and Pharmaceuticals
    new_tickers = [
        "ISRG", "SQ", "AMD", "ENPH", "SEDG", "FSLR", "RUN", "BE", "PLUG", "SPWR",
        "NOVA", "BLDP", "REGI", "CWEN", "HASI", "BIIB", "AMGN", "GILD", "MRNA", "VRTX",
        "FLNC", "RNW"
    ]

    for ticker in new_tickers:
        fetch_and_filter_data(ticker)
