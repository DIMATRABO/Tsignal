class GetOneInput:
    id: str = None
    login: str = None
    passwd: str = None

    def __init__(self, id = None  , login = None , passwd = None):
        self.uuid = id
        self.login = login
        self.passwd = passwd