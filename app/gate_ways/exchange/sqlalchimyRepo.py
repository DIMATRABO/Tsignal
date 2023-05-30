from entities.entity import Base , ExchangeEntity

class SqlAlchimy_repo :
    def __init__(self ):
        self.Base = Base

        


    def getAll(self, session ):
        exchanges = session.query(ExchangeEntity).all()
        return [exchange.to_domain() for exchange in exchanges]
      
    def getById(self, session , id):
        exchange = session.query(ExchangeEntity).filter(ExchangeEntity.id == id).first()
        return None if exchange == None else exchange.to_domain()
    