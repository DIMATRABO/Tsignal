
from dataclasses import dataclass, asdict

@dataclass
class UserHomeResponse:
    total_orders: float = None


    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        return asdict(self)
