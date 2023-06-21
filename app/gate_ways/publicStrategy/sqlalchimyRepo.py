

from gate_ways.log import Log
from sqlalchemy import   exc
from entities.entity import Base , PublicStrategyEntity , AccountEntity , OrderEntity
from models.model import PublicStrategy 
import uuid


logger = Log()
class SqlAlchimy_repo :
    def __init__(self ):
        self.Base = Base

        
    def save(self, session , publicStrategy:PublicStrategy):
        publicStrategyEntity = PublicStrategyEntity()
        publicStrategyEntity.from_domain(model=publicStrategy)
        publicStrategyEntity.id=str(uuid.uuid4())
        
        session.add(publicStrategyEntity)
        try:        
            session.commit()
        except exc.SQLAlchemyError as e:
            logger.log(e)
            session.rollback()
            raise Exception("publicStrategy not saved")
         
        return publicStrategyEntity.to_domain()
        
