
from dataclasses import dataclass, asdict, field
from typing import List, Tuple


@dataclass
class UserHomeResponse:
    total_orders: int = None

    total_sell_orders : int = None
    total_buy_orders: int = None

    average_sell_price: float = None 
    average_buy_price: float = None

    total_sell_quantitiy: float = None
    total_buy_quantity: float = None

    total_failed_orders : int = None

    monthly_profit: List[Tuple[int, float]] = field(default_factory=list)

    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        
        self['monthly_profit'] = [(month, float(profit)) for month, profit in self['monthly_profit']]
        data = asdict(self)
        return data
