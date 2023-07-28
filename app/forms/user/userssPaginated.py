from dataclasses import dataclass, field, asdict
from typing import List
from models.model import User


@dataclass
class UsersPage:
    total_records: int
    page_number: int
    page_size: int
    users: List[User] = field(default_factory=list)

    def to_dict(self):
        self.users = [user.to_dict() for user in self.users]
        return asdict(self)