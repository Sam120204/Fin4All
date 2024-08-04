from transformers import AutoModel, AutoTokenizer, AutoModelForCausalLM, LlamaForCausalLM, LlamaTokenizerFast
from peft import PeftModel
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
from parse_news import get_finnhub_news
import concurrent.futures

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

def create_collection_if_not_exists(db, collection_name):
    try:
        collection_names = db.list_collection_names()
        if collection_name not in collection_names:
            db.create_collection(collection_name)
            print(f"Created the '{collection_name}' collection.")
    except Exception as e:
        print(f"Error creating collection: {e}")


def load_model_and_tokenizer(base_model, peft_model):
    # Load the tokenizer and model
    tokenizer = LlamaTokenizerFast.from_pretrained(base_model, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    model = LlamaForCausalLM.from_pretrained(base_model, trust_remote_code=True, device_map="cuda:0", load_in_8bit=True)
    model = PeftModel.from_pretrained(model, peft_model)
    model = model.eval()
    return model, tokenizer


def analyze_sentiment(model, tokenizer, text, ticker):
    # Prepare the input prompt
    prompt = f'''Instruction: What is the sentiment of this news about this ticker: {ticker}? Please choose an answer from {{negative/neutral/positive}}
Input: {text}
Answer: '''

    # Tokenize the input text
    tokens = tokenizer(prompt, return_tensors='pt', padding=True, max_length=1000)

    # Generate the response from the model
    res = model.to('cuda').generate(**tokens, max_length=1000)

    # Decode and extract the sentiment
    res_sentences = tokenizer.decode(res[0])
    sentiment = res_sentences.split("Answer: ")[1].strip()

    return sentiment


def update_finnhub_news_sentiment(tickers):
    all_info_and_sentiments = {}
    base_model = "NousResearch/Llama-2-13b-hf"
    peft_model = "FinGPT/fingpt-sentiment_llama2-13b_lora"

    # Load the model and tokenizer once
    model, tokenizer = load_model_and_tokenizer(base_model, peft_model)

    for ticker in tickers:
        print(f"Analyzing news for {ticker}")
        news_info_and_sentiments = []
        latest_news = get_finnhub_news(ticker)

        for news in latest_news:
            try:
                print(f"Analyzing news: {news['headline']}")
                print(f"Summary: {news['summary']}")

                # Use a thread pool executor to manage the timeout
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(
                        analyze_sentiment,
                        model,
                        tokenizer,
                        news['headline'] + ' ' + news['summary'],
                        news['related']
                    )
                    sentiment_result = future.result(timeout=45)

                news_info_and_sentiments.append({
                    'headline': news['headline'],
                    'summary': news['summary'],
                    'sentiment': sentiment_result
                })
            except concurrent.futures.TimeoutError:
                print(f"Sentiment analysis for news titled '{news['headline']}' timed out.")
            except Exception as e:
                print(f"An error occurred: {str(e)}")

        print(news_info_and_sentiments)
        all_info_and_sentiments[ticker] = news_info_and_sentiments
        print(f"Finished analyzing news for {ticker}")
        update_ticker_news_sentiment(ticker, news_info_and_sentiments)

    return all_info_and_sentiments


def update_ticker_news_sentiment(ticker, news_sentiments):
    db = get_database()
    try:
        collection_name = "NewsSentiment"
        create_collection_if_not_exists(db, collection_name)
        collection = db[collection_name]
        document = {
            "articles": news_sentiments
        }
        collection.update_one(
            {"ticker": ticker},
            {"$set": document},
            upsert=True
        )
        print(f"News sentiment for {ticker} stored successfully.")

    except Exception as e:
        print(e)
