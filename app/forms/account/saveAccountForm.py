from models.model import Account, Exchange

class SaveAccountForm:

    exchange_id: str
    name: str
    currency: str
    key: str

    def __init__(self , jsonAccount):
        if(  not "exchange_id" in  jsonAccount):
            raise Exception("exchange_id required")
        else:
            self.exchange_id=jsonAccount["exchange_id"]


        if(  not "name" in  jsonAccount):
            raise Exception("name required")
        else:
            self.name=jsonAccount["name"]
        if(  not "currency" in  jsonAccount):
            raise Exception("currency required")
        else:
            self.currency=jsonAccount["currency"]

        
        if(  not "key" in  jsonAccount):
            raise Exception("key required")
        else:
            self.key=jsonAccount["key"]
    
     

    def to_domain(self):
        return Account(
            id=None,
            name=self.name,
            exchange=Exchange(id=self.exchange_id),
            key_id=None,
            currency=self.currency,
            key=self.key
        )