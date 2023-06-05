from apifairy.decorators import other_responses
from flask import Blueprint, abort, request
from apifairy import authenticate, body, response
from datetime import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import joinedload

from api.app import db
from models.lesson import Lesson,LessonStatus
from models.balance import Balance
from api.schema.lessons import PlaybackUrlSchema, CalendarLessons, LessonSchema,\
    UpdateLessonSchema, RescheduledLesson, \
    CreateLessonSchema, CompleteLessonSchema, \
    CancelLessonSchema
from api.auth import token_auth, admin_auth, limit_user_to_own_routes_decorator
from api.decorators import paginated_response, query_params
from api.utils.utils import get_date
from api.utils.lessonspace import get_playback_url
from api.schemas import LessonsPaginationSchema
import time
# Blueprint
lessons = Blueprint('lessons', __name__)

# Schemas
lesson_schema = LessonSchema()
lessons_schema = LessonSchema(many=True)


@lessons.route('/lesson', methods=['POST'])
@authenticate(token_auth)
@body(CreateLessonSchema())
@response(CreateLessonSchema(), 201)
def new(args):
    """Creates a new Lesson.
    Adds Lessonspace integration and updates the student's customer's Balance.
    Returns the Lesson """

    # Create the Lesson
    lesson = Lesson.add_new_lesson(**args)

    # Update the Balance.
    Balance.schedule_lesson(lesson.id)
    return lesson.to_dict()


@lessons.route('/lesson/<int:id>', methods=['DELETE'])
@authenticate(admin_auth)
@response(lesson_schema)
@other_responses({404: 'lesson not found'})
def delete_lesson(id):
    """Delete a lesson by id"""
    lesson = Lesson.delete_lesson(id) or abort(404)
    return lesson


@lessons.route('/lesson', methods=['GET'])
@authenticate(token_auth)
@paginated_response(schema=lessons_schema, pagination_schema=LessonsPaginationSchema())
def all():
    """Retrieve all lessons"""
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    if (from_date is None and to_date is None):
        return Lesson.query
    start_date_time = datetime.strptime(from_date, '%Y-%m-%d')
    end_date_time = datetime.strptime(to_date, '%Y-%m-%d')
    lessons = Lesson.query.filter(
        Lesson.from_time.between(start_date_time, end_date_time))
    return lessons


@lessons.route('/lesson/<int:id>', methods=['GET'])
@authenticate(token_auth)
@limit_user_to_own_routes_decorator
@response(lesson_schema)
@other_responses({404: 'lesson not found'})
def get(id):
    """Retrieve a lesson by id"""
    lesson = Lesson.get_lesson_by_id(id) or abort(404)
    return lesson.to_dict()


@lessons.route('/lesson_replay/<int:id>', methods=['GET'])
@authenticate(token_auth)
@limit_user_to_own_routes_decorator
@response(PlaybackUrlSchema())
@other_responses({404: 'lesson not found'})
def get_lesson_replay(id):
    """Retrieves a recording of the lessons
    Returns an array of each recording 
    for every session that has occured for a lesson
    between the student and the teacher
    """
    lesson = Lesson.get_lesson_by_id(id) or abort(404)
    playback_array = get_playback_url(
        lesson.lessons_teacher, lesson.lessons_students[0], lesson.session_id, lesson)
    return playback_array


@lessons.route('/update_lessons', methods=['PUT'])
@authenticate(token_auth)
@response(UpdateLessonSchema(), 201)
@body(UpdateLessonSchema())
def put_lesson(data):
    """Edit lessons information
     Fields given get updated all other ones don't"""
    return Lesson.update_lesson(**data).to_dict()


@lessons.route('/complete_lessons', methods=['PUT'])
@authenticate(token_auth)
@limit_user_to_own_routes_decorator
@response(LessonSchema())
@body(CompleteLessonSchema())
def complete_lessons(data):
    """Completes a Lesson,changes the balance of the customer account as well"""
    lesson_data = {'id': data['id'], 'status': data['status'], 'completed_at': get_date(
    ), 'completion_notes': data['completion_notes']}
    lesson = Lesson.update_lesson(**lesson_data).to_dict()
    new_balance = Balance.use_lesson(lesson_id=lesson_data['id'])
    return lesson


@lessons.route('/reschedule_lesson', methods=['PUT'])
@authenticate(token_auth)
@limit_user_to_own_routes_decorator
@response(LessonSchema())
@body(RescheduledLesson())
def reschedule_lesson(args):
    """Reschedules a lesson, recalculates the balance at the same time"""
    lesson = Lesson.reschedule_lesson(
        id=args['id'], from_time=args['from_time'], to_time=args['to_time'])
    # Balance.schedule_lesson(args['id'])
    return lesson.to_dict()


@lessons.route('/cancel_lesson', methods=['PUT'])
@authenticate(token_auth)
@limit_user_to_own_routes_decorator
@response(LessonSchema())
@body(CancelLessonSchema())
def cancel_lesson(args):
    """Cancel a lesson, recalculates the balance at the same time"""
    from models.balance import Balance
    reason = args['cancellation_reason']
    lesson_id = args['lesson_id']
    lesson = Lesson.update_lesson(id=lesson_id, status=reason)
    Balance.cancel_lesson(lesson_id, reason)
    return lesson.to_dict()


@lessons.route('/lessons-teacher/<int:teacher_id>', methods=['GET'])
@authenticate(token_auth)
@query_params(CalendarLessons(many=True), CalendarLessons())
@other_responses({404: 'lesson not found'})
def get_all_lessons_for_teacher(args, teacher_id):
    """Retrieve all lessons for a teacher"""
    start_date = None
    end_date = None
    if 'start_date' in args.keys() and 'end_date' in args.keys():
        start_date = args['start_date']
        end_date = args['end_date']
    lessons = Lesson.get_all_lessons_for_teacher(
        teacher_id, start_date, end_date)
    data = [i.to_dict() for i in (lessons or [])]
    db.session.remove()
    return {'data': data}

@lessons.route('/lessons-admin', methods=['GET'])
#@authenticate(admin_auth)
@query_params(CalendarLessons(many=True), CalendarLessons())
@other_responses({404: 'lesson not found'})
def get_all_lessons_for_admin(args):
    """Retrieve all lessons for an admin"""
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    start_time = time.time()
    if (from_date is None or to_date is None):
        end_date_time = get_date()
        start_date_time = end_date_time + relativedelta(end_date_time, months=-1)

    start_date_time = datetime.strptime(from_date, '%Y-%m-%d')
    end_date_time = datetime.strptime(to_date, '%Y-%m-%d')
    lessons = Lesson.query.options(
            joinedload(Lesson.lessons_students),
            joinedload(Lesson.lessons_teacher)
        ).filter(
        Lesson.from_time.between(start_date_time, end_date_time)).all()
    data = [i.to_calendar() for i in lessons]
    end_time = time.time()
    time_elapsed = end_time - start_time
    print(f"Time complexity for input size n: {time_elapsed:.8f} seconds")
    return {'data': data}

@lessons.route('/lessons-student/<int:student_id>', methods=['GET'])
#@authenticate(token_auth)
@query_params(CalendarLessons(many=True), CalendarLessons())
@other_responses({404: 'lesson not found'})
def get_all_lessons_for_student(args, student_id):
    """Retrieve all lessons for a student"""
    start_date = None
    end_date = None
    if 'start_date' in args.keys() and 'end_date' in args.keys():
        start_date = args['start_date']
        end_date = args['end_date']
    lessons = Lesson.get_all_lessons_for_student(
        student_id, start_date, end_date)
    print(lessons)
    data = [i.to_calendar() for i in (lessons or [])]
    db.session.remove()
    return {'data': data}


@lessons.route('/lessons-customer/<int:customer_id>', methods=['GET'])
@authenticate(token_auth)
@query_params(CalendarLessons(many=True), CalendarLessons())
@other_responses({404: 'lesson not found'})
def get_all_lessons_for_customer(args, customer_id):
    """Retrieve all lessons for a customer"""
    start_date = None
    end_date = None
    if 'start_date' in args.keys() and 'end_date' in args.keys():
        start_date = args['start_date']
        end_date = args['end_date']
    lessons = Lesson.get_all_lessons_for_a_customer(customer_id,
                                                    start_date,
                                                    end_date)
    data = [i.to_calendar() for i in (lessons or [])]
    db.session.remove()
    return {'data': data}
