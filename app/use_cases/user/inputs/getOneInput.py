class GetOneInput:
    uuid: str = None
    login: str = None
    passwd: str = None

    def __init__(self, uuid = None  , login = None , passwd = None):
        self.uuid = uuid
        self.login = login
        self.passwd = passwd