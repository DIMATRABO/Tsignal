

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
        return userEntity.to_domain()
         
      
    
    def delete(self, session , user):
        num_deleted = session.query(UserEntity).filter_by(id=user.id).delete()
        if num_deleted == 0:
            # handle case where no matching records were found
            raise Exception("No matching records found for user ID {}".format(user.id))

        try:
            session.commit()
        except exc.SQLAlchemyError as e:
            logger.log(e)
            session.rollback()
            raise Exception("Error deleting user with ID {}".format(user.id))
            
    

    def getAllUsers(self, session):
        
        users = session.query("users")
        
        return users

    def getUserByEmail(self, session , email):
        user = session.query(UserEntity).filter(UserEntity.email == email).first()
        return None if user == None else user.to_domain()
    
    def getUserById(self, session , uuid):
        user = session.query(UserEntity).filter(UserEntity.id == uuid).first()
        return None if user == None else user.to_domain()
    
