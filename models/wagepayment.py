from api.app import db
from api.utils.utils import Updateable, get_date
from models.teacher import Teacher
from flask import abort


class WagePayment(Updateable, db.Model):  # type:ignore
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.ForeignKey('teacher.id'), index=True)
    teacher = db.relationship('Teacher', backref='wagepayments')
    referrals = db.relationship('Referral', backref='wagepayment')
    amount = db.Column(db.Float)
    referrals_amount = db.Column(db.Float, nullable=True)
    referrals_number = db.Column(db.Float, nullable=True)
    hours = db.Column(db.Float)
    payment_date = db.Column(db.DateTime, index=True)
    from_date = db.Column(db.DateTime, index=True)
    to_date = db.Column(db.DateTime, index=True)
    created_at = db.Column(db.DateTime, default=get_date)
    last_updated = db.Column(
        db.DateTime, default=get_date, onupdate=get_date)

    def to_dict(self):
        return {
            "id": self.id,
            "payment_date": self.payment_date,
            "start_date": self.from_date,
            "end_date": self.to_date,
            "referrals_number": self.referrals_number,
            "referrals_amount": self.referrals_amount,
            "amount": self.amount,
            "hours": self.hours,
            "teacher_id": self.teacher_id,
            "created_at": self.created_at,
            "last_updated": self.last_updated
        }

    @staticmethod
    def get_wagepayment_by_id(id):
        return WagePayment.query.get(id)

    @staticmethod
    def get_tutor_wagepayments_by_email(email):
        """ Gets all wagepayments associated with teacher by their email. """
        return Teacher.get_teacher_by_email(email).wagepayments

    @staticmethod
    def get_tutor_wagepayments_by_id(id):
        """ Gets all wagepayments associated with teacher by their email. """
        return Teacher.get_teacher_by_id(id).wagepayments

    @staticmethod
    def create_wagepayment(teacher, start_date, end_date, payment_date):
        amount_hours = WagePayment.calculate_teacher_payment(
            teacher, start_date, end_date)
        if amount_hours['unpaid_wage'] != 0 or amount_hours['referrals_amount_unpaid'] != 0:
            wagepayment = WagePayment(
                teacher_id=teacher.id,
                payment_date=payment_date,
                amount=amount_hours['unpaid_wage'] +
                amount_hours['referrals_amount_unpaid'],
                hours=amount_hours['unpaid_hours'],
                referrals_amount=amount_hours['referrals_amount_unpaid'],
                referrals_number=amount_hours['referrals_number_unpaid'],
                from_date=start_date,
                to_date=end_date)
            for i in teacher.lessons_teacher:
                date_to_time = i.to_time.date()
                if start_date <= date_to_time <= end_date and i.status.value != 'scheduled':
                    i.paid = True
            for i in teacher.referrals:
                referral_date = i.created_at.date()
                if start_date <= referral_date <= end_date:
                    i.paid = True
            db.session.add(wagepayment)
            db.session.commit()
            return wagepayment
        return WagePayment(
            teacher_id=teacher.id,
            payment_date=payment_date,
            amount=0,
            referrals_amount=0,
            referrals_number=0,
            hours=0,
            from_date=start_date,
            to_date=end_date)

    @staticmethod
    def delete_wagepayment(id):
        wagepayment = WagePayment.get_wagepayment_by_id(id) or abort(404)
        db.session.delete(wagepayment)
        db.session.commit()
        return wagepayment

    @staticmethod
    def update_wagepayment(id=int, **kwargs):
        """Updates a wagepayment by the User id from the DB"""
        wagepayment = WagePayment.query.get(id)
        WagePayment.update(wagepayment, kwargs)
        db.session.commit()
        return wagepayment

    @staticmethod
    def calculate_teacher_payment(teacher, start_date, end_date):
        """Use this to calculate the wage 
        that has been paid and unpaid as well as paid/unpaid hours of a teacher 
        between 2 given dates
        """
        hours = 0
        paid_hours = 0
        wage = 0
        paid_wage = 0
        referrals_number_unpaid = 0
        referrals_amount_unpaid = 0
        referrals_amount_paid = 0
        referrals_number_paid = 0
        for i in teacher.lessons_teacher:
            date_to_time = i.to_time.date()
            lesson_duration = i.duration_in_minutes/60
            if start_date <= date_to_time <= end_date:
                if not i.paid:
                    if i.status.value == 'attended':
                        wage += i.wage
                        hours += lesson_duration
                    elif i.status.value == 'bad cancellation student':
                        if not i.trial_lesson:
                            if lesson_duration < 2:
                                wage += i.wage
                                hours += lesson_duration
                            else:
                                wage += (i.wage/lesson_duration)*2
                                hours += 2
                else:
                    if i.status.value == 'attended':
                        paid_wage += i.wage
                        paid_hours += lesson_duration
                    elif i.status.value == 'bad cancellation student':
                        if not i.trial_lesson:
                            if lesson_duration < 2:
                                paid_wage += i.wage
                                paid_hours += lesson_duration
                            else:
                                paid_wage += (i.wage/lesson_duration)*2
                                paid_hours += 2
        for i in teacher.referrals:
            if i.paid:
                referrals_number_paid += 1
                referrals_amount_paid += i.referral_amount
            else:
                referrals_number_unpaid += 1
                referrals_amount_unpaid += i.referral_amount
        return {'teacher_id': teacher.id,
                'unpaid_hours': hours,
                'unpaid_wage': wage,
                'paid_hours': paid_hours,
                'referrals_number_unpaid': referrals_number_unpaid,
                'referrals_amount_unpaid': referrals_amount_unpaid,
                'referrals_number_paid': referrals_number_paid,
                'referrals_amount_paid': referrals_amount_paid,
                'paid_wage': paid_wage,
                'start_date': start_date,
                'end_date': end_date}
