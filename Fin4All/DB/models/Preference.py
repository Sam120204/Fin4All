from Fin4All.DB.models.utils import *

default_preference = """Any sector, stable return"""
class Preference:
    def __init__(self, stock = default_preference, bond = default_preference, mutual_fund = default_preference):
        self.stock = stock
        self.bond = bond
        self.mutual_fund = mutual_fund
    
    def __str__(self):
        return f"Preference: stock={self.stock}, bond={self.bond}, mutual_fund={self.mutual_fund})"
    
    @staticmethod
    def from_dict(preference_dict):
        return Preference(
            preference_dict.get("stock", default_preference),
            preference_dict.get("bond", default_preference),
            preference_dict.get("mutual_fund", default_preference)
        )
    
    def to_dict(self):
        return {
            "stock": self.stock,
            "bond": self.bond,
            "mutual_fund": self.mutual_fund
        }
