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
    account_id: str = None
    is_buy: bool = None
    is_future: bool = None
    is_limit: bool = None
    limit_price: float = None
    base: str = None
    quote: str = None
    amount: float = None

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
    orders: List[Order] = field(default_factory=list)

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
