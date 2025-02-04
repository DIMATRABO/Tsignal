

from gate_ways.log import Log
from sqlalchemy import   exc
from entities.entity import Base , StrategyEntity , AccountEntity , OrderEntity
from models.model import Strategy 
import uuid


logger = Log()
class SqlAlchimy_repo :
    def __init__(self ):
        self.Base = Base

        
    def save(self, session , strategy:Strategy):
        strategyEntity = StrategyEntity()
        strategyEntity.from_domain(model=strategy)
        strategyEntity.id=str(uuid.uuid4())
        
        session.add(strategyEntity)
        try:        
            session.commit()
        except exc.SQLAlchemyError as e:
            logger.log(e)
            session.rollback()
            raise Exception("strategy not saved")
         
        return strategyEntity.to_domain()
        


    def update(self, session , strategy:Strategy):
        strategyEntity = StrategyEntity()
        strategyEntity.from_domain(model=strategy)
        
        session.merge(strategyEntity)
        try:        
            session.commit()
        except exc.SQLAlchemyError as e:
            logger.log(e)
            session.rollback()
            raise Exception("strategy not updated")
         
      
    def deleteUsersStrategy(self, session, strategy, user_id):
        try:
            # Delete associated orders first
            session.query(OrderEntity).filter(OrderEntity.strategy_id == strategy.webhook_id, StrategyEntity.account_id == AccountEntity.id, AccountEntity.user_id == user_id).delete(synchronize_session='fetch')

            # Delete the strategy only if it belongs to the user
            num_deleted = session.query(StrategyEntity).filter(StrategyEntity.id == strategy.id, StrategyEntity.account_id == AccountEntity.id, AccountEntity.user_id == user_id).delete(synchronize_session='fetch')
            if num_deleted == 0:
                # Handle case where no matching records were found
                raise Exception("No matching records found for strategy ID {} belonging to user ID {}".format(strategy.id, user_id))

            session.commit()
        except exc.SQLAlchemyError as e:
            session.rollback()
            raise Exception("Error deleting strategy with ID {} belonging to user ID {}: {}".format(strategy.id, user_id, str(e)))


    def getAllStrategies(self, session):
        strategies = session.query(StrategyEntity).all()
        return [strategy.to_domain() for strategy in strategies]
      
 
    def getStrategyById(self, session , uuid):
        strategy = session.query(StrategyEntity).filter(StrategyEntity.id == uuid).first()
        return None if strategy == None else strategy.to_domain()
    
    def getStrategyByIdAndUserId(self, session, uuid, user_id):
        strategy = session.query(StrategyEntity).filter(
        StrategyEntity.id == uuid,
        StrategyEntity.account_id.in_(
            session.query(AccountEntity.id).filter(AccountEntity.user_id == user_id)
            )
        ).first()
        return None if strategy is None else strategy.to_domain()

    def getStrategyByWebhookId(self, session , webhookid):
        strategy = session.query(StrategyEntity).filter(StrategyEntity.webhook_id == webhookid).first()
        return None if strategy == None else strategy.to_domain()
    
    def getAllByAccountId(self, session , account_id):
        strategies = session.query(StrategyEntity).filter_by(account_id=account_id).all()
        return [strategy.to_domain() for strategy in strategies]

    def getAllByUserId(self , session, user_id):
        strategies = session.query(StrategyEntity).filter(
        StrategyEntity.account_id.in_(
            session.query(AccountEntity.id).filter(AccountEntity.user_id == user_id)
            )
        ).all()
        return [strategy.to_domain() for strategy in strategies]
