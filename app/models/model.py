
from dataclasses import dataclass
from datetime import datetime
from typing import List
from datetime import datetime


@dataclass
class Exchange:
    id: str = None
    name: str = None

    @classmethod
    def from_dict(cls, d):
        return cls(
            id=d.get('id'),
            name=d.get('name')
        )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

@dataclass
class Order:
    id: str = None
    account_id: str = None
    is_buy: bool = None
    is_future: bool = None
    is_limit: bool = None
    limit_price: float = None
    symbol: str = None
    amount: float = None

    @classmethod
    def from_dict(cls, d):
        return cls(
            id=d.get('id'),
            account_id=d.get('account_id'),
            is_buy=d.get('is_buy'),
            is_future=d.get('is_future'),
            is_limit=d.get('is_limit'),
            limit_price=d.get('limit_price'),
            symbol=d.get('symbol'),
            amount=d.get('amount')
        )

    def to_dict(self):
        return {
            'id': self.id,
            'account_id': self.account_id,
            'is_buy': self.is_buy,
            'is_future': self.is_future,
            'is_limit': self.is_limit,
            'limit_price': self.limit_price,
            'symbol': self.symbol,
            'amount': self.amount
        }

@dataclass
class Account:
    id: str = None
    exchange: Exchange = None
    key_id: str = None
    key: object = None
    user_id: str = None
    orders: List[Order] = None

    @classmethod
    def from_dict(cls, d):
        exchange = Exchange.from_dict(d.get('exchange', {}))
        orders = [Order.from_dict(ordr) for ordr in d.get('orders', [])]
        return cls(
            id=d.get('id'),
            exchange=exchange,
            key_id=d.get('key_id'),
            key=d.get('key'),
            orders=orders
        )

    def to_dict(self):
        exchange = self.exchange.to_dict() if self.exchange else None
        orders = [ordr.to_dict() for ordr in self.orders] if self.orders else []
        return {
            'id': self.id,
            'exchange': exchange,
            'api_key': self.api_key,
            'api_secret': self.api_secret,
            'orders': orders
        }
    


@dataclass
class User:
    id: str = None
    login: str = None
    password: str = None
    first_name: str = None
    last_name: str = None
    birthday: datetime = None
    accounts: List[Account] = None

    @classmethod
    def from_dict(cls, d):
        #accounts = [Account.from_dict(acc) for acc in d.get('accounts', [])]
        return cls(
            id=d.get('id'),
            login=d.get('login'),
            password=d.get('password'),
            first_name=d.get('first_name'),
            last_name=d.get('last_name'),
            birthday=datetime.fromisoformat(d.get('birthday')) if d.get('birthday') else None,
            accounts=d.get('accounts')
        )

    def to_dict(self):
        self.password = None
        self.birthday = self.birthday.isoformat() if self.birthday else None
        accounts = [acc.to_dict() for acc in self.accounts] if self.accounts else []
        return {
            'id': self.id,
            'login': self.login,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birthday': self.birthday,
            'accounts': accounts
        }