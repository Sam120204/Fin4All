from Fin4All.DB.models import InvestmentType

class Preference:
    def __init__(self, username, detail, type):
        self.username = username
        self.detail = detail
        self.type = InvestmentType.from_string(type).name
