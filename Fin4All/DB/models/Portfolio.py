from Fin4All.DB.models.utils import *
from Fin4All.DB.models.ExperienceLevel import *
from Fin4All.DB.models.Preference import *

class Portfolio():
    def __init__(self, username, experience, balance, preference):
        self.username = username
        self.experience = experience
        self.balance = balance
        self.preference = preference

    def __str__(self):
        return f"Portfolio: {self.username}, {self.experience}, {self.balance}, {self.preference}"
    
    @staticmethod
    def from_dict(portfolio_dict):
        return Portfolio(
            portfolio_dict.get("username", ""),
            ExperienceLevel.from_string(portfolio_dict.get("experience", "BEGINNER")).name,
            portfolio_dict.get("balance", 0),
            Preference.from_dict(portfolio_dict.get("preference", {}))
        )

    def to_dict(self):
        return {
            "username": self.username,
            "experience": self.experience,
            "balance": self.balance,
            "preference": self.preference.to_dict()
        }

def update_portfolio(username, portfolio):
    try:
        delete_from_collection_if_exists("portfolio", {"username": username})
        insert_into_collection("portfolio", portfolio)
    except Exception as e:
        print(e)

def get_portfolio(username):
    portfolio = find_from_collection("portfolio", {"username": username})
    if portfolio is None:
        default = {
            "username": username, 
            "experience": ExperienceLevel.BEGINNER, 
            "balance": 0, 
            "preference": Preference()
        }
        insert_into_collection("portfolio", default)
        return default
    return portfolio
