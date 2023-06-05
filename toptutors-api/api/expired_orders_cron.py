import time
from dateutil.relativedelta import relativedelta
from sqlalchemy import func
from api.utils.utils import get_date
from models.order import Order, OrderStatus
from models.balance import Balance
from models.lesson import Lesson
from models.student import Student
from api.app import db


def expire_orders():
    print('Expiration working')

    filter_date = get_date() + relativedelta(days=-1)
    print(filter_date)

    start_time = time.time()
    orders = db.session.query(
        Order.customer_id, func.sum(Order.total_hours),
        func.max(Balance.hours_used), func.count(
            Order.uid),
        func.array_agg(Order.uid))\
        .join(Balance, Balance.customer_id == Order.customer_id)\
        .filter(Order.expiration_date <= filter_date,
                Order.status != OrderStatus.VOID,
                Order.expired != True)\
        .group_by(Order.customer_id).all()

    for order in orders:
        order_ids = order[4]
        Order.query.filter(Order.uid.in_(order_ids)).\
            update({Order.expired: True}, synchronize_session=False)
        diffrence = float(order[1] - order[2])

        if diffrence > 0:
            from_time = filter_date.replace(hour=23, minute=59)
            to_time = filter_date.replace(hour=23, minute=59)
            order_customer_id = order[0]
            student = (
                db.session.query(Student)
                .filter(Student.customer_id == order_customer_id)
                .first()
            )

            lesson = Lesson(
                title='EXPIRED LESSONS ',
                space='',
                secret='',
                space_id='',
                completion_notes='EXPIRED LESSON',
                session_id='EXPIRED LESSON',
                teacher_id=1,
                from_time=from_time,
                to_time=to_time,
                duration_in_minutes=round(diffrence*60),
                description="EXPIRED LESSONS",
                wage=0,
                status='expired'
            )
            db.session.add(lesson)
            db.session.commit()
            lesson.lessons_students.append(student)

    db.session.commit()
    end_time = time.time()
    time_elapsed = end_time - start_time
    print(f"Time complexity for input size n: {time_elapsed:.8f} seconds")

