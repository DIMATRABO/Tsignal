from models.model import Account, Exchange

class SaveAccountForm:

    exchange_id: str
    name: str
    currency: str
    api_key: str
    secret: str
    password: str

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

        
        if(  not "api_key" in  jsonAccount):
            raise Exception("api_key required")
        else:
            self.api_key=jsonAccount["api_key"]


        if(  not "secret" in  jsonAccount):
            raise Exception("secret required")
        else:
            self.secret=jsonAccount["secret"]
    

        if(  not "password" in  jsonAccount):
            self.password=None
        else:
            self.password=jsonAccount["password"]
    
     
  
    def to_domain(self):

        if self.password == None:
            return Account(
            id=None,
            name=self.name,
            exchange=Exchange(id=self.exchange_id),
            key_id=None,
            currency=self.currency,
            key={
                "apiKey": self.api_key,
                "secret": self.secret
                }
            )



        return Account(
            id=None,
            name=self.name,
            exchange=Exchange(id=self.exchange_id),
            key_id=None,
            currency=self.currency,
            key={
                "apiKey": self.api_key,
                "password": self.password,
                "secret": self.secret
                }
        )