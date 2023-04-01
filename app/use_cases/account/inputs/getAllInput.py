class GetAllInput:
    all :str = None
    user_id: str = None
    exchange_id: str = None


    def __init__(self, all=None , user_id=None , exchange_id=None):
        self.all = all
        self.user_id = user_id
        self.exchange_id = exchange_id