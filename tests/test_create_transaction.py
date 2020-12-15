from fastapi import FastAPI
from fastapi.testclient import TestClient
from datetime import datetime
import json

from main import app

client = TestClient(app)

def test_create_transaction_older_than_a_min_from_now():
    response = client.post(
        "/transactions",
        data=json.dumps({
            "amount":"12.3343",
            "timestamp":"2018-07-17T09:59:51.312Z"
        })
    )
    assert response.status_code == 204


def test_create_transaction_new_than_a_min_from_now():
    timestamp = datetime.utcnow().isoformat() + 'Z'

    response = client.post(
        "/transactions",
        data=json.dumps({
            "amount":"12.3343",
            "timestamp": timestamp
        })
    )
    assert response.status_code == 201
    assert response.json() == {'amount': 12.3343, 'timestamp': timestamp.replace('Z', '+00:00')}


def test_create_transaction_bad_request():
    timestamp = datetime.utcnow().isoformat() + 'Z'

    response = client.post(
        "/transactions",
        data=json.dumps({
            "amount":"",
            "timestamp": timestamp
        })
    )
    assert response.status_code == 422
    assert response.json() == {
        'detail': [
            {
                'loc': ['body', 'amount'],
                'msg': 'value is not a valid float',
                'type': 'type_error.float'
            }
        ]
    }


