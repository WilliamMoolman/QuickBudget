from flask import Flask, request, jsonify
import logging

from backend import Database, Account, Transaction

app = Flask('qb')
app.logger.setLevel(logging.DEBUG)

db = Database()

@app.route("/accounts", methods=["GET"])
def get_accounts():
    accounts = db.get_accounts()
    return jsonify([account.__dict__ for account in accounts])


@app.route("/transactions", methods=["GET"])
def get_transactions():
    transactions = db.get_transactions()
    app.logger.info([transaction.as_dict() for transaction in transactions])
    return jsonify([transaction.as_dict() for transaction in transactions])

@app.route("/transaction", methods=["POST"])
def add_transaction():
    app.logger.info(request.json)
    transaction = Transaction(**request.json)
    db.add_transaction(transaction)
    return jsonify(transaction.__dict__)

if __name__ == "__main__":
    app.run(debug=True)
