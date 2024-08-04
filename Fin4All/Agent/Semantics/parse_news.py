from newspaper import Article
from bs4 import BeautifulSoup
import requests
import yfinance as yf
import dotenv
import os
import finnhub
from datetime import datetime, timedelta

dotenv.load_dotenv()
# test_url = "https://finance.yahoo.com/video/intel-needs-lot-things-play-224846113.html"


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


# Function to extract article text using Newspaper3K
def extract_with_newspaper(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text
