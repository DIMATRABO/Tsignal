from dataclasses import dataclass, field, asdict
from typing import List
from models.model import PublicStrategy


@dataclass
class PublicStrategiesPaginated:
    total_records: int
    page_number: int
    page_size: int
    strategies: List[PublicStrategy] = field(default_factory=list)

    def to_dict(self):
        self.strategies = [strategy.to_dict() for strategy in self.strategies]
        return asdict(self)