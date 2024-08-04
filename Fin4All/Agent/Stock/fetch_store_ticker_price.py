import yfinance as yf
import pandas as pd
import datetime

def fetch_three_months_data(ticker):
    """
    Fetches the historical stock data for the past three months using yfinance
    and returns only the date and close price.

    Args:
    ticker (str): The stock ticker symbol.

    Returns:
    pd.DataFrame: A DataFrame containing the date and close price for the past three months.
    """
    try:
        # Create a Ticker object
        stock = yf.Ticker(ticker)

        # Fetch historical data for the past 3 months
        hist_data = stock.history(period="3mo")

        # Check if the DataFrame is empty
        if hist_data.empty:
            print(f"{ticker}: No data found, symbol may be delisted")
            return None

        # Filter only the date and closing price
        hist_data = hist_data[['Close']]

        # Reset index to have dates as a separate column
        hist_data = hist_data.reset_index()

        # Convert datetime to date
        hist_data['Date'] = hist_data['Date'].dt.date

        return hist_data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

def date_to_str(date_obj):
    """
    Convert a datetime.date or datetime.datetime object to a string in YYYY-MM-DD format.

    Args:
        date_obj (datetime.date or datetime.datetime): The date object to convert.

    Returns:
        str: The date as a string in YYYY-MM-DD format.
    """
    if isinstance(date_obj, (pd.Timestamp, datetime.datetime, datetime.date)):
        return date_obj.strftime('%Y-%m-%d')
    return str(date_obj)

if __name__ == "__main__":
    # Example usage
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
        data = fetch_three_months_data(ticker)
        if data is not None:
            print(data)
        else: break
