from api.app import db
from api.utils.utils import Updateable, get_date
from flask import abort


class Referral(Updateable, db.Model):  # type:ignore

    __tablename__ = "referral"
    id = db.Column(db.Integer, primary_key=True)
    referred_id = db.Column(
        db.Integer, db.ForeignKey('teacher.id'), index=True)
    referrer_id = db.Column(
        db.Integer, db.ForeignKey('teacher.id'), index=True)
    wage_payment_id = db.Column(
        db.Integer, db.ForeignKey('wage_payment.id'), nullable=True, index=True)
    paid = db.Column(db.Boolean, default=False,
                     server_default='f', nullable=False, index=True)
    referral_amount = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=get_date)
    last_updated = db.Column(
        db.DateTime, default=get_date, onupdate=get_date)

    def to_dict(self):
        return {
            "referred": self.referred_id,
            "referrer": self.referrer_id,
            "paid": self.paid,
            "referral_amount": self.referral_amount,
            "created_at": self.created_at,
            "last_updated": self.last_updated,
            "id": self.id
        }

    @staticmethod
    def get_referral_by_id(id):
        return Referral.query.get(id)

    @staticmethod
    def update_referral(id=int, **kwargs):
        """Updates a referral by the User id from the DB"""
        referral_query = Referral.query.get(id)
        Referral.update(referral_query, kwargs)
        db.session.commit()
        return referral_query

    @staticmethod
    def add_new_referral(**kwargs):
        """ Adds a new referral to the DB. TODO """
        referral = Referral(**kwargs)
        db.session.add(referral)
        db.session.commit()
        return referral.to_dict()

    @staticmethod
    def delete_referral(id=str):
        """Deletes a referral from the DB"""
        referral = Referral.query.get(id) or abort(404)
        db.session.delete(referral)
        db.session.commit()
        return referral
