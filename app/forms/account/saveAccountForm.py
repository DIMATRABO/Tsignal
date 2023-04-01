from models.model import Account, Exchange

class SaveAccountForm:
    exchange_id: str
    api_key: str
    api_secret: str

    def __init__(self , jsonAccount):
        if(  not "exchange_id" in  jsonAccount):
            raise Exception("exchange_id required")
        else:
            self.exchange_id=jsonAccount["exchange_id"]
        
        if(  not "api_key" in  jsonAccount):
            raise Exception("api_key required")
        else:
            self.api_key=jsonAccount["api_key"]
    
        if(  not "api_secret" in  jsonAccount):
            raise Exception("api_secret required")
        else:
            self.api_secret=jsonAccount["api_secret"]

    

    def to_domain(self):
        return Account(
            id=None,
            exchange=Exchange(id=self.exchange_id),
            key_id=None,
            key={"api_key":self.api_key , "api_secret": self.api_secret}
        )