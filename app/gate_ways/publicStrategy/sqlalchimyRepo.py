

from gate_ways.log import Log
from sqlalchemy import   exc
from entities.entity import Base , PublicStrategyEntity , SubscriptionEntity 
from models.model import PublicStrategy 
from forms.publicStrategy.publicStrategiesPaginated import PublicStrategiesPaginated
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
        


    def update(self, session , publicStrategy:PublicStrategy):
        publicStrategyEntity = PublicStrategyEntity()
        publicStrategyEntity.from_domain(model=publicStrategy)
        
        session.merge(publicStrategyEntity)
        try:        
            session.commit()
        except exc.SQLAlchemyError as e:
            logger.log(e)
            session.rollback()
            raise Exception("publicStrategy not updated")
         
      
    """ 
    def deleteUsersPublicStrategy(self, session, publicStrategy, user_id):
        try:
            # Delete associated orders first
            session.query(OrderEntity).filter(OrderEntity.publicStrategy_id == publicStrategy.webhook_id, PublicStrategyEntity.account_id == AccountEntity.id, AccountEntity.user_id == user_id).delete(synchronize_session='fetch')

            # Delete the publicStrategy only if it belongs to the user
            num_deleted = session.query(PublicStrategyEntity).filter(PublicStrategyEntity.id == publicStrategy.id, PublicStrategyEntity.account_id == AccountEntity.id, AccountEntity.user_id == user_id).delete(synchronize_session='fetch')
            if num_deleted == 0:
                # Handle case where no matching records were found
                raise Exception("No matching records found for publicStrategy ID {} belonging to user ID {}".format(publicStrategy.id, user_id))

            session.commit()
        except exc.SQLAlchemyError as e:
            session.rollback()
            raise Exception("Error deleting publicStrategy with ID {} belonging to user ID {}: {}".format(publicStrategy.id, user_id, str(e)))
    """

    def getAllStrategies(self, session):
        strategies = session.query(PublicStrategyEntity).all()
        return [publicStrategy.to_domain() for publicStrategy in strategies]
      
 
    def getPublicStrategyById(self, session , uuid):
        publicStrategy = session.query(PublicStrategyEntity).filter(PublicStrategyEntity.id == uuid).first()
        return None if publicStrategy == None else publicStrategy.to_domain()
    
    def getStrategyByWebhookId(self, session , webhookid):
        strategy = session.query(PublicStrategyEntity).filter(PublicStrategyEntity.webhook_id == webhookid).first()
        return None if strategy == None else strategy.to_domain()
    
  
    def getAllPaginated(self, session, page_number, page_size):
        query = session.query(PublicStrategyEntity).offset((page_number - 1) * page_size).limit(page_size)

        total_records = query.count()
        starting_index = (page_number - 1) * page_size
     
        strategies = query.offset(starting_index).limit(page_size).all()

        return PublicStrategiesPaginated(
            total_records =  total_records,
            page_number= page_number,
            page_size= page_size,
            strategies= [strategy.to_domain() for strategy in strategies]
            )

    
    def getAllByAccountId(self , session, account_id, page_number, page_size):
        subquery = session.query(SubscriptionEntity.strategy_id).filter(
            SubscriptionEntity.account_id == account_id
        ).subquery()

        strategies = session.query(PublicStrategyEntity).filter(
            PublicStrategyEntity.webhook_id.in_(subquery)
        ).offset((page_number - 1) * page_size).limit(page_size)

        return [strategy.to_domain() for strategy in strategies]


    def getAllByUserId(self, session, user_id, page_number, page_size):
        subquery = session.query(SubscriptionEntity.strategy_id).filter(
            SubscriptionEntity.user_id == user_id
        ).subquery()

        strategies = session.query(PublicStrategyEntity).filter(
            PublicStrategyEntity.webhook_id.in_(subquery)
        ).offset((page_number - 1) * page_size).limit(page_size)

        return [strategy.to_domain() for strategy in strategies]
