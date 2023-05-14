class GetAllInput:
    all :str = None
    account_id: str = None


    def __init__(self, all=None , account_id=None):
        self.all = all
        self.account_id = account_id