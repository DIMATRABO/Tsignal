from dataclasses import dataclass, asdict, field
from typing import List, Tuple


@dataclass
class UserStrategyResponse:
   
    total_orders: int = None

    total_sell_orders : int = None
    total_buy_orders: int = None

    average_sell_price: float = None 
    average_buy_price: float = None

    total_sell_quantitiy: float = None
    total_buy_quantity: float = None

    total_failed_orders : int = None

    monthly_profit: List[float] = field(default_factory=list)
 
    orders_by_trading_pair: List[Tuple[str, int]] = field(default_factory=list)


    @classmethod
    def from_dict(self, d):
        return self(**d)
    
    def to_dict(self):
        self.average_sell_price = round(self.average_sell_price , 4) 
        self.average_buy_price = round(self.average_buy_price , 4) 
        self.total_sell_quantitiy = round(self.total_sell_quantitiy , 4) 
        self.total_buy_quantity = round(self.total_buy_quantity , 4) 
        return asdict(self)
