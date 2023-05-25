from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List
from datetime import datetime


@dataclass
class Exchange:
    id: str = None
    name: str = None

    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        return asdict(self)


@dataclass
class Order:
    id: str = None
    strategy_id:str = None
    is_buy: bool = None
    is_future: bool = None
    is_limit: bool = None
    limit_price: float = None
    symbol_base: str = None
    symbol_quote: str = None
    amount: float = None
    status: str = None
    reception_date: datetime = None 
    execution_date: datetime = None
    response: str = None    
    

    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        self.reception_date = self.reception_date.isoformat() if self.reception_date else None
        self.execution_date = self.execution_date.isoformat() if self.execution_date else None
        return asdict(self)



@dataclass
class Strategy:
    id: str = None
    account_id: str = None
    name: str = None
    webhook_id: str = None
    webhook_key: str = None
    symbol_base: str = None
    symbol_quote: str = None
    is_future: bool = None
    leverage: float = None
    entry_size: float = None
    is_percentage: bool = None
    capital: float = None
    orders: List[Order] = field(default_factory=list)

    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        return asdict(self)


@dataclass
class Account:
    id: str = None
    name: str = None
    exchange: Exchange = None
    key_id: str = None
    key: object = None
    balance :float = None
    currency: float = None
    user_id: str = None
    strategies: List[Strategy] = field(default_factory=list)
    created_at: datetime = None

    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        self.key = None
        self.key_id = None
        self.created_at = self.created_at.isoformat() if self.created_at else None
        return asdict(self)

@dataclass
class User:
    id: str = None
    client_id: str = None
    email: str = None
    password: str = None
    first_name: str = None
    last_name: str = None
    birthday: datetime = None
    created_at: datetime = None
    expiration_date: datetime = None
    subscription_plan : str = None
    is_actif: bool = None
    accounts: List[Account] = field(default_factory=list)

    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        self.birthday = self.birthday.isoformat() if self.birthday else None
        self.created_at = self.created_at.isoformat() if self.created_at else None
        self.expiration_date = self.expiration_date.isoformat() if self.expiration_date else None
        self.password = None
        return asdict(self)


@dataclass
class Admin:
    id: str = None
    login: str = None
    password: str = None
    first_name: str = None
    last_name: str = None
    privilege: str = None 
  
    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        self.password = None
        return asdict(self)
