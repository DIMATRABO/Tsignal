
class CreateBasicOrderForm:
    key:str = None
    side: str = None
    closing_price:float=None


    def __init__(self , jsonAccount):
       
        if(  not "key" in  jsonAccount):
            raise Exception("key required")
        else:
            self.key=jsonAccount["key"]

        if(  not "side" in  jsonAccount):
            raise Exception("side required")
        
        elif(not( jsonAccount["side"] == "BUY"  or jsonAccount["side"] == "SELL") ):
            raise Exception("side must be equal to BUY or SELL ")
        else:
            self.side=jsonAccount["side"]



        if(  not "closing_price" in  jsonAccount):
            raise Exception("closing_price required")
        else:
            self.closing_price=jsonAccount["closing_price"]
        

