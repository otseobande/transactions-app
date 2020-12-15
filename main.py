from fastapi import FastAPI, Response, status
from datetime import datetime, timedelta, timezone
import pytz

from models import Transaction, transactions

app = FastAPI(
    title="Transaction App",
    description="An application to manage transactions and get transaction insights"
)

utc=pytz.UTC

@app.get("/")
def home():
    return {
        "message": "Welcome to the Transactions app"
    }

@app.post("/transactions", status_code=status.HTTP_201_CREATED)
def create_transaction(transaction: Transaction, response: Response):
    a_min_ago = datetime.utcnow() - timedelta(seconds=60)

    if transaction.timestamp <= utc.localize(a_min_ago):
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    transactions.append(transaction)

    return transaction


@app.get("/statistics")
def get_stats():
    a_min_ago = datetime.utcnow() - timedelta(seconds=60)
    transaction_amounts = []

    for transaction in transactions:
        if transaction.timestamp >= utc.localize(a_min_ago):
            transaction_amounts.append(transaction.amount)

    num_of_transactions = len(transaction_amounts)
    transactions_sum = sum(transaction_amounts)

    try:
        transactions_avg = transactions_sum / num_of_transactions
    except ZeroDivisionError:
        transactions_avg = 0

    try:
        max_transaction_amount = max(transaction_amounts)
    except ValueError:
        max_transaction_amount = 0

    try:
        min_transaction_amount = min(transaction_amounts)
    except ValueError:
        min_transaction_amount = 0

    return {
       "sum": round(transactions_sum, 2),
       "avg": round(transactions_avg, 2),
       "max": max_transaction_amount,
       "min": min_transaction_amount,
       "count": num_of_transactions
    }

@app.delete('/transactions', status_code=status.HTTP_204_NO_CONTENT)
def delete_transactions():
    transactions.clear()
