from dataclasses import dataclass
from models.model import Subscription


@dataclass
class UnsubscribeToPublicStrategyForm:
    
    strategy_id: str = None

    def __init__(self, json_data):
        self.validate_fields(json_data)

        self.strategy_id = json_data.get('webhook_id')

    def validate_fields(self, json_data):
        required_fields = [
             'webhook_id'
        ]
        missing_fields = [field for field in required_fields if field not in json_data]

        if missing_fields:
            raise Exception(f"Missing required fields: {', '.join(missing_fields)}")

    def to_domain(self):
        return Subscription(
            strategy_id=self.strategy_id
        )
