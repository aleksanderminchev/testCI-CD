import hashlib
import enum
from sqlalchemy.orm import Session

from api.app import db
from api.utils.utils import get_date, Updateable
from models.teacher import Teacher


class CourseStatus(enum.Enum):
    """ To add this type in migration add:
        from sqlalchemy.dialects import postgresql
        banner_status = postgresql.ENUM('Pending', 'Taken','Cancelled', name='coursestatus')
        banner_status.create(op.get_bind())
    """
    PENDING = "Pending"
    TAKEN = "Taken"
    CANCELLED = "Cancelled"


class Course(Updateable, db.Model):  # type:ignore

    __tablename__ = "Tutor course"

    uid = db.Column(db.Integer, primary_key=True)
    hashed_id = db.Column(db.String(256), nullable=True, index=True)
    crm_deal_id = db.Column(db.BigInteger, nullable=True, index=True)
    tw_customer_id = db.Column(db.Integer, nullable=True, index=True)
    tw_student_id = db.Column(db.Integer, nullable=True, index=True)
    created_at = db.Column(db.DateTime, default=get_date)
    last_updated = db.Column(
        db.DateTime, default=get_date, onupdate=get_date)
    subjects = db.Column(db.String(256), nullable=False)
    math_programs = db.Column(db.String(256), nullable=True)
    class_grade = db.Column(db.String(80), nullable=True)
    education = db.Column(db.String(256), nullable=True)
    course_type = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    hidden = db.Column(db.Boolean, default=False)
    hours_per_session = db.Column(db.Integer, nullable=False)
    weekly_frequency = db.Column(db.Integer, nullable=True)
    comment = db.Column(db.Text, nullable=True)
    estimated_length = db.Column(db.String(256), nullable=False)
    unavailable_days = db.Column(db.String(256), nullable=True)
    status = db.Column(
        db.Enum(
            CourseStatus,
            values_callable=lambda obj: [e.value for e in obj]
        ),
        nullable=False,
        default=CourseStatus.PENDING.value,
        server_default=CourseStatus.PENDING.value,
        index=True
    )  # Can either be Pending or Taken.

    taken_by = db.Column(
        db.Integer, db.ForeignKey("teacher.id"), index=True)
        
    @staticmethod
    def add(data):
        if "taken_by" in data:
            # Get the TW ID and remove it from the data.
            teacher_id = data.pop("taken_by")

            # Create the course
            course = Course(**data)

            course.taken_by = teacher_id
        else:
            course = Course(**data)

        db.session.add(course)
        db.session.commit()

        uid_hash = str(course.uid) + str(course.crm_deal_id)
        uid_hash = uid_hash.encode('utf-8')
        course.hashed_id = hashlib.sha224(uid_hash).hexdigest()

        db.session.commit()

        return course

    @staticmethod
    def change_status(id, status):
        course = Course.query.filter_by(uid=id).first()
        course.status = status
        db.session.commit()

    @staticmethod
    def update_tw_id(uid: int, tw_customer_id: int, tw_student_id: int):
        course = Course.query.filter_by(uid=uid).first()
        course.tw_customer_id = tw_customer_id
        course.tw_student_id = tw_student_id
        db.session.commit()

    @staticmethod
    def in_db(hashed_id):
        course = db.session.query(Course).filter_by(
            hashed_id=hashed_id).first()
        if bool(course):
            return course
        return "No tutor found with the specified paramaters."

    def to_dict(self):
        # Exports Course data from db to a dictionary
        return {"id": self.uid, "hashed_id": self.hashed_id, "crm_deal_id": self.crm_deal_id, "tw_customer_id": self.tw_customer_id, "tw_student_id": self.tw_student_id, "created_at": self.created_at, "last_updated": self.last_updated, "subjects": self.subjects, "math_programs": self.math_programs, "class_grade": self.class_grade, "education": self.education, "course_type": self.course_type, "name": self.name, "hidden": self.hidden, "hours_per_session": self.hours_per_session, "weekly_frequency": self.weekly_frequency, "comment": self.comment, "estimated_length": self.estimated_length, "unavailable_days": self.unavailable_days, "status": self.status, "taken_by": self.taken_by}

    def assign_teacher_to_course(self, tutor_id):
        self.taken_by = tutor_id
        db.session.commit()
