from dataclasses import dataclass, field, asdict
from typing import List
from models.model import Order


@dataclass
class OrdersPage:
    total_records: int
    page_number: int
    page_size: int
    orders: List[Order] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)