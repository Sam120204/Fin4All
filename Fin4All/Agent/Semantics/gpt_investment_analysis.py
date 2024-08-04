from openai import OpenAI
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Load environment variables from the .env file
load_dotenv()

MONGO_DB_USER = os.getenv('MONGO_DB_USER')
MONGO_DB_PWD = os.getenv('MONGO_DB_PWD')


def get_database():
    try:
        connect_string = f"mongodb+srv://{MONGO_DB_USER}:{MONGO_DB_PWD}@fin4all.r3ihnkl.mongodb.net/?retryWrites=true&w=majority&appName=Fin4All"
        client = MongoClient(connect_string)
        return client['Fin4All']
    except ConnectionFailure as e:
        print(f"Could not connect to MongoDB: {e}")
        return None


def get_sector_full_name(sector):
    if sector == 'tech':
        return "Technology"
    elif sector == 'renew':
        return "Renewable Energy"
    elif sector == 'pharma':
        return "Biotechnology and Pharmaceuticals"
    return None

def get_financial_data(ticker):
    db = get_database()
    collection = db['TickersStatement']
    financial_data = collection.find_one({'ticker': ticker}, {"_id": 0})

    # Extract balance sheet data
    balance_sheet_data = financial_data.get("balance_sheet", {})
    balance_sheet_info = ""
    for date, details in balance_sheet_data.items():
        balance_sheet_info += f"On {date}, the balance sheet shows:\n"
        for key, value in details.items():
            balance_sheet_info += f"  - {key.replace('_', ' ')}: ${value}\n"

    # Extract cash flow data
    cashflow_data = financial_data.get("cashflow", {})
    cashflow_info = ""
    for date, details in cashflow_data.items():
        cashflow_info += f"On {date}, the cash flow statement includes:\n"
        for key, value in details.items():
            cashflow_info += f"  - {key.replace('_', ' ')}: ${value}\n"

    # Extract income statement data
    income_statement_data = financial_data.get("income_statement_quarter", {})
    income_statement_info = ""
    for date, details in income_statement_data.items():
        income_statement_info += f"On {date}, the income statement shows:\n"
        for key, value in details.items():
            income_statement_info += f"  - {key.replace('_', ' ')}: ${value}\n"

    # Combine all the financial information
    financial_info = f"""
Financial Overview for {ticker}:
Balance Sheet:
{balance_sheet_info}
Cash Flow Statement:
{cashflow_info}
Income Statement:
{income_statement_info}
"""

    return financial_info


def get_sentiment_by_ticker(ticker):
    db = get_database()
    collection = db['NewsSentiment']
    return collection.find_one({'ticker': ticker}, {"_id": 0, "ticker": 1, "articles": 1})

def get_sentiment_by_field(field):
    db = get_database()
    collection = db['NewsSentiment']
    cursor = None
    if field == 'tech':
        tech = [
            "AAPL",  # Apple Inc.
            "MSFT",  # Microsoft Corporation
            "GOOGL",  # Alphabet Inc.
            "AMZN",  # Amazon.com, Inc.
            "META",  # Meta Platforms, Inc.
            "TSLA",  # Tesla, Inc.
            "NVDA",  # NVIDIA Corporation
            "PYPL",  # PayPal Holdings, Inc.
            "ADBE",  # Adobe Inc.
            "INTC",  # Intel Corporation
            "CSCO",  # Cisco Systems, Inc.
            "ORCL",  # Oracle Corporation
            "ACN",  # Accenture plc
            "AVGO",  # Broadcom Inc.
            "QCOM",  # Qualcomm Incorporated
            "SQ",  # Block, Inc.
            "AMD",  # Advanced Micro Devices, Inc.
            "FLNC"  # Fluence Energy, Inc.
        ]
        cursor = collection.find({'ticker': {'$in': tech}}, {'summary': 0})
    elif field == 'renew':
        renewable_energy_or_environmental = [
            "NEE",  # NextEra Energy, Inc.
            "ENPH",  # Enphase Energy, Inc.
            "SEDG",  # SolarEdge Technologies, Inc.
            "FSLR",  # First Solar, Inc.
            "RUN",  # Sunrun Inc.
            "BE",  # Bloom Energy Corporation
            "PLUG",  # Plug Power Inc.
            "SPWR",  # SunPower Corporation
            "NOVA",  # Sunnova Energy International Inc.
            "BLDP",  # Ballard Power Systems Inc.
            "CWEN",  # Clearway Energy, Inc.
            "HASI"  # Hannon Armstrong Sustainable Infrastructure Capital, Inc.
        ]
        cursor = collection.find({'ticker': {'$in': renewable_energy_or_environmental}}, {'summary': 0})
    elif field == 'pharma':
        biotechnology_and_pharmaceuticals = [
            "JNJ",  # Johnson & Johnson
            "PFE",  # Pfizer Inc.
            "MRK",  # Merck & Co., Inc.
            "ABBV",  # AbbVie Inc.
            "LLY",  # Eli Lilly and Company
            "BMY",  # Bristol-Myers Squibb Company
            "UNH",  # UnitedHealth Group Incorporated
            "MDT",  # Medtronic plc
            "BIIB",  # Biogen Inc.
            "AMGN",  # Amgen Inc.
            "GILD",  # Gilead Sciences, Inc.
            "MRNA",  # Moderna, Inc.
            "VRTX"  # Vertex Pharmaceuticals Incorporated
        ]
        cursor = collection.find({'ticker': {'$in': biotechnology_and_pharmaceuticals}}, {'summary': 0})

    if cursor is None:
        return None
    else:
        result = []
        for document in list(cursor):
            info_list = []
            for article in document['articles']:
                info_list.append({
                    'headline': article['headline'],
                    'sentiment': article['sentiment']
                })

            result.append({document['ticker']: info_list})

        return result


def get_sentiment_analysis(ticker=None, field=None):
    if ticker is not None:
        return get_sentiment_by_ticker(ticker)
    elif field is not None:
        return get_sentiment_by_field(field)
    return None


def get_price_by_ticker(ticker):
    db = get_database()
    collection = db['TickersStatement']
    return collection.find_one({'ticker': ticker}, {"_id": 0, "ticker": 1, "price": 1})


def get_price_by_field(field):
    db = get_database()
    collection = db['TickersStatement']
    cursor = None
    if field == 'tech':
        tech = [
            "AAPL",  # Apple Inc.
            "MSFT",  # Microsoft Corporation
            "GOOGL",  # Alphabet Inc.
            "AMZN",  # Amazon.com, Inc.
            "META",  # Meta Platforms, Inc.
            "TSLA",  # Tesla, Inc.
            "NVDA",  # NVIDIA Corporation
            "PYPL",  # PayPal Holdings, Inc.
            "ADBE",  # Adobe Inc.
            "INTC",  # Intel Corporation
            "CSCO",  # Cisco Systems, Inc.
            "ORCL",  # Oracle Corporation
            "ACN",  # Accenture plc
            "AVGO",  # Broadcom Inc.
            "QCOM",  # Qualcomm Incorporated
            "SQ",  # Block, Inc.
            "AMD",  # Advanced Micro Devices, Inc.
            "FLNC"  # Fluence Energy, Inc.
        ]
        cursor = collection.find({'ticker': {'$in': tech}}, {"_id": 0, "ticker": 1, "price": 1})
    elif field == 'renew':
        renewable_energy_or_environmental = [
            "NEE",  # NextEra Energy, Inc.
            "ENPH",  # Enphase Energy, Inc.
            "SEDG",  # SolarEdge Technologies, Inc.
            "FSLR",  # First Solar, Inc.
            "RUN",  # Sunrun Inc.
            "BE",  # Bloom Energy Corporation
            "PLUG",  # Plug Power Inc.
            "SPWR",  # SunPower Corporation
            "NOVA",  # Sunnova Energy International Inc.
            "BLDP",  # Ballard Power Systems Inc.
            "CWEN",  # Clearway Energy, Inc.
            "HASI"  # Hannon Armstrong Sustainable Infrastructure Capital, Inc.
        ]
        cursor = collection.find({'ticker': {'$in': renewable_energy_or_environmental}}, {"_id": 0, "ticker": 1, "price": 1})
    elif field == 'pharma':
        biotechnology_and_pharmaceuticals = [
            "JNJ",  # Johnson & Johnson
            "PFE",  # Pfizer Inc.
            "MRK",  # Merck & Co., Inc.
            "ABBV",  # AbbVie Inc.
            "LLY",  # Eli Lilly and Company
            "BMY",  # Bristol-Myers Squibb Company
            "UNH",  # UnitedHealth Group Incorporated
            "MDT",  # Medtronic plc
            "BIIB",  # Biogen Inc.
            "AMGN",  # Amgen Inc.
            "GILD",  # Gilead Sciences, Inc.
            "MRNA",  # Moderna, Inc.
            "VRTX"  # Vertex Pharmaceuticals Incorporated
        ]
        cursor = collection.find({'ticker': {'$in': biotechnology_and_pharmaceuticals}}, {"_id": 0, "ticker": 1, "price": 1})

    return list(cursor)


def get_price_data(ticker=None, field=None):
    if ticker is not None:
        return get_sentiment_by_ticker(ticker)
    elif field is not None:
        return get_sentiment_by_field(field)
    return None


def format_news_for_prompt(news_data):
    formatted_articles = f"News sentiment for {news_data['ticker']}:\n"
    for article in news_data["articles"]:
        formatted_articles += f"  - {article['headline']} (Sentiment: {article['sentiment']})\n"

    return formatted_articles


def format_field_news_for_prompt(news_data):
    formatted_data = ""
    for sector in news_data:
        for ticker, articles in sector.items():
            formatted_data += f"News sentiment for {ticker}:\n"
            for article in articles:
                formatted_data += f"  - {article['headline']} (Sentiment: {article['sentiment']})\n"

    return formatted_data.strip()


def format_price_data_for_prompt(price_data):
    formatted_data = f"""
    Stock Information for {price_data['ticker']}:
    - Current Price: ${price_data['price']['Current Price']}
    - Price Change compared to a week ago: {price_data['price']['Price Change (%)']:.2f}%
    - 52-Week High: ${price_data['price']['52-Week High']}
    - 52-Week Low: ${price_data['price']['52-Week Low']}
    - Volume: {price_data['price']['Volume']:,}
    """
    return formatted_data.strip()


def format_field_price_data_for_prompt(price_data):
    formatted_data = ""
    for sector in price_data:
            formatted_data += f"""
Stock Information for {sector['ticker']}:
- Current Price: ${sector['price']['Current Price']}
- Price Change compared to a week ago: {sector['price']['Price Change (%)']:.2f}%
- 52-Week High: ${sector['price']['52-Week High']}
- 52-Week Low: ${sector['price']['52-Week Low']}
- Volume: {sector['price']['Volume']:,}
"""
    return formatted_data.strip()


def get_prompt(experience, perference, balance, ticker=None, field=None):
    if ticker is not None:
        financial_data = get_financial_data(ticker)
        sentiment_data = format_news_for_prompt(get_sentiment_analysis(ticker=ticker))
        price_data = format_price_data_for_prompt(get_price_by_ticker(ticker))
        prompt = f'''
Here is an investment analysis request. The investor currently has a balance of ${balance} and is looking for investment opportunities in the {experience} market.
The investor has a preference for {perference} strategies. The investor is interested in investing in {ticker}.
This investment analysis request is based on the following data for {ticker}:
1. **Financial Data:**
{financial_data}
2. **Current News Sentiment Analysis:**
{sentiment_data}
3. **Stock Price Data:**
{price_data}
Based on this information, what investment strategy would you recommend to the investor? Try to be specific on numbers and strategies and provide a detailed reasoning on why to invest, why to short, why to hold or why to avoid.
Your final response should be in the format of a detailed investment report.
'''
        return prompt
    elif field is not None:
        sentiment_data = format_field_news_for_prompt(get_sentiment_analysis(field=field))
        price_data = format_field_price_data_for_prompt(get_price_by_field(field))
        prompt = f'''
Here is an investment analysis request. The investor currently has a balance of ${balance} and is looking for investment opportunities in the {experience} market.
The investor has a preference for {perference} strategies. The investor is interested in investing in the {get_sector_full_name(field)} sector.
This investment analysis request is based on the following data for the {get_sector_full_name(field)} sector:
1. **Current News Sentiment Analysis of each ticker in the sector:**
{sentiment_data}
2. **Stock Price Data of each ticker in the sector:**
{price_data}
Based on this information, what investment strategy would you recommend to the investor? Try to be specific on tickers, numbers and strategies and provide a detailed reasonin on why to invest, why to short, why to hold or why to avoid.
Your final response should be in the format of a detailed investment report. Try to incorporate an educational aspect on how investing in field of {get_sector_full_name(field)} can be beneficial for both the investor and human society.
        '''
        return prompt


# Function to generate sentiment summary using OpenAI
def generate_sentiment_summary(ticker, articles):
    # Prepare the prompt
    prompt = f"""
    Here are the summarized sentiments for the news articles about {ticker}:
    """

    for article in articles:
        prompt += f"- {article['headline']}: {article['sentiment'].replace('</s>', '')}\n"

    prompt += "\nBased on this information, please summarize the overall sentiment toward {ticker}."
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    # Call the OpenAI API to generate the summary
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        stream=True,
        max_tokens=4000
    )

    full_text = ""
    for chunk in response:
        full_text += chunk.choices[0].delta.content or ""

    print(full_text.strip())
    return full_text.strip()


# Function to update MongoDB with the sentiment summary
def update_ticker_with_sentiment_summary():
    db = get_database()
    collection = db['NewsSentiment']

    # Fetch all tickers with articles
    tickers = collection.find({"articles": {"$exists": True, "$not": {"$size": 0}}})

    for ticker_data in tickers:
        ticker = ticker_data['ticker']
        articles = ticker_data['articles']

        # Generate sentiment summary using OpenAI
        sentiment_summary = generate_sentiment_summary(ticker, articles)

        # Update the MongoDB document with the sentiment summary
        collection.update_one(
            {"_id": ticker_data['_id']},
            {"$set": {"sentiment_summary": sentiment_summary}}
        )
        print(f"Updated sentiment summary for ticker: {ticker}")


def get_gpt_recommendation(experience, perference, balance, ticker=None, field=None):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "user",
                    "content": get_prompt(experience, perference, balance, ticker, field)
                }
            ],
            stream=True,
            max_tokens=4000
        )
        full_text = ""
        for chunk in response:
            full_text += chunk.choices[0].delta.content or ""

        print(full_text.strip())
        return full_text.strip()
    except Exception as e:
        print(e)
        return f"Error: {str(e)}"


def store_gpt_recommendation_in_db(user, experience, perference, balance, ticker=None, field=None):
    db = get_database()
    collection = db['recommendation']

    recommendation = get_gpt_recommendation(experience, perference, balance, ticker, field)

    try:
        collection.update_one({"username": user},
                              {"$set": {"stock_suggestion": recommendation}},
                              upsert=True
        )
        print("Recommendation stored successfully.")
    except Exception as e:
        print(e)
