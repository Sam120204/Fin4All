from Fin4All.DB.models import InvestmentType
from Fin4All.DB.models.utils import *

default_suggestion = "No suggestion available"
class Recommendation:
    def __init__(self, username, stock_suggestion, bond_suggestion, mutual_fund_suggestion):
        self.username = username
        self.stock_suggestion = stock_suggestion
        self.bond_suggestion = bond_suggestion
        self.mutual_fund_suggestion = mutual_fund_suggestion

    def __str__(self):
        return f"Recommendation for {self.username}: {self.stock_suggestion}, {self.bond_suggestion}, {self.mutual_fund_suggestion}"
    
    @staticmethod
    def from_dict(recommendation_dict):
        return Recommendation(
            recommendation_dict.get("username", ""),
            recommendation_dict.get("stock_suggestion", default_suggestion),
            recommendation_dict.get("bond_suggestion", default_suggestion),
            recommendation_dict.get("mutual_fund_suggestion", default_suggestion)
        )

    def to_dict(self):
        return {
            "username": self.username,
            "stock_suggestion": self.stock_suggestion,
            "bond_suggestion": self.bond_suggestion,
            "mutual_fund_suggestion": self.mutual_fund_suggestion
        }

def update_recommendation(username, data):
    try:
        delete_from_collection_if_exists("recommendation", {"username": username})
        insert_into_collection("recommendation", Recommendation.from_dict(data))
    except Exception as e:
        print(e)

def get_recommendation(username):
    return find_from_collection("recommendation", {"username": username})