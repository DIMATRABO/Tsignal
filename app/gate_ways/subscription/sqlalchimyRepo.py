from sqlalchemy import   exc
from entities.entity import Base , SubscriptionEntity
from models.model import Subscription 
from datetime import datetime

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
            raise Exception("subscription not saved"+ str(e))
        return subscriptionEntity.to_domain()
        

    def unsubscribe(self, session, user_id , strategy_id, account_id):
        # Find the subscription to update
        subscription = session.query(SubscriptionEntity).filter(
            SubscriptionEntity.user_id ==  user_id,
            SubscriptionEntity.strategy_id == strategy_id,
            SubscriptionEntity.account_id == account_id
        ).first()

        if subscription:
            # Update the unsubscription date to the current datetime
            subscription.unsubscription_date = datetime.now()
            session.commit()
        return subscription.to_domain()