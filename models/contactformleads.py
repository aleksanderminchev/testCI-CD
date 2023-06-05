from api.utils.utils import get_date
from api.app import db


class ContactFormLead(db.Model):  # type:ignore
    """ The DB model for leads. Saved after they fill in the contact form."""

    __tablename__ = "contact_form_lead"

    uid = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=get_date)
    last_updated = db.Column(
        db.DateTime, default=get_date, onupdate=get_date)
    name = db.Column(db.String(256), nullable=False)
    started_course = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(256))
    terms_accepted = db.Column(db.Boolean)
    newsletter_accepted = db.Column(db.Boolean)
    message = db.Column(db.Text())
    zip_code = db.Column(db.Integer)
    adresse = db.Column(db.String(256))

    def exists(self, email):  # check if user email exists in db
        for lead in self.query.all():
            if lead.email == email:  # user already exists
                return True
            else:
                return False
