import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    
    # General info
    try:
        info = stock.info
        print("General Info:")
        print(info)
    except Exception as e:
        print(f"Could not fetch general info: {e}")

    # Historical market data
    try:
        hist = stock.history(period="1mo")
        print("\nHistorical Data:")
        print(hist)
    except Exception as e:
        print(f"Could not fetch historical data: {e}")

    # History metadata
    try:
        metadata = stock.history_metadata
        print("\nHistory Metadata:")
        print(metadata)
    except Exception as e:
        print(f"Could not fetch history metadata: {e}")

    # Actions (dividends, splits, capital gains)
    try:
        actions = stock.actions
        dividends = stock.dividends
        splits = stock.splits
        capital_gains = stock.capital_gains  # only for mutual funds & ETFs
        print("\nActions (Dividends, Splits, Capital Gains):")
        print(actions)
        print(dividends)
        print(splits)
        print(capital_gains)
    except Exception as e:
        print(f"Could not fetch actions: {e}")

    # Financials
    try:
        # Quarterly income statement
        quarterly_income_stmt = stock.quarterly_income_stmt
        print("\nQuarterly Income Statement:")
        print(quarterly_income_stmt)
        quarterly_income_stmt.to_csv(f'{ticker_symbol}_quarterly_income_statement.csv')

        # Quarterly balance sheet
        quarterly_balance_sheet = stock.quarterly_balance_sheet
        print("\nQuarterly Balance Sheet:")
        print(quarterly_balance_sheet)
        quarterly_balance_sheet.to_csv(f'{ticker_symbol}_quarterly_balance_sheet.csv')

        # Quarterly cash flow statement
        quarterly_cashflow = stock.quarterly_cashflow
        print("\nQuarterly Cash Flow Statement:")
        print(quarterly_cashflow)
        quarterly_cashflow.to_csv(f'{ticker_symbol}_quarterly_cashflow.csv')

    except Exception as e:
        print(f"Could not fetch financials: {e}")

    # Holders
    try:
        major_holders = stock.major_holders
        institutional_holders = stock.institutional_holders
        mutualfund_holders = stock.mutualfund_holders
        insider_transactions = stock.insider_transactions
        print("\nMajor Holders:")
        print(major_holders)
        print("\nInstitutional Holders:")
        print(institutional_holders)
        print("\nMutualfund Holders:")
        print(mutualfund_holders)
        print("\nInsider Transactions:")
        print(insider_transactions)
    except Exception as e:
        print(f"Could not fetch holders: {e}")

    # Recommendations
    try:
        recommendations = stock.recommendations
        recommendations_summary = stock.recommendations_summary
        upgrades_downgrades = stock.upgrades_downgrades
        print("\nRecommendations:")
        print(recommendations)
        print("\nRecommendations Summary:")
        print(recommendations_summary)
        print("\nUpgrades/Downgrades:")
        print(upgrades_downgrades)
    except Exception as e:
        print(f"Could not fetch recommendations: {e}")

    # Earnings dates
    try:
        earnings_dates = stock.earnings_dates
        print("\nEarnings Dates:")
        print(earnings_dates)
    except Exception as e:
        print(f"Could not fetch earnings dates: {e}")

    # ISIN
    try:
        isin = stock.isin
        print("\nISIN:")
        print(isin)
    except Exception as e:
        print(f"Could not fetch ISIN: {e}")

    # Options expirations
    try:
        options = stock.options
        print("\nOptions Expirations:")
        print(options)
    except Exception as e:
        print(f"Could not fetch options expirations: {e}")

    # News
    try:
        news = stock.news
        print("\nNews:")
        print(news)
    except Exception as e:
        print(f"Could not fetch news: {e}")

if __name__ == '__main__':
    ticker_symbol = "AAPL"  # Example ticker symbol for Apple Inc.
    fetch_stock_data(ticker_symbol)
