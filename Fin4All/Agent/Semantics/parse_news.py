from bs4 import BeautifulSoup
import requests
import yfinance as yf
import dotenv
import os
import finnhub
from datetime import datetime, timedelta
from gpt_investment_analysis import get_database

dotenv.load_dotenv()


def clean_text(text):
    # Define the special characters to remove
    special_chars = r"\/+=-"
    # Remove special characters
    for char in special_chars:
        text = text.replace(char, "")
    return text


def trim_text(text, max_length=500):
    """ Trims the text to a maximum length without cutting off words. """
    if len(text) > max_length:
        return text[:max_length].rsplit(' ', 1)[0] + '...'
    return text


def get_finnhub_news(ticker):
    finnhub_client = finnhub.Client(api_key=os.environ.get("FINNHUB_API_KEY"))

    # Calculate the date range for the past three days
    to_date = datetime.now().strftime('%Y-%m-%d')
    from_date = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')

    # Fetch company news for the past week
    news = finnhub_client.company_news(ticker, _from=from_date, to=to_date)

    # Filter and sort news articles by their datetime in descending order (newest first)
    # Exclude articles with empty headline or summary
    filtered_sorted_news = sorted(
        (article for article in news if clean_text(article['headline']) and clean_text(article['summary'])),
        key=lambda x: x['datetime'],
        reverse=True
    )

    newest_news = []
    for article in filtered_sorted_news[:5]:
        article['summary'] = trim_text(article['summary'], 500)
        newest_news.append(article)

    return newest_news


# Function to extract article url from Yahoo Finance
def extract_article_url(ticker):
    stock = yf.Ticker(ticker)
    return [item['link'] for item in stock.news]


# Function to extract article text using BeautifulSoup
def extract_with_bs4(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    article_div = soup.find('div', class_='caas-body')
    article_text = ""

    if article_div:
        paragraphs = article_div.find_all('p')
        article_text = " ".join([p.get_text() for p in paragraphs])

    return article_text


def update_url(ticker, finnhub_news):
    db = get_database()
    collection = db['NewsSentiment']

    for new_article in finnhub_news:
        headline = new_article['headline']
        url = new_article['url']

        if url:
            # Find the matching news in the database by headline
            result = collection.find_one({"ticker": ticker, "articles.headline": headline})

            if result:
                # Update the existing news article with the new URL
                collection.update_one(
                    {"ticker": ticker, "articles.headline": headline},
                    {"$set": {"articles.$.url": url}}
                )
                print(f"Updated article with headline: {headline} with URL: {url}")
            else:
                print(f"No match found for headline: {headline} in the database.")
        else:
            print(f"No URL found for article with headline: {headline}")


def process_all_tickers():
    db = get_database()
    collection = db['NewsSentiment']

    # Get all distinct tickers in the database
    tickers = collection.distinct("ticker")

    finnhub_client = finnhub.Client(api_key=os.environ.get("FINNHUB_API_KEY"))

    # Calculate the date range for the past week
    to_date = datetime.now().strftime('%Y-%m-%d')
    from_date = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')

    # Iterate through each ticker and update the news articles
    for ticker in tickers:
        print(f"Processing ticker: {ticker}")

        # Fetch company news for the past week
        finnhub_news = finnhub_client.company_news(ticker, _from=from_date, to=to_date)

        # Update the news articles in the database with the URL
        update_url(ticker, finnhub_news)


process_all_tickers()
