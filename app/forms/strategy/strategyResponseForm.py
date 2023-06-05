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

    roi_7_days : float = None
    pnl_7_days: float = None
    nb_orders_7days: int = None

    @classmethod
    def from_dict(self, d):
        return self(**d)
    

    @classmethod
    def from_strategy(self, strategy:Strategy):
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
        return self
 
 
    def to_dict(self):
        return asdict(self)
