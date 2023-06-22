from dataclasses import dataclass
from models.model import Subscription


@dataclass
class SubscribeToPublicStrategyForm:
    user_id: str =None
    strategy_id: str = None
    account_id: str = None


    def __init__(self, json_data):
        self.validate_fields(json_data)

        self.user_id = json_data.get('user_id')
        self.strategy_id = json_data.get('strategy_id')
        self.account_id = json_data.get('account_id')

    def validate_fields(self, json_data):
        required_fields = [
            'user_id', 'strategy_id', 'account_id'
        ]
        missing_fields = [field for field in required_fields if field not in json_data]

        if missing_fields:
            raise Exception(f"Missing required fields: {', '.join(missing_fields)}")

    def to_domain(self):
        return Subscription(
            user_id=self.user_id,
            strategy_id=self.strategy_id,
            account_id=self.account_id
        )
