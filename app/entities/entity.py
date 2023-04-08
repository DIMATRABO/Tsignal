from sqlalchemy import Column, ForeignKey , String , DateTime, Float , Boolean
from sqlalchemy.orm import declarative_base 
from models.model import *

Base = declarative_base()


class AccountEntity(Base):
    __tablename__ = "accounts"
    id = Column("id",String , primary_key=True)
    exchange_id = Column(String)
    key_id = Column("key_id",String)
    user_id = Column("user_id", String)

    def __init__(self, id=None, exchange_id=None, key_id=None, user_id=None):
        self.id = id
        self.exchange_id = exchange_id
        self.key_id = key_id
        self.user_id = user_id

    def __repr__(self):
        return "<AccountEntity(id='%s', exchange='%s', user='%s')>" % (
            self.id,
            self.exchange_id,
            self.user_id
        )

    def from_domain(self, model: Account):
        self.id = model.id
        self.exchange_id = None if model.exchange is None else model.exchange.id
        self.key_id = model.key_id
        self.user_id = model.user_id

    def to_domain(self):
        return Account(
            id=self.id,
            exchange=Exchange(self.exchange_id),
            key_id=self.key_id,
            user_id=self.user_id
        )

class UserEntity(Base):
    __tablename__ = "users"
    id = Column("id", String, primary_key=True)
    login = Column("login", String, unique=True)
    password = Column("password", String)
    first_name = Column("first_name", String)
    last_name = Column("last_name", String)
    birthday = Column("birthday", DateTime)
    

    def __init__(self, id=None, login=None, password=None, first_name=None, last_name=None, birthday=None):
        self.id = id
        self.login = login
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        
    def __repr__(self):
        return "<UserEntity(id='%s', first_name='%s', last_name='%s')>" % (
            self.id,
            self.first_name,
            self.last_name
        )
        
    def from_domain(self, model: User):
        self.id = model.id
        self.login = model.login
        self.password = model.password
        self.first_name = model.first_name
        self.last_name = model.last_name
        self.birthday = model.birthday
        

    def to_domain(self):
        return User(
            id=self.id,
            login=self.login,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
            birthday=self.birthday
        )


class OrderEntity(Base):
    __tablename__ = "orders"
    id = Column("id", String, primary_key=True)
    account_id = Column(String, ForeignKey("accounts.id"))
    is_buy = Column("is_buy", Boolean)
    is_future = Column("is_future", Boolean)
    is_limit = Column("is_limit", Boolean)
    limit_price = Column("limit_price", Float)
    base = Column("base", String)
    quote = Column("quote", String)
    amount = Column("amount", Float)

    def __init__(self, id=None, account_id=None, is_buy=None, is_future=None,
                 is_limit=None, limit_price=None, base=None, quote = None ,amount=None):
        self.id = id
        self.account = account_id
        self.is_buy = is_buy
        self.is_future = is_future
        self.is_limit = is_limit
        self.limit_price = limit_price
        self.base = base
        self.quote = quote
        self.amount = amount

    def __repr__(self):
        return "<OrderEntity(id='%s', account='%s')>" % (
            self.id,
            self.account_id
        )

    def from_domain(self, model: Order):
        self.id = model.id
        self.account_id = model.account_id
        self.is_buy = model.is_buy
        self.is_future = model.is_future
        self.is_limit = model.is_limit
        self.limit_price = model.limit_price
        self.base = model.base
        self.quote = model.quote
        self.amount = model.amount

    def to_domain(self):
        return Order(
            id=self.id,
            account_id=self.account_id,
            is_buy=self.is_buy,
            is_future=self.is_future,
            is_limit=self.is_limit,
            limit_price=self.limit_price,
            base=self.base,
            quote=self.quote,
            amount=self.amount
        )


class ExchangeEntity(Base):
    __tablename__ = "exchanges"
    id = Column("id", String, primary_key=True)
    name = Column("name", String)

    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    def __repr__(self):
        return "<ExchangeEntity(id='%s', name='%s')>" % (
            self.id,
            self.name
        )

    def from_domain(self, model: Exchange):
        self.id = model.id
        self.name = model.name

    def to_domain(self):
        return Exchange(
            id=self.id,
            name=self.name
        )
