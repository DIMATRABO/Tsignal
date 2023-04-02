

from gate_ways.log import Log
from sqlalchemy import   exc
from entities.entity import Base , AccountEntity 
from gate_ways.account.secretsManager import SecretRepo
from models.model import Account
import uuid


secretRepo = SecretRepo()
logger = Log()
class SqlAlchimy_repo :
    def __init__(self ):
        self.Base = Base

        
    def save(self, session , account:Account , user_id):
        accountEntity = AccountEntity()
        accountEntity.from_domain(model=account,user_id=user_id)
        accountEntity.id=str(uuid.uuid4())
        
        session.add(accountEntity)
        try:        
            session.commit()
        except exc.SQLAlchemyError as e:
            logger.log(e)
            session.rollback()
            raise Exception("account not saved")
         
        return accountEntity.to_domain()
        


    def update(self, session , account:Account):
        accountEntity = AccountEntity()
        accountEntity.from_domain(model=account)
        
        session.merge(accountEntity)
        try:        
            session.commit()
        except exc.SQLAlchemyError as e:
            logger.log(e)
            session.rollback()
            raise Exception("account not updated")
         
      
    
    def delete(self, session , account):
        accountEntity = AccountEntity()
        accountEntity.from_domain(model=account)
        
        session.delete(accountEntity)
        try:        
            session.commit()
        except exc.SQLAlchemyError as e:
            logger.log(e)
            session.rollback()
            raise Exception("account not deleted")
         
      

    def getAllAccounts(self, session):
        accounts = session.query("accounts")
        return accounts

 
    def getAccountById(self, session , uuid):
        account = session.query(AccountEntity).filter(AccountEntity.id == uuid).first()
        return None if account == None else account.to_domain()


    def loadKey(self, account:Account):
        account.key = secretRepo.read(account.key_id)
        return account
    
    def getAllByUserId(self, session , user_id):
        accounts = session.query("accounts")
        return accounts


    def getAllByExchangeId(self, session, exchange_id):
            accounts = session.query("accounts")
            return accounts
