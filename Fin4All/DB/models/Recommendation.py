from Fin4All.DB.models import InvestmentType

class Recommendation:
    def __init__(self, username, suggestion, type):
        self.username = username
        self.suggestion = suggestion
        self.type = InvestmentType.from_string(type).name
