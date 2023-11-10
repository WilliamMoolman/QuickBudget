from mongoengine import *
import pandas as pd


class Transaction(Document):
    date = DateTimeField()
    description = StringField()
    amount_c = IntField()
    account = StringField()
    category = StringField()
    notes = StringField()

    def as_dict(self):
        return self.to_mongo().to_dict()


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

    def as_dict(self):
        return self.to_mongo().to_dict()
