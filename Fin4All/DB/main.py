from pymongo.mongo_client import MongoClient
from django.conf import settings
from Fin4All.DB.models.Recommendation import Recommendation
from Fin4All.DB.models.utils import *

def update_recommendation(username, suggestion, type):
    try:
        delete_from_collection_if_exists("recommendation", {"username": username})
        insert_into_collection("recommendation", Recommendation(username, suggestion, type))
    except Exception as e:
        print(e)

def get_recommendation(username):
    return find_from_collection("recommendation", {"username": username})