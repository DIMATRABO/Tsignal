from entities.entity import Base , ExchangeEntity

class SqlAlchimy_repo :
    def __init__(self ):
        self.Base = Base

        


    def getAll(self, session ):
        exchanges = session.query(ExchangeEntity).allf()
        return [exchange.to_domain() for exchange in exchanges]
      
 