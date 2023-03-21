

from gate_ways.log import Log
from sqlalchemy import  and_ , exc
from entities.entity import Base , UserEntity 
from models.model import User
import uuid


logger = Log()
class SqlAlchimy_repo :
    def __init__(self ):
        self.Base = Base

        
    def save(self, session , user:User):
        userEntity = UserEntity()
        userEntity.from_domain(model=user)
        userEntity.id=str(uuid.uuid4())
        
        session.add(userEntity)
        try:        
            session.commit()
        except exc.SQLAlchemyError as e:
            logger.log(e)
            session.rollback()
            raise Exception("user not saved")
         
        return userEntity.to_domain()
        


    def update(self, session , user:User):
        userEntity = UserEntity()
        userEntity.from_domain(model=user)
        
        session.merge(userEntity)
        try:        
            session.commit()
        except exc.SQLAlchemyError as e:
            logger.log(e)
            session.rollback()
            raise Exception("user not updated")
         
      
    
    def delete(self, session , user):
        userEntity = UserEntity()
        userEntity.from_domain(model=user)
        
        session.delete(userEntity)
        try:        
            session.commit()
        except exc.SQLAlchemyError as e:
            logger.log(e)
            session.rollback()
            raise Exception("user not deleted")
         
      
    

    def getAllUsers(self, session):
        
        users = session.query("users")
        
        return users

    def getUserByLogin(self, session , login):
        user = session.query(UserEntity).filter(UserEntity.login == login).first()
        return None if user == None else user.to_domain()
    
    def getUserById(self, session , uuid):
        user = session.query(UserEntity).filter(UserEntity.id == uuid).first()
        return None if user == None else user.to_domain()
    
    def getUserByLoginPasswd(self, session , login , passwd):
        first =  session.query(UserEntity).filter(and_(UserEntity.login == login ,UserEntity.password == passwd)).first()
        return first
        
    