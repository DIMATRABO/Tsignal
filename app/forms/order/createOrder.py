from models.model import Order

class CreateOrderForm:
    key:str = None
    is_buy: bool = None
    is_future: bool = None
    is_limit: bool = None
    limit_price: float = None
    symbol: str = None
    symbol_id:str = None
    amount: float = None


    def __init__(self , jsonAccount):
       
        if(  not "key" in  jsonAccount):
            raise Exception("key required")
        else:
            self.key=jsonAccount["key"]

        if(  not "is_buy" in  jsonAccount):
            raise Exception("is_buy required")
        else:
            self.is_buy=jsonAccount["is_buy"]
    
        if(  not "is_future" in  jsonAccount):
            raise Exception("is_future required")
        else:
            self.is_future=jsonAccount["is_future"]

        if(  not "is_limit" in  jsonAccount):
            raise Exception("is_limit required")
        else:
            self.is_limit=jsonAccount["is_limit"]
        
        if(  not "limit_price" in  jsonAccount):
            raise Exception("limit_price required")
        else:
            self.limit_price=jsonAccount["limit_price"]
    
        if(  not "symbol" in  jsonAccount):
            raise Exception("symbol required")
        else:
            self.symbol=jsonAccount["symbol"]

        if(  not "symbol_id" in  jsonAccount):
            raise Exception("symbol_id required")
        else:
            self.symbol_id=jsonAccount["symbol_id"]

        if(  not "amount" in  jsonAccount):
            raise Exception("amount required")
        else:
            self.amount=jsonAccount["amount"]


    

    def to_domain(self):
        return Order(
            id=None,
            is_buy=self.is_buy,
            is_future=self.is_future,
            is_limit=self.is_limit,
            limit_price=self.limit_price,
            symbol=self.symbol,
            symbol_id = self.symbol_id,
            amount=self.amount
        )