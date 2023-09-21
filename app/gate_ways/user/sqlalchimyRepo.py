

from gate_ways.log import Log
from sqlalchemy import  and_ , exc , or_
from entities.entity import Base , UserEntity 
from models.model import User
from forms.user.userssPaginated import UsersPage
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
        
        users = session.query(UserEntity).all()
        
        return users
    
    def getUserByEmail(self, session , email):
        user = session.query(UserEntity).filter(UserEntity.email == email).first()
        return None if user is None else user.to_domain()
    

    def getActiveUserByEmail(self, session , email):
        user = session.query(UserEntity).filter(UserEntity.email == email , UserEntity.is_actif).first()
        return None if user is None else user.to_domain()
    
    def getUserById(self, session , uuid):
        user = session.query(UserEntity).filter(UserEntity.id == uuid).first()
        return None if user is None else user.to_domain()
    
 


    def getAllPaginated(self, session, page_number, page_size):
        query =  session.query(UserEntity)
        total_records = query.count()
        starting_index = (page_number - 1) * page_size
        users = query.offset(starting_index).limit(page_size).all()
        return UsersPage(
             total_records =  total_records,
            page_number= page_number,
            page_size= page_size,
            users= [user.to_domain() for user in users]
            )


    def getAllByFisrtAndLastName(self, session, first_name, last_name, page_number, page_size):
        query = session.query(UserEntity).filter(and_(UserEntity.first_name == first_name, UserEntity.last_name == last_name))
        total_records = query.count()
        starting_index = (page_number - 1) * page_size
        users = query.offset(starting_index).limit(page_size).all()
        return UsersPage(
             total_records =  total_records,
            page_number= page_number,
            page_size= page_size,
            users= [user.to_domain() for user in users]
            )
    
 
    def getAllByFisrtName(self, session, first_name, page_number, page_size):
        query =  session.query(UserEntity).filter(UserEntity.first_name == first_name)
        total_records = query.count()
        starting_index = (page_number - 1) * page_size
        users = query.offset(starting_index).limit(page_size).all()
        return UsersPage(
             total_records =  total_records,
            page_number= page_number,
            page_size= page_size,
            users= [user.to_domain() for user in users]
            )
    
    def getAllByLastName(self, session, last_name, page_number, page_size):
        query =  session.query(UserEntity).filter(UserEntity.last_name == last_name)
        total_records = query.count()
        starting_index = (page_number - 1) * page_size
        users = query.offset(starting_index).limit(page_size).all()
        return UsersPage(
             total_records =  total_records,
            page_number= page_number,
            page_size= page_size,
            users= [user.to_domain() for user in users]
            )
    
    def getAllByNameOrEmail(self, session, search, page_number, page_size):
        query = session.query(UserEntity).filter(
        or_(
            UserEntity.first_name.ilike(f"%{search}%"),
            UserEntity.last_name.ilike(f"%{search}%"),
            UserEntity.email.ilike(f"%{search}%")
            )
        )
        total_records = query.count()
        starting_index = (page_number - 1) * page_size
        users = query.offset(starting_index).limit(page_size).all()
        return UsersPage(
             total_records =  total_records,
            page_number= page_number,
            page_size= page_size,
            users= [user.to_domain() for user in users]
            )