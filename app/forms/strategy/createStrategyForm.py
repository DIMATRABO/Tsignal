from dataclasses import dataclass
from models.model import Strategy

@dataclass
class CreateStrategyForm:
    account_id: str = None
    name: str = None
    symbol: str = None
    symbol_id: str = None
    is_future: bool = None
    leverage: float = None
    entry_size: float = None
    is_percentage: bool = None
    capital: float = None

    def __init__(self, json_data):
        self.validate_fields(json_data)

        self.account_id = json_data.get('account_id')
        self.name = json_data.get('name')
        self.symbol = json_data.get('symbol')
        self.symbol_id = json_data.get('symbol_id')
        self.is_future = json_data.get('is_future')
        self.leverage = json_data.get('leverage')
        self.entry_size = json_data.get('entry_size')
        self.is_percentage = json_data.get('is_percentage')
        self.capital = json_data.get('capital')

    def validate_fields(self, json_data):
        required_fields = [
            'account_id', 'name',
            'symbol', 'symbol_id', 'is_future', 'leverage',
            'entry_size', 'is_percentage', 'capital'
        ]
        missing_fields = [field for field in required_fields if field not in json_data]

        if missing_fields:
            raise Exception(f"Missing required fields: {', '.join(missing_fields)}")
        


    def to_domain(self):
        return Strategy(
            account_id=self.account_id,
            name=self.name,
            symbol=self.symbol,
            symbol_id=self.symbol_id,
            is_future=self.is_future,
            leverage=self.leverage,
            entry_size=self.entry_size,
            is_percentage=self.is_percentage,
            capital=self.capital
        )
