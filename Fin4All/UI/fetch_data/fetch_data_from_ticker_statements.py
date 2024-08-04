import os
import pandas as pd
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
import yfinance as yf

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


# Function to fetch stock data from MongoDB
def fetch_stock_data_from_db():
    db = get_database()
    if db is None:
        return {}

    collection_name = "TickersStatement"
    collection_news = "NewsSentiment"
    collection = db[collection_name]
    news_info = db[collection_news]
    stock_data = {}

    # Fetch all documents from the collection
    cursor = collection.find({})

    for document in cursor:
        ticker = document['ticker']
        
        # Fetch news articles and sentiment summary for the current ticker
        news_document = news_info.find_one({"ticker": ticker})

        if news_document:
            articles = news_document.get('articles', [])
            news = [{"title": article['headline'], "url": article['url']} for article in articles]
            sentiment_summary = news_document.get('sentiment_summary', '')
        else:
            news = []
            sentiment_summary = ''

        # Construct the stock data structure
        stock_data[ticker] = {
            'Current Price': document['price']['Current Price'],
            'Price Change (%)': document['price']['Price Change (%)'],
            '52-Week High': document['price']['52-Week High'],
            '52-Week Low': document['price']['52-Week Low'],
            'Volume': document['price']['Volume'],
            'Prices': document.get('Prices', []),
            'Open Price': document['price']['Open Price'],
            'Close Price': document['price']['Close Price'],
            'Balance Sheet': pd.DataFrame(document['balance_sheet']).transpose(),
            'Cash Flow': pd.DataFrame(document['cashflow']).transpose(),
            'Income Statement': pd.DataFrame(document['income_statement_quarter']).transpose(),
            'News': news,
            'Sentiment Summary': sentiment_summary
        }
    
    return stock_data

if __name__ == "__main__":
    stock_data = fetch_stock_data_from_db()
    # Print out the stock data for verification
    for ticker, data in stock_data.items():
        print(f"{ticker}: {data}")
