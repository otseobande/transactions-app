from typing import List
from pydantic import BaseModel
from datetime import datetime

class Transaction(BaseModel):
    amount: float
    timestamp: datetime

transactions: List[Transaction] = []
