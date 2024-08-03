from enum import Enum

class InvestmentType(Enum):
    STOCK = 1,
    BOND = 2,
    MUTUAL_FUND = 3,
    @classmethod
    def from_string(cls, s):
        try:
            return cls[s]
        except KeyError:
            raise ValueError(f"'{s}' is not a valid InvestmentType")

class Recommendation:
    def __init__(self, username, suggestion, type):
        self.username = username
        self.suggestion = suggestion
        self.type = InvestmentType.from_string(type).name
