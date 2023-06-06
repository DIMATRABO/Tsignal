from dataclasses import dataclass, asdict
from datetime import datetime
from models.model import Strategy

@dataclass
class StrategyResponseForm:
    id: str = None
    account_name: str = None
    name: str = None
    webhook_id: str = None
    webhook_key: str = None
    symbol: str = None
    symbol_id: str = None
    is_future: bool = None
    leverage: float = None
    entry_size: float = None
    is_percentage: bool = None
    capital: float = None
    creation_date: datetime = None

    invested_7_days : float = None
    income_7_days: float = None
    invested_7_days_percent : float = None
    income_7_days_percent: float = None

    nb_orders_7days: int = None

    def __init__(self, strategy: Strategy):
        self.id=strategy.id                                     
        self.name=strategy.name                                     
        self.webhook_id=strategy.webhook_id                               
        self.webhook_key=strategy.webhook_key                            
        self.symbol=strategy.symbol                            
        self.symbol_id=strategy.symbol_id                   
        self.is_future=strategy.is_future
        self.leverage=strategy.leverage             
        self.entry_size=strategy.entry_size                  
        self.is_percentage=strategy.is_percentage
        self.capital=strategy.capital     
        self.creation_date = strategy.created_at 

       

    @classmethod
    def from_dict(self, d):
        return self(**d)
     
 
    def to_dict(self):
        self.creation_date = self.creation_date.isoformat() if self.creation_date else None
        return asdict(self)
