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
    exchange: Exchange = None
    key_id: str = None
    key: object = None
    user_id: str = None
    strategies: List[Strategy] = field(default_factory=list)

    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        return asdict(self)

@dataclass
class User:
    id: str = None
    login: str = None
    password: str = None
    first_name: str = None
    last_name: str = None
    birthday: datetime = None
    accounts: List[Account] = field(default_factory=list)

    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        self.birthday = self.birthday.isoformat()
        self.password = None
        return asdict(self)
