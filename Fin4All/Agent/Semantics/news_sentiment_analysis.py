from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
import dotenv
import finnhub

dotenv.load_dotenv()

def check_if_subjective(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(text)
    return sentiment['neu'] > 0.7


def get_general_sentiment(tickers):
    formatted_reports = []
    finnhub_client = finnhub.Client(api_key=os.environ.get("FINNHUB_API_KEY"))

    for ticker in tickers:
        report = finnhub_client.news_sentiment(ticker)
        formatted_report = f"""
            **{report['symbol']}**:
            - **News Score**: {report['companyNewsScore']}
            - **Sentiment**: {report['sentiment']['bullishPercent'] * 100}% Bullish, {report['sentiment']['bearishPercent'] * 100}% Bearish
            - **Articles This Week**: {report['buzz']['articlesInLastWeek']}
            """
        formatted_reports.append(formatted_report.strip())

    return "\n".join(formatted_reports)
