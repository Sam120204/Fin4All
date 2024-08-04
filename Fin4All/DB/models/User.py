from Fin4All.DB.models.utils import *
class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

def get_user_by_credential(username, password):
    return find_from_collection("users", {"username": username, "password": password})

def create_user(username, password):
    return insert_into_collection("users", {"username": username, "password": password})