# import hashlib
# import enum
# from sqlalchemy.orm import Session

# from api.app import db
# from api.utils.utils import get_date, Updateable
# from . import relationships, tutor


# class CourseStatus(enum.Enum):
#     """ To add this type in migration add:
#         from sqlalchemy.dialects import postgresql
#         banner_status = postgresql.ENUM('Pending', 'Taken','Cancelled', name='coursestatus')
#         banner_status.create(op.get_bind())
#     """
#     PENDING = "Pending"
#     TAKEN = "Taken"
#     CANCELLED= "Cancelled"

# Juster' overstående så det passer til nedenstående


# class stoppedCustomers(Updateable, db.Model):  # type:ignore

#     __tablename__ = "Stopped Customers"
#     uid = db.Column(db.Integer, primary_key=True)
#     data = db.Column(db.String, nullable=False)
#     email = db.Column(db.String, nullable=False)
#     crm_id = db.Column(db.Integer, nullable=False)

#     customer = db.Column(db.Integer, db.ForeignKey("course.uid"))
