from Fin4All.DB.models import InvestmentType
from Fin4All.DB.models.utils import *

class Recommendation:
    def __init__(self, username, suggestion, type):
        self.username = username
        self.suggestion = suggestion
        self.type = InvestmentType.from_string(type).name

def update_recommendation(username, suggestion, type):
    try:
        delete_from_collection_if_exists("recommendation", {"username": username})
        insert_into_collection("recommendation", Recommendation(username, suggestion, type))
    except Exception as e:
        print(e)

def get_recommendation(username):
    return find_from_collection("recommendation", {"username": username})