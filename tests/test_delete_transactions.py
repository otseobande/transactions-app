from fastapi import FastAPI
from fastapi.testclient import TestClient
from datetime import datetime
import json

from main import app
from models import transactions, Transaction

client = TestClient(app)

def test_delete_transactions():
    for i in range(10):
        transactions.append(
            Transaction(
                amount=100,
                timestamp="2018-07-17T09:59:51.312Z"
            )
        )

    response = client.delete("/transactions")

    assert response.status_code == 204
    assert len(transactions) == 0





