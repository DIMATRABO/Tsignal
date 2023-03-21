
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class User:
    id: str = None
    login: str = None
    password: str = None
    first_name: str = None
    last_name: str = None
    birthday: datetime = None
    balance: float = None

    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        #self.password = None
        #self.birthday = self.birthday.isoformat() if self.birthday else None
        #return asdict(self)
        return '{"id":"'+self.id+'","login": "'+self.login+'","first_name": "'+self.first_name+'","last_name": "'+self.last_name+'","birthday": "'+ self.birthday.isoformat() + '","balance":' + self.balance +'}'
