# Test accounts endpoints with pytest and flask
import pytest
from mongoengine import *
import os
import json
from server import create_app
from models import Account, Transaction
from datetime import datetime
import pandas as pd


@pytest.fixture
def client():
    # Set the Testing configuration prior to creating the Flask application
    os.environ["FLASK_ENV"] = "Testing"
    flask_app = create_app()
    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as client:
        yield client


# Clear db before each test
@pytest.fixture(autouse=True)
def clear_db():
    connect(host=os.getenv("MONGO_URI_TEST"))
    Account.drop_collection()
    Transaction.drop_collection()


def test_get_accounts_empty(client):
    response = client.get("/accounts")
    assert response.status_code == 200
    assert response.json == []


def test_add_account(client):
    response = client.post(
        "/account",
        json={
            "name": "Test Account",
            "transaction_headers": ["None", "None", "None", "None", "None"],
            "balance": 0,
        },
    )
    assert response.status_code == 200
    assert response.json == {
        "name": "Test Account",
        "transaction_headers": ["None", "None", "None", "None", "None"],
        "_id": str(Account.objects.first().id),
        "balance": 0,
    }


def test_get_accounts(client):
    client.post(
        "/account",
        json={
            "name": "Test Account",
            "transaction_headers": ["None", "None", "None", "None", "None"],
            "balance": 0,
        },
    )
    response = client.get("/accounts")
    assert response.status_code == 200
    assert response.json == [
        {
            "name": "Test Account",
            "transaction_headers": ["None", "None", "None", "None", "None"],
            "_id": str(Account.objects.first().id),
            "balance": 0,
        }
    ]


def test_add_transactions(client):
    client.post(
        "/account",
        json={
            "name": "Test Account",
            "transaction_headers": [
                "Date",
                "Description",
                "Amount",
                "Category",
                "Notes",
            ],
            "balance": 0,
        },
    )
    response = client.post(
        "/transactions",
        json={
            "transactions": [
                {
                    "date": "2021-01-01 00:00:00",
                    "description": "Test Transaction",
                    "amount_c": 10000,
                    "category": "Test Category",
                    "account": "Test Account",
                    "notes": "Test Notes",
                }
            ],
        },
    )
    assert response.status_code == 200
    assert response.json == [
        {
            "date": "2021-01-01 00:00:00",
            "description": "Test Transaction",
            "amount_c": 10000,
            "category": "Test Category",
            "account": "Test Account",
            "notes": "Test Notes",
            "_id": str(Transaction.objects.first().id),
        }
    ]
