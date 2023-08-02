from dataclasses import dataclass, asdict
from datetime import datetime
from models.model import PublicStrategy

@dataclass
class PublicStrategyResponseForm:
    id: str = None
    name: str = None
    name: str = None
    symbol: str = None
    symbol_id: str = None
    is_future: bool = None
    leverage: float = None
    capital: float = None
    created_at: datetime = None
    backtesting_start_date: datetime = None
    backtesting_end_date: datetime = None
    backtesting_initial_capital: float = None
    net_profit: float = None
    total_closed_trades: float = None
    percentage_profitable: float = None
    max_drawdown: float = None


    def __init__(self, strategy: PublicStrategy):
        self.id = strategy.id
        self.webhook_id = strategy.webhook_id #here
        self.name = strategy.name
        self.symbol = strategy.symbol
        self.symbol_id = strategy.symbol_id
        self.is_future = strategy.is_future
        self.leverage = strategy.leverage
        self.capital = strategy.capital
        self.created_at = strategy.created_at
        self.backtesting_start_date = strategy.backtesting_start_date
        self.backtesting_end_date = strategy.backtesting_end_date
        self.backtesting_initial_capital = strategy.backtesting_initial_capital
        self.net_profit = strategy.net_profit
        self.total_closed_trades = strategy.total_closed_trades
        self.percentage_profitable = strategy.percentage_profitable
        self.max_drawdown = strategy.max_drawdown

    @classmethod
    def from_dict(self, d):
        return self(**d)
     
 
    def to_dict(self):
        self.created_at = self.created_at.isoformat() if self.created_at else None
        self.backtesting_start_date = self.backtesting_start_date.isoformat() if self.backtesting_start_date else None
        self.backtesting_end_date = self.backtesting_end_date.isoformat() if self.backtesting_end_date else None
        return asdict(self)
