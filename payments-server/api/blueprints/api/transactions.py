from api.schema.transactions import UpdateTransactionSchema, TransactionSchema, CreateTransactionSchema
from apifairy.decorators import other_responses
from flask import Blueprint, abort
from apifairy import authenticate, body, response

from models.transaction import Transaction
from api.auth import token_auth, admin_auth, limit_user_to_own_routes_decorator
from api.decorators import paginated_response
from api.utils.stripe_utils import requestRefund
transactions = Blueprint('transactions', __name__)
transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)


@transactions.route('/transactions', methods=['POST'])
@authenticate(admin_auth)
@body(CreateTransactionSchema())
@response(transaction_schema, 201)
def new(args):
    """Creates a new transaction and adds it to the the customers account"""
    transaction = Transaction.add_new_transaction(**args)
    return transaction.to_dict()


@transactions.route('/transaction/<int:id>', methods=['DELETE'])
@authenticate(admin_auth)
@response(transaction_schema)
@other_responses({404: 'transaction not found'})
def delete_transaction(id):
    """Delete a transaction by id"""
    transaction = Transaction.delete_transaction(id) or abort(404)
    return transaction


@transactions.route('/transaction', methods=['GET'])
@authenticate(token_auth)
@limit_user_to_own_routes_decorator
@paginated_response(schema=transactions_schema)
def all():
    """Retrieve all transactions"""
    return Transaction.query


@transactions.route('/transactions_customer/<int:id>', methods=['GET'])
@authenticate(token_auth)
@limit_user_to_own_routes_decorator
@paginated_response(schema=transactions_schema)
def all_customer_transactions(id):
    """Retrieve all customer transactions"""
    return Transaction.query.filter_by(customer_id=id)


@transactions.route('/transaction/<int:id>', methods=['GET'])
@authenticate(token_auth)
@limit_user_to_own_routes_decorator
@response(transaction_schema)
@other_responses({404: 'transaction not found'})
def get(id):
    """Retrieve a transaction by id"""
    transaction = Transaction.get_transaction_by_id(id) or abort(404)
    return transaction.to_dict()


@transactions.route('/update_transactions', methods=['PUT'])
@authenticate(admin_auth)
@response(UpdateTransactionSchema(), 201)
@body(UpdateTransactionSchema())
def put_transaction(data):
    """Edit transactions information
     Fields given get updated all other ones don't"""
    return Transaction.update_transaction(**data).to_dict()


@transactions.route('/refundTransaction/<int:id>', methods=['GET'])
@authenticate(admin_auth)
@response(transaction_schema)
@other_responses({404: 'transaction not found'})
def refund(id):
    """Refund a transaction by id"""
    transaction = Transaction.get_transaction_by_id(id) or abort(404)
    requestRefund(transaction.stripe_transaction_id)
    return transaction.to_dict()
