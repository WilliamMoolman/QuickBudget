from mongoengine import *
import pandas as pd


class Transaction(Document):
    id = StringField(primary_key=True)
    date = DateTimeField()
    # statement = ReferenceField("Statement")
    description = StringField()
    amount_c = IntField()
    account = StringField()
    category = StringField(default="Uncategorised")
    notes = StringField(default="")

    def as_dict(self):
        return self.to_mongo().to_dict()


class Account(Document):
    name = StringField()
    balance = IntField(default=0)
    transaction_headers = ListField(StringField())
    header_rows = IntField(default=0)

    def load_transactions(self, transactions: pd.DataFrame):
        transactions_with_headers = transactions.set_axis(
            self.transaction_headers, axis=1
        )
        for transaction in transactions_with_headers.to_dict(orient="records"):
            Transaction(**transaction).save()

    def as_dict(self):
        return self.to_mongo().to_dict()


class Statement(Document):
    account = ReferenceField(Account)
    checksum = StringField()
    statement = FileField()

    def as_dict(self):
        return self.to_mongo().to_dict()
