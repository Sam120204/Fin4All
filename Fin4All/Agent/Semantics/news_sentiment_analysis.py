from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from parse_news import extract_with_bs4, extract_article_url
from openai import OpenAI
import os
import dotenv


def check_if_subjective(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(text)
    return sentiment['neu'] > 0.7





for url in extract_article_url("AAPL"):
    print(url)
    print(extract_with_bs4(url))
    print(check_if_subjective(extract_with_bs4(url)))

