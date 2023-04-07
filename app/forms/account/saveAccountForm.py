from models.model import Account, Exchange

class SaveAccountForm:
    exchange_id: str
    key: str

    def __init__(self , jsonAccount):
        if(  not "exchange_id" in  jsonAccount):
            raise Exception("exchange_id required")
        else:
            self.exchange_id=jsonAccount["exchange_id"]
        
        if(  not "key" in  jsonAccount):
            raise Exception("key required")
        else:
            self.key=jsonAccount["key"]
    
     

    def to_domain(self):
        return Account(
            id=None,
            exchange=Exchange(id=self.exchange_id),
            key_id=None,
            key=self.key
        )