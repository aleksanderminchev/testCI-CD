from api.utils.utils import get_date
from api.app import db


class PhoneLead(db.Model):  # type:ignore
    """ The DB model for PhoneLeads gotten from the phone form"""

    __tablename__ = "PhoneLead"

    uid = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=get_date)
    last_updated = db.Column(
        db.DateTime, default=get_date, onupdate=get_date)

    phone = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f"{self.phone}"
