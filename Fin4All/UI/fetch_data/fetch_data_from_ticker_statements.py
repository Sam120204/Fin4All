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
