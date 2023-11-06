from mongoengine import *
import os
import pandas as pd
import logging

logger = logging.getLogger('qb.backend')



class Database:
    def __init__(self):
        connect(host=os.getenv("MONGO_URI"))
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

class Transaction(Document):
    date = DateTimeField()
    description = StringField()
    amount_c = IntField()
    account = StringField()
    category = StringField()
    notes = StringField()

    def as_dict(self):
        return {
            "date": self.date.strftime("%Y-%m-%d %H:%M:%S"),
            "description": self.description,
            "amount_c": self.amount_c,
            "account": self.account,
            "category": self.category,
            "notes": self.notes,
        }



class Account(Document):
    name = StringField()
    balance = IntField()
    transaction_headers = ListField(StringField())

    def load_transactions(self, transactions: pd.DataFrame):
        transactions_with_headers = transactions.set_axis(
            self.transaction_headers, axis=1
        )
        for transaction in transactions_with_headers.to_dict(orient="records"):
            Transaction(**transaction).save()

