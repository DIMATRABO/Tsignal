from sqlalchemy import Column , String , DateTime, Float , Boolean , UniqueConstraint
from sqlalchemy.orm import declarative_base 
from models.model import *

Base = declarative_base()


class AccountEntity(Base):
    __tablename__ = "accounts"
    id = Column("id",String , primary_key=True)
    name = Column("name", String)
    exchange_id = Column(String)
    key_id = Column("key_id",String)
    balance = Column("balance", Float)
    currency = Column("currency",String)
    user_id = Column("user_id", String)
    created_at =Column("created_at", DateTime)


    def __init__(self, id=None, name=None, exchange_id=None, key_id=None, balance=None, currency=None, user_id=None , created_at=None):
        self.id = id
        self.name = name
        self.exchange_id = exchange_id
        self.key_id = key_id
        self.balance = balance
        self.currency = currency
        self.user_id = user_id
        self.created_at = created_at

    def __repr__(self):
        return "<AccountEntity(id='%s', exchange='%s', user='%s')>" % (
            self.id,
            self.exchange_id,
            self.user_id
        )

    def from_domain(self, model: Account):
        self.id = model.id
        self.name = model.name
        self.exchange_id = None if model.exchange is None else model.exchange.id
        self.key_id = model.key_id
        self.balance = model.balance
        self.currency = model.currency
        self.user_id = model.user_id
        self.created_at = model.created_at

    def to_domain(self):
        return Account(
            id=self.id,
            name=self.name,
            exchange=Exchange(self.exchange_id),
            key_id=self.key_id,
            balance=self.balance,
            currency=self.currency,
            user_id=self.user_id,
            created_at=self.created_at,
        )

class UserEntity(Base):
    __tablename__ = "users"
    id = Column("id", String, primary_key=True)
    email = Column("email", String, unique=True)
    password = Column("password", String)
    first_name = Column("first_name", String)
    last_name = Column("last_name", String)
    birthday = Column("birthday", DateTime)
    created_at =Column("created_at", DateTime)
    expiration_date =Column("expiration_date", DateTime)
    subscription_plan = Column("subscription_plan", String)
    is_actif = Column("is_actif",Boolean)

    def __init__(self, id=None, email=None, password=None, first_name=None, last_name=None, birthday=None,  created_at=None, expiration_date=None,subscription_plan=None, is_actif=None):
        self.id = id
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.created_at = created_at
        self.expiration_date = expiration_date
        self.subscription_plan=subscription_plan
        self.is_actif = is_actif

        
    def __repr__(self):
        return "<UserEntity(id='%s', first_name='%s', last_name='%s')>" % (
            self.id,
            self.first_name,
            self.last_name
        )
        
    def from_domain(self, model: User):
        self.id = model.id
        self.email = model.email
        self.password = model.password
        self.first_name = model.first_name
        self.last_name = model.last_name
        self.birthday = model.birthday
        self.created_at = model.created_at
        self.expiration_date = model.expiration_date
        self.subscription_plan = model.subscription_plan
        self.is_actif = model.is_actif
        

    def to_domain(self):
        return User(
            id=self.id,
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
            birthday=self.birthday,
            created_at=self.created_at,
            expiration_date = self.expiration_date,
            subscription_plan = self.subscription_plan,
            is_actif=self.is_actif
        )




class StrategyEntity(Base):
    __tablename__ = "strategies"

    id = Column(String, primary_key=True)
    account_id = Column(String)
    name = Column(String)
    webhook_id = Column(String, unique=True)  # Make webhook_id unique
    webhook_key = Column(String)
    symbol = Column(String)
    symbol_id = Column(String)
    is_future = Column(Boolean)
    leverage = Column(Float)
    entry_size = Column(Float)
    is_percentage = Column(Boolean)
    capital = Column(Float)
    created_at = Column(DateTime)

    # Define a unique constraint for webhook_id
    __table_args__ = (UniqueConstraint('webhook_id'),)


    def __init__(self, id=None, account_id=None, name=None, webhook_id=None, webhook_key=None, symbol=None, symbol_id=None,
                 is_future=None, leverage=None, entry_size=None, is_percentage=None, capital=None , created_at=None):
        self.id = id
        self.account_id = account_id
        self.name = name
        self.webhook_id = webhook_id
        self.webhook_key = webhook_key
        self.symbol = symbol
        self.symbol_id = symbol_id
        self.is_future = is_future
        self.leverage = leverage
        self.entry_size = entry_size
        self.is_percentage = is_percentage
        self.capital = capital
        self.created_at = created_at

    def __repr__(self):
        return "<StrategyEntity(id='%s', name='%s')>" % (
            self.id,
            self.name
        ) 
    
    def from_domain(self, model: Strategy):
        self.id = model.id
        self.account_id = model.account_id
        self.name = model.name
        self.webhook_id = model.webhook_id
        self.webhook_key = model.webhook_key
        self.symbol = model.symbol
        self.symbol_id = model.symbol_id
        self.is_future = model.is_future
        self.leverage = model.leverage
        self.entry_size = model.entry_size
        self.is_percentage = model.is_percentage
        self.capital = model.capital
        self.created_at = model.created_at


    def to_domain(self):
        return Strategy(
            id= self.id,
            account_id= self.account_id,
            name= self.name,
            webhook_id= self.webhook_id,
            webhook_key= self.webhook_key,
            symbol= self.symbol,
            symbol_id= self.symbol_id,
            is_future= self.is_future,
            leverage=self.leverage,
            entry_size= self.entry_size,
            is_percentage=self.is_percentage,
            capital=self.capital,
            created_at=self.created_at
        )
        
class OrderEntity(Base):
    __tablename__ = "orders"
    
    id = Column(String, primary_key=True)
    strategy_id = Column(String)
    subscription_id = Column(String)
    is_buy = Column(Boolean)
    is_future = Column(Boolean)
    is_limit = Column(Boolean)
    limit_price = Column(Float)
    symbol = Column(String)
    symbol_id = Column(String)
    amount = Column(Float)
    status = Column(String)
    reception_date = Column(DateTime)
    execution_id = Column(String)
    execution_price = Column(Float)
    execution_date= Column(DateTime)
    response = Column(String)

    def __init__(self, id=None, strategy_id=None,subscription_id=None, is_buy=None, is_future=None,
                 is_limit=None, limit_price=None, symbol=None, symbol_id=None,
                 amount=None, status=None, reception_date=None, execution_id=None,
                 execution_price=None, execution_date=None, response=None):
        self.id = id
        self.strategy_id = strategy_id
        self.subscription_id = subscription_id
        self.is_buy = is_buy
        self.is_future = is_future
        self.is_limit = is_limit
        self.limit_price = limit_price
        self.symbol = symbol
        self.symbol_id = symbol_id
        self.amount = amount
        self.status = status
        self.reception_date = reception_date
        self.execution_id = execution_id
        self.execution_price = execution_price
        self.execution_date = execution_date
        self.response = response

    def __repr__(self):
        return "<OrderEntity(id='%s', is_buy='%s' , symbol='%s' , symbol_id='%s')>" % (
            self.id,
            self.is_buy,
            self.symbol,
            self.symbol_id
        )   


    def from_domain(self, model: Order):
        self.id = model.id
        self.strategy_id = model.strategy_id
        self.subscription_id = model.subscription_id
        self.is_buy = model.is_buy
        self.is_future = model.is_future
        self.is_limit = model.is_limit
        self.limit_price = model.limit_price
        self.symbol = model.symbol
        self.symbol_id = model.symbol_id
        self.amount = model.amount
        self.status = model.status
        self.reception_date = model.reception_date
        self.execution_id = model.execution_id
        self.execution_price = model.execution_price
        self.execution_date = model.execution_date
        self.response = model.response

    def to_domain(self):
        return Order(
            id=self.id,
            strategy_id=self.strategy_id,
            subscription_id = self.subscription_id,
            is_buy=self.is_buy,
            is_future=self.is_future,
            is_limit=self.is_limit,
            limit_price=self.limit_price,
            symbol=self.symbol,
            symbol_id=self.symbol_id,
            amount=self.amount,
            status=self.status,
            reception_date=self.reception_date,
            execution_id = self.execution_id,
            execution_price = self.execution_price,
            execution_date=self.execution_date,
            response=self.response
        )

class ExchangeEntity(Base):
    __tablename__ = "exchanges"
    id = Column("id", String, primary_key=True)
    name = Column("name", String)
    image = Column("image", String)

    def __init__(self, id=None, name=None , image=None):
        self.id = id
        self.name = name
        self.image = image

    def __repr__(self):
        return "<ExchangeEntity(id='%s', name='%s')>" % (
            self.id,
            self.name
        )

    def from_domain(self, model: Exchange):
        self.id = model.id
        self.name = model.name
        self.image = model.image

    def to_domain(self):
        return Exchange(
            id=self.id,
            name=self.name,
            image= self.image
        )




class AdminEntity(Base):
    __tablename__ = "admins"
    id = Column("id", String, primary_key=True)
    login = Column("login", String, unique=True)
    password = Column("password", String)
    first_name = Column("first_name", String)
    last_name = Column("last_name", String)
    privilege = Column("privilege", String)  # genin - chunin - jonin - anbu - kage
    

    def __init__(self, id=None, login=None, password=None, first_name=None, last_name=None, privilege=None):
        self.id = id
        self.login = login
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.privilege = privilege
        
    def __repr__(self):
        return "<AdminEntity(id='%s', first_name='%s', last_name='%s')>" % (
            self.id,
            self.first_name,
            self.last_name
        )
        
    def from_domain(self, model: Admin):
        self.id = model.id
        self.login = model.login
        self.password = model.password
        self.first_name = model.first_name
        self.last_name = model.last_name
        self.privilege = model.privilege
        

    def to_domain(self):
        return Admin(
            id=self.id,
            login=self.login,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
            privilege=self.privilege
        )


   
   
class PublicStrategyEntity(Base):
    __tablename__ = "public_strategies"

    id = Column(String, primary_key=True)
    name = Column(String)
    webhook_id = Column(String, unique=True)  # Make webhook_id unique
    webhook_key = Column(String)
    symbol = Column(String)
    symbol_id = Column(String)
    is_future = Column(Boolean)
    leverage = Column(Float)
    capital = Column(Float)
    created_at = Column(DateTime)
    backtesting_start_date = Column(DateTime)
    backtesting_end_date = Column(DateTime)
    backtesting_initial_capital = Column(Float)
    net_profit = Column(Float)
    total_closed_trades = Column(Float)
    percentage_profitable = Column(Float)
    max_drawdown = Column(Float)

    def __init__(self, id=None, name=None, webhook_id=None, webhook_key=None, symbol=None, symbol_id=None,
                 is_future=None, leverage=None, capital=None, created_at=None, backtesting_start_date=None,
                 backtesting_end_date=None, backtesting_initial_capital=None, net_profit=None,
                 total_closed_trades=None, percentage_profitable=None, max_drawdown=None):
        self.id = id
        self.name = name
        self.webhook_id = webhook_id
        self.webhook_key = webhook_key
        self.symbol = symbol
        self.symbol_id = symbol_id
        self.is_future = is_future
        self.leverage = leverage
        self.capital = capital
        self.created_at = created_at
        self.backtesting_start_date = backtesting_start_date
        self.backtesting_end_date = backtesting_end_date
        self.backtesting_initial_capital = backtesting_initial_capital
        self.net_profit = net_profit
        self.total_closed_trades = total_closed_trades
        self.percentage_profitable = percentage_profitable
        self.max_drawdown = max_drawdown

    def __repr__(self):
        return "<PublicStrategyEntity(id='%s', name='%s')>" % (
            self.id,
            self.name
        )

    def from_domain(self, model: PublicStrategy):
        self.id = model.id
        self.name = model.name
        self.webhook_id = model.webhook_id
        self.webhook_key = model.webhook_key
        self.symbol = model.symbol
        self.symbol_id = model.symbol_id
        self.is_future = model.is_future
        self.leverage = model.leverage
        self.capital = model.capital
        self.created_at = model.created_at
        self.backtesting_start_date = model.backtesting_start_date
        self.backtesting_end_date = model.backtesting_end_date
        self.backtesting_initial_capital = model.backtesting_initial_capital
        self.net_profit = model.net_profit
        self.total_closed_trades = model.total_closed_trades
        self.percentage_profitable = model.percentage_profitable
        self.max_drawdown = model.max_drawdown

    def to_domain(self):
        return PublicStrategy(
            id=self.id,
            name=self.name,
            webhook_id=self.webhook_id,
            webhook_key=self.webhook_key,
            symbol=self.symbol,
            symbol_id=self.symbol_id,
            is_future=self.is_future,
            leverage=self.leverage,
            capital=self.capital,
            created_at=self.created_at,
            backtesting_start_date=self.backtesting_start_date,
            backtesting_end_date=self.backtesting_end_date,
            backtesting_initial_capital=self.backtesting_initial_capital,
            net_profit=self.net_profit,
            total_closed_trades=self.total_closed_trades,
            percentage_profitable=self.percentage_profitable,
            max_drawdown=self.max_drawdown
        )


class SubscriptionEntity(Base):
    __tablename__ = "subscriptions"
 
    id = Column(String, primary_key=True)
    user_id = Column(String)
    strategy_id = Column(String)
    account_id = Column(String)
    created_at = Column(DateTime)
    unsubscription_date = Column(DateTime)

    def __init__(self, id=None, user_id=None, strategy_id=None, account_id=None , created_at=None , unsubscription_date=None):
        self.id = id
        self.user_id = user_id
        self.strategy_id = strategy_id
        self.account_id = account_id
        self.created_at = created_at
        self.unsubscription_date = unsubscription_date

    def __repr__(self):
        return "<SubscriptionEntity(id='%s', user_id='%s', strategy_id='%s')>" % (
            self.id,
            self.user_id,
            self.strategy_id
        )

    def from_domain(self, model: Subscription):
        self.id = model.id
        self.user_id = model.user_id
        self.strategy_id = model.strategy_id
        self.account_id  = model.account_id
        self.created_at = model.created_at
        self.unsubscription_date = model.unsubscription_date

    def to_domain(self):
        return Subscription(
            id=self.id,
            user_id=self.user_id,
            strategy_id=self.strategy_id,
            account_id = self.account_id,
            created_at=self.created_at,
            unsubscription_date = self.unsubscription_date
        )