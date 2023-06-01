
from dataclasses import dataclass, asdict

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
    
    total_invisted: float = None
    total_income: float = None


    monthly_profit : dict = None



    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        return asdict(self)
