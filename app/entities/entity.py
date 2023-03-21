from sqlalchemy import Column, String , DateTime, Float , Boolean, Integer
from sqlalchemy.orm import declarative_base
from models.model import *

Base = declarative_base()


class UserEntity(Base):
    __tablename__ = "users"
    id = Column("id",String , primary_key=True)
    login= Column("login",String, unique=True )
    password=Column("password",String)
    first_name= Column("first_name",String)
    last_name=Column("last_name",String)
    birthday=Column("birthday",DateTime)
    balance = Column("balance", Float)
  

    def __init__(self,id=None , login=None , password=None, first_name =None, last_name =None,  birthday =None , balance=None):
        self.id=id
        self.login=login
        self.password=password
        self.first_name=first_name
        self.last_name=last_name
        self.birthday=birthday
        self.balance = balance
     

        
    def __repr__(self):
        return "<UserEntity(id='%s', first_name='%s', last_name='%s')>" % (
            self.id,
            self.first_name,
            self.last_name
        )
        
    def from_domain(self,model : User):
        self.id=model.id
        self.login=model.login
        self.password=model.password
        self.first_name=model.first_name
        self.last_name=model.last_name
        self.birthday=model.birthday
        self.balance=model.balance
 
    def to_domain(self):
        return User(
            id=self.id,
            login =self.login,
            password=self.password,
            first_name = self.first_name,
            last_name = self.last_name,
            birthday = self.birthday,
            balance = self.balance
            )
       
    
