import yfinance as yf
import pandas as pd

def fetch_price_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1mo")

        if hist.empty:
            print(f"{ticker}: No data found, symbol may be delisted")
            return None  # Return None to handle this case

        current_price = hist['Close'].iloc[-1]
        price_change = ((hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100
        high_52_week = stock.history(period="1y")['High'].max()
        low_52_week = stock.history(period="1y")['Low'].min()
        volume = hist['Volume'].sum()

        return {
            'Current Price': float(current_price),
            'Price Change (%)': float(price_change),
            '52-Week High': float(high_52_week),
            '52-Week Low': float(low_52_week),
            'Volume': int(volume)
        }
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None  # Handle errors gracefully

if __name__ == "__main__":
    # Renewable Energy or Environmental Protection Tickers, Tech Tickers (AI, Fintech, Cloud Computing, Robotics), Biotechnology and Pharmaceuticals
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
    fetch_price_data(tickers)
