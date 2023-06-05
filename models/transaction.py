
import enum
from api.app import db

from api.utils.utils import Updateable, get_date
from flask import abort


class TransactionType(enum.Enum):
    """ 
    To add this type in migration add:
    from sqlalchemy.dialects import postgresql
    student_status = postgresql.ENUM('refund','payment', name='transactiontype')
    student_status.create(op.get_bind())
    """
    REFUND = "refund"
    PAYMENT = "payment"


class CurrencyEnum(enum.Enum):
    """ Add this to migration file:
    from sqlalchemy.dialects import postgresql
    student_status = postgresql.ENUM('dkk', name='currencyenum')
    student_status.create(op.get_bind())
    """
    DKK = "DKK"


class MethodEnum(enum.Enum):
    """ Add this to migration file:
    from sqlalchemy.dialects import postgresql
    student_status = postgresql.ENUM('bank','stripe','other', name='methodenum')
    student_status.create(op.get_bind())
    """
    BANK = "bank"
    STRIPE = "stripe"
    OTHER = "other"


class Transaction(Updateable, db.Model):  # type:ignore
    """
    Model for transactions
    """

    __tablename__ = "transaction"
    id = db.Column(db.Integer, primary_key=True)
    type_transaction = db.Column(
        db.Enum(
            TransactionType,
            values_callable=lambda obj: [e.value for e in obj]
        ),
        nullable=False,
        default=TransactionType.PAYMENT.value,
        server_default=TransactionType.PAYMENT.value,
        index=True
    )
    customer_id = db.Column(db.Integer, db.ForeignKey(
        "customer.id"), nullable=False, index=True)
    balance_id = db.Column(db.Integer, db.ForeignKey('balance.id'), index=True)
    customer = db.relationship("Customer", backref="transactions")
    created_at = db.Column(db.DateTime, nullable=False, default=get_date)
    last_updated = db.Column(db.DateTime, nullable=False,
                             default=get_date, onupdate=get_date)
    currency = db.Column(
        db.Enum(
            CurrencyEnum,
            values_callable=lambda obj: [e.value for e in obj]
        ),
        nullable=False,
        default=CurrencyEnum.DKK.value,
        server_default=CurrencyEnum.DKK.value,
    )
    amount = db.Column(db.Float, nullable=False)
    void = db.Column(db.Boolean, nullable=False,
                     default=False, server_default='f')
    method = db.Column(
        db.Enum(
            MethodEnum,
            values_callable=lambda obj: [e.value for e in obj]
        ),
        nullable=False,
        default=MethodEnum.STRIPE.value,
        server_default=MethodEnum.STRIPE.value,
        index=True
    )
    stripe_transaction_id = db.Column(db.String, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "type_transaction": self.type_transaction.value,
            "method": self.method.value,
            "currency": self.currency.value,
            "amount": self.amount,
            "void": self.void,
            "stripe_transaction_id": self.stripe_transaction_id,
            "last_updated": self.last_updated,
            "created_at": self.created_at,
            "customer": self.customer.to_dict(),
        }

    @staticmethod
    def get_transaction_by_id(id):
        return Transaction.query.get(id)

    @staticmethod
    def update_transaction(id=int, **kwargs):
        """Updates a transaction by the User id from the DB"""
        transaction_query = Transaction.query.get(id)
        transaction_query.customer.balance[0].invoice_balance = transaction_query.customer.balance[
            0].invoice_balance - transaction_query.amount
        Transaction.update(transaction_query, kwargs)
        transaction_query.customer.balance[0].invoice_balance = transaction_query.customer.balance[0].invoice_balance + kwargs['amount']
        db.session.commit()
        return transaction_query

    @staticmethod
    def add_new_transaction(**kwargs):
        """ Adds a new transaction to the DB. TODO """
        transaction = Transaction(**kwargs)
        db.session.add(transaction)
        db.session.commit()
        return transaction

    @staticmethod
    def delete_transaction(id=str):
        """Deletes a transaction from the DB"""
        # delete student transactions
        transaction = Transaction.query.get(id) or abort(404)
        transaction_for_return = transaction.to_dict()
        db.session.delete(transaction)
        db.session.commit()
        return transaction_for_return
