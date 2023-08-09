class GetAllInput:
    all :str = None
    account_id: str = None
    user_id : str = None
    not_user_id : str = None
    


    def __init__(self, all=None , account_id=None , user_id=None , not_user_id=None):
        self.all = all
        self.account_id = account_id
        self.user_id = user_id
        self.not_user_id = not_user_id