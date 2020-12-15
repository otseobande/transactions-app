from fastapi import FastAPI
from fastapi.testclient import TestClient
from datetime import datetime
import json

from main import app
from models import transactions, Transaction

client = TestClient(app)

def test_get_statistics():
    transactions.append(
            Transaction(
                amount=8.9,
                timestamp=datetime.utcnow().isoformat() + '+00:00'
            )
        )
    for i in range(10):
        transactions.append(
            Transaction(
                amount=100,
                timestamp=datetime.utcnow().isoformat() + '+00:00'
            )
        )

    response = client.get("/statistics")

    assert response.status_code == 200
    assert response.json() == {
        'sum': 1008.9,
        'avg': 91.72,
        'max': 100.0,
        'min': 8.9,
        'count': 11
    }






