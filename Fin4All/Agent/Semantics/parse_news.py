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


def get_finnhub_news(ticker):
    finnhub_client = finnhub.Client(api_key=os.environ.get("FINNHUB_API_KEY"))

    # Calculate the date range for the past three days
    to_date = datetime.now().strftime('%Y-%m-%d')
    from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

    # Fetch company news for the past three days
    news = finnhub_client.company_news(ticker, _from=from_date, to=to_date)

    # Sort news articles by their datetime in descending order (newest first)
    sorted_news = sorted(news, key=lambda x: x['datetime'], reverse=True)

    # Get the 10 newest articles
    newest_news = sorted_news[:10]

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


api_key = os.environ.get("FINNHUB_API_KEY")
ticker = "USDT-USD"
print(get_finnhub_news(ticker))