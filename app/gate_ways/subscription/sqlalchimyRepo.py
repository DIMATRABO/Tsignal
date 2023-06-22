from sqlalchemy import   exc
from entities.entity import Base , SubscriptionEntity
from models.model import Subscription 

class SqlAlchimy_repo :
    def __init__(self ):
        self.Base = Base
        
    def save(self, session , subscription:Subscription):
        subscriptionEntity = SubscriptionEntity()
        subscriptionEntity.from_domain(model=subscription)

        session.add(subscriptionEntity)
        try:        
            session.commit()
        except exc.SQLAlchemyError as e:
            session.rollback()
            raise Exception("subscription not saved")
        return subscriptionEntity.to_domain()
        
