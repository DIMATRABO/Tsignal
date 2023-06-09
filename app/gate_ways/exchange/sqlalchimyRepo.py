from sqlalchemy import   exc
from entities.entity import Base , ExchangeEntity
from models.model import Exchange 

class SqlAlchimy_repo :
    def __init__(self ):
        self.Base = Base

        


    def getAll(self, session ):
        exchanges = session.query(ExchangeEntity).all()
        return [exchange.to_domain() for exchange in exchanges]
      
    def getById(self, session , id):
        exchange = session.query(ExchangeEntity).filter(ExchangeEntity.id == id).first()
        return None if exchange == None else exchange.to_domain()
        
    def save(self, session , exchange:Exchange):
        exchangeEntity = ExchangeEntity()
        exchangeEntity.from_domain(model=exchange)

        session.add(exchangeEntity)
        try:        
            session.commit()
        except exc.SQLAlchemyError as e:
            session.rollback()
            raise Exception("exchange not saved")
        return exchangeEntity.to_domain()
        
