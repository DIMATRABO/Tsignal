from dataclasses import dataclass
from models.model import PublicStrategy
from datetime import datetime

@dataclass
class CreatePublicStrategyForm:
    name: str = None
    webhook_id: str = None
    webhook_key: str = None
    symbol: str = None
    symbol_id: str = None
    is_future: bool = None
    leverage: float = None
    capital: float = None
    backtesting_start_date: datetime = None
    backtesting_end_date: datetime = None
    backtesting_initial_capital: float = None
    net_profit: float = None
    total_closed_trades: float = None
    percentage_profitable: float = None
    max_drawdown: float = None

    def __init__(self, json_data):
        self.validate_fields(json_data)

        self.name = json_data.get('name')
        self.webhook_id = json_data.get('webhook_id')
        self.webhook_key = json_data.get('webhook_key')
        self.symbol = json_data.get('symbol')
        self.symbol_id = json_data.get('symbol_id')
        self.is_future = json_data.get('is_future')
        self.leverage = json_data.get('leverage')
        self.capital = json_data.get('capital')
        self.backtesting_start_date = json_data.get('backtesting_start_date')
        self.backtesting_end_date = json_data.get('backtesting_end_date')
        self.backtesting_initial_capital = json_data.get('backtesting_initial_capital')
        self.net_profit = json_data.get('net_profit')
        self.total_closed_trades = json_data.get('total_closed_trades')
        self.percentage_profitable = json_data.get('percentage_profitable')
        self.max_drawdown = json_data.get('max_drawdown')

    def validate_fields(self, json_data):
        required_fields = [
            'name', 'webhook_id', 'webhook_key',
            'symbol', 'symbol_id', 'is_future', 'leverage',
            'capital', 'backtesting_start_date',
            'backtesting_end_date', 'backtesting_initial_capital',
            'net_profit', 'total_closed_trades', 'percentage_profitable',
            'max_drawdown'
        ]
        missing_fields = [field for field in required_fields if field not in json_data]

        if missing_fields:
            raise Exception(f"Missing required fields: {', '.join(missing_fields)}")

    def to_domain(self):
        return PublicStrategy(
            name=self.name,
            webhook_id=self.webhook_id,
            webhook_key=self.webhook_key,
            symbol=self.symbol,
            symbol_id=self.symbol_id,
            is_future=self.is_future,
            leverage=self.leverage,
            capital=self.capital,
            backtesting_start_date=self.backtesting_start_date,
            backtesting_end_date=self.backtesting_end_date,
            backtesting_initial_capital=self.backtesting_initial_capital,
            net_profit=self.net_profit,
            total_closed_trades=self.total_closed_trades,
            percentage_profitable=self.percentage_profitable,
            max_drawdown=self.max_drawdown
        )
