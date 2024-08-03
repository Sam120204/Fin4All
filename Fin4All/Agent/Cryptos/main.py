import yfinance as yf

def fetch_ticker_data(ticker_symbol):
    # Initialize the Ticker object
    ticker = yf.Ticker(ticker_symbol)
    
    # Fetch and display general information
    try:
        info = ticker.info
        print("Info:")
        print(info)
    except Exception as e:
        print(f"Could not fetch info for {ticker_symbol}: {e}")
    
    # Fetch and display historical market data
    try:
        hist = ticker.history(period="1mo")
        print("\nHistorical Data:")
        print(hist)
    except Exception as e:
        print(f"Could not fetch historical data for {ticker_symbol}: {e}")
    
    # Fetch and display news
    try:
        news = ticker.news
        print("\nNews:")
        for item in news:
            print(f"Title: {item['title']}")
            print(f"Publisher: {item['publisher']}")
            print(f"Link: {item['link']}\n")
    except Exception as e:
        print(f"Could not fetch news for {ticker_symbol}: {e}")

# Test the function with a cryptocurrency ticker
fetch_ticker_data("BTC.X")
