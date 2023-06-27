

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
        
        return [user.to_domain() for user in users]


    
    def getUserById(self, session , uuid):
        user = session.query(UserEntity).filter(UserEntity.id == uuid).first()
        return None if user == None else user.to_domain()
    

    


    def getAllPaginated(self, session, page_number, page_size):
        users = session.query(UserEntity).offset((page_number - 1) * page_size).limit(page_size)
        return [user.to_domain() for user in users]

    def getAllByFisrtAndLastName(self, session, first_name, last_name, page_number, page_size):
        users = session.query(UserEntity).filter(
            and_(UserEntity.first_name == first_name, UserEntity.last_name == last_name)
        ).offset((page_number - 1) * page_size).limit(page_size)
        return [user.to_domain() for user in users]

    def getAllByFisrtName(self, session, first_name, page_number, page_size):
        users = session.query(UserEntity).filter(
            UserEntity.first_name == first_name
        ).offset((page_number - 1) * page_size).limit(page_size)
        return [user.to_domain() for user in users]

    def getAllByLastName(self, session, last_name, page_number, page_size):
        users = session.query(UserEntity).filter(
            UserEntity.last_name == last_name
        ).offset((page_number - 1) * page_size).limit(page_size)
        return [user.to_domain() for user in users]
    
