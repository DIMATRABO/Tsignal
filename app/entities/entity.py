from sqlalchemy import Column, ForeignKey , String , DateTime, Float , Boolean, Integer
from sqlalchemy.orm import declarative_base , relationship 
from models.model import *

Base = declarative_base()


class AccountEntity(Base):
    __tablename__ = "accounts"
    id = Column("id",String , primary_key=True)
    exchange_id = Column(String, ForeignKey("exchanges.id"))
    exchange = relationship("ExchangeEntity", back_populates="exchanges")
    key_id = Column("key_id",String)
    user_id = Column(String, ForeignKey("users.id"))
    user = relationship("UserEntity", back_populates="accounts")
    orders = relationship("OrderEntity", back_populates="account")

    def __init__(self, id=None, exchange=None, key_id=None, user=None):
        self.id = id
        self.exchange = exchange
        self.key_id = key_id
        self.user = user

    def __repr__(self):
        return "<AccountEntity(id='%s', exchange='%s', user='%s')>" % (
            self.id,
            self.exchange,
            self.user.first_name + " " + self.user.last_name
        )

    def from_domain(self, model: Account , user_id):
        self.id = model.id
        self.exchange = model.exchange
        self.key_id = model.key_id
        self.user_id = user_id

    def to_domain(self):
        return Account(
            id=self.id,
            exchange=self.exchange,
            key_id=self.key_id,
            orders=self.orders
        )

class UserEntity(Base):
    __tablename__ = "users"
    id = Column("id", String, primary_key=True)
    login = Column("login", String, unique=True)
    password = Column("password", String)
    first_name = Column("first_name", String)
    last_name = Column("last_name", String)
    birthday = Column("birthday", DateTime)
    
    accounts = relationship("AccountEntity", back_populates="user")

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
        
        # Map list of accounts to AccountEntities
        self.accounts = [] if model.accounts is None else[AccountEntity.from_domain(account) for account in model.accounts]
 
    def to_domain(self):
        return User(
            id=self.id,
            login=self.login,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
            birthday=self.birthday,
            accounts=[account.to_domain() for account in self.accounts]
        )


class OrderEntity(Base):
    __tablename__ = "orders"
    id = Column("id", String, primary_key=True)
    account_id = Column(String, ForeignKey("accounts.id"))
    account = relationship("AccountEntity", back_populates="orders")
    exchange_id = Column(String, ForeignKey("exchanges.id"))
    exchange = relationship("ExchangeEntity", back_populates="orders")
    is_buy = Column("is_buy", Boolean)
    is_future = Column("is_future", Boolean)
    is_limit = Column("is_limit", Boolean)
    limit_price = Column("limit_price", Float)
    symbol = Column("symbol", String)
    amount = Column("amount", Float)

    def __init__(self, id=None, account=None, exchange=None, is_buy=None, is_future=None,
                 is_limit=None, limit_price=None, symbol=None, amount=None):
        self.id = id
        self.account = account
        self.exchange = exchange
        self.is_buy = is_buy
        self.is_future = is_future
        self.is_limit = is_limit
        self.limit_price = limit_price
        self.symbol = symbol
        self.amount = amount

    def __repr__(self):
        return "<OrderEntity(id='%s', account='%s', exchange='%s')>" % (
            self.id,
            self.account.id,
            self.exchange.name
        )

    def from_domain(self, model: Order):
        self.id = model.id
        self.account_id = model.account_id
        self.exchange_id = model.exchange_id
        self.is_buy = model.is_buy
        self.is_future = model.is_future
        self.is_limit = model.is_limit
        self.limit_price = model.limit_price
        self.symbol = model.symbol
        self.amount = model.amount

    def to_domain(self):
        return Order(
            id=self.id,
            account_id=self.account_id,
            exchange_id=self.exchange_id,
            is_buy=self.is_buy,
            is_future=self.is_future,
            is_limit=self.is_limit,
            limit_price=self.limit_price,
            symbol=self.symbol,
            amount=self.amount
        )


class ExchangeEntity(Base):
    __tablename__ = "exchanges"
    id = Column("id", String, primary_key=True)
    name = Column("name", String)
    orders = relationship("OrderEntity", back_populates="exchange")

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
