class GetAllInput:
    all :str = None
    first_name: str = None
    last_name: str = None


    def __init__(self, all=None , first_name=None , last_name=None):
        self.all = all
        self.first_name = first_name
        self.last_name = last_name