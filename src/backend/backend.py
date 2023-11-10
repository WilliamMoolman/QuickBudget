from mongoengine import *
import os
import pandas as pd
import logging
from models import Account, Transaction

logger = logging.getLogger("qb.backend")


class Database:
    def __init__(self, mongo_uri=None):
        if mongo_uri is None:
            mongo_uri = os.getenv("MONGO_URI")
        connect(host=mongo_uri)
        logger.info("Connected to database")

    def get_accounts(self):
        return Account.objects

    def get_account(self, account_id):
        return Account.objects(id=account_id).first()

    def get_transactions(self):
        return Transaction.objects

    def update_transaction(self, transaction):
        return transaction.save()

    def add_transactions(self, transactions):
        return Transaction.objects.insert(transactions)

    def add_transaction(self, transaction):
        return transaction.save()

    def add_account(self, account):
        return account.save()

    def get_accounts(self):
        return Account.objects

    def delete_account(self, account):
        return account.delete()
