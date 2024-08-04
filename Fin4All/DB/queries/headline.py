from langchain_openai import OpenAIEmbeddings
from pymongo.mongo_client import MongoClient
from django.conf import settings
from Fin4All.DB.models.utils import *

embeddings_model = OpenAIEmbeddings()

# find highly similar semantic article headlines with query index recently
def vector_search(query):
    embedded_query = embeddings_model.embed_query(query)
    result = db.NewsSentiment.aggregate([
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "headline_embedding",
                "queryVector": embedded_query,
                "numCandidates": 100,
                "limit": 5
            }
        }
    ])
    return result

for doc in vector_search("Warren Buffett selling apple stakes"):
    print(doc)