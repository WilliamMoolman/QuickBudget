from flask import Flask, request, jsonify
import logging
import os

from backend import Database, Account, Transaction

from bson import json_util
import json


def jsonify_mongo(data):
    return jsonify(json.loads(json.dumps(data, default=str)))


def create_app():
    app = Flask("qb")
    app.logger.setLevel(logging.DEBUG)
    if os.getenv("FLASK_ENV") == "Testing":
        app.config["TESTING"] = True

    if app.config["TESTING"]:
        app.logger.info("Testing mode")
        app.config["MONGO_URI"] = os.getenv("MONGO_URI_TEST")
    else:
        app.logger.info("Production mode")
        app.config["MONGO_URI"] = os.getenv("MONGO_URI")

    db = Database(app.config["MONGO_URI"])

    @app.route("/account", methods=["POST"])
    def add_account():
        account = Account(**request.json)
        db.add_account(account)
        return jsonify_mongo(account.as_dict())

    @app.route("/accounts", methods=["GET"])
    def get_accounts():
        accounts = db.get_accounts()
        return jsonify_mongo([account.as_dict() for account in accounts])

    @app.route("/transactions", methods=["GET"])
    def get_transactions():
        transactions = db.get_transactions()
        app.logger.info([transaction.as_dict() for transaction in transactions])
        return jsonify_mongo([transaction.as_dict() for transaction in transactions])

    @app.route("/transaction", methods=["POST"])
    def add_transaction():
        app.logger.info(request.json)
        transaction = Transaction(**request.json)
        db.add_transaction(transaction)
        return jsonify_mongo(transaction.as_dict())

    @app.route("/transactions", methods=["POST"])
    def add_transactions():
        transactions = [
            Transaction(**transaction) for transaction in request.json["transactions"]
        ]
        db.add_transactions(transactions)
        return jsonify_mongo([transaction.as_dict() for transaction in transactions])

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
