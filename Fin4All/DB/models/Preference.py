from Fin4All.DB.models import InvestmentType, Preference
from Fin4All.DB.models.utils import *

class Preference:
    def __init__(self, username, detail, type):
        self.username = username
        self.detail = detail
        self.type = InvestmentType.from_string(type).name

def update_preference(username, detail, type):
    try:
        delete_from_collection_if_exists("preference", {"username": username})
        insert_into_collection("preference", Preference(username, detail, type))
    except Exception as e:
        print(e)

def get_preference(username):
    return find_from_collection("preference", {"username": username})