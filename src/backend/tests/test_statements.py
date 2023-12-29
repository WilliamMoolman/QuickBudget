# Test accounts endpoints with pytest and flask
import pytest
from mongoengine import *
import os
import json
from server import create_app
from models import Account, Transaction, Statement
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


def test_get_statements_empty(client):
    response = client.get("/statements")
    assert response.status_code == 200
    assert response.json == []


def test_add_statements(client):
    client.post(
        "/statement",
        json={
            "name": "Test Statement",
            "account_id": "123",
            "md5checksum": "123",
            "transactions": [],
        },
    )
    response = client.get("/statements")
    assert response.status_code == 200
    assert response.json == [
        {
            "name": "Test Statement",
            "account_id": "123",
            "md5checksum": "123",
            "transactions": [],
            "_id": str(Statement.objects.first().id),
        }
    ]
