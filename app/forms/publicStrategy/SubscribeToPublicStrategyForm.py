from dataclasses import dataclass
from models.model import Subscription


@dataclass
class SubscribeToPublicStrategyForm:
    
    strategy_id: str = None
    account_id: str = None
    amount: float = None
    capital: float = None


    def __init__(self, json_data):
        self.validate_fields(json_data)

        self.strategy_id = json_data.get('webhook_id')
        self.account_id = json_data.get('account_id')
        self.amount = json_data.get('amount')
        self.capital = json_data.get('capital')


    def validate_fields(self, json_data):
        required_fields = [
             'webhook_id', 'account_id' , 'amount', 'capital'
        ]
        missing_fields = [field for field in required_fields if field not in json_data]

        if missing_fields:
            raise Exception(f"Missing required fields: {', '.join(missing_fields)}")

    def to_domain(self):
        return Subscription(
            strategy_id=self.strategy_id,
            account_id=self.account_id,
            amount=self.amount,
            capital=self.capital
        )
