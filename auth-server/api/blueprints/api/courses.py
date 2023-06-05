from flask import request, Blueprint, abort
from apifairy import authenticate, other_responses, body, response


from api.auth import admin_auth
from api.utils.matching_algorithm import get_matching_tutors
from api.schemas import CourseAddSchema, UpdateCourseStatusSchema, UpdateCourseSchema, CourseSchema, TutorMatchSchema
from models.course import Course
from api import db

courses = Blueprint('Courses', __name__)

# Add route "/" POST"


@courses.route("/course", methods=["POST"])
@authenticate(admin_auth)
@body(CourseSchema)
@other_responses({401: 'Bad request: error in body.'})
@response(CourseSchema, 201)
def create_course(course):
    """ Create Course
    This endpoint creates a course."""
    course = Course.add(request.json)
    return course.to_dict()


@courses.route("/generate_course_url", methods=["POST"])
@authenticate(admin_auth)
@body(CourseAddSchema)
@other_responses({401: 'Bad request: error in body.'})
def generate_course_url(filters):
    """ Create Course & algorithmic match."""
    # Get posted arguments

    # Create a course course data
    Course.add(filters["course"])

    # Get data for algorithm
    hard_filters = filters["hard_filters"]  # DICTIONARY OF HARD FILTERS
    soft_filters = filters["soft_filters"]  # DICTIONARY OF SOFT FILTERS

    # Adding hard filters
    hard_filters["subjects"] = filters["subjects"]  # LIST OF SUBJECTS
    hard_filters["status"] = "active"
    hard_filters["open_for_new_students"] = True

    matching_tutors = get_matching_tutors(hard_filters, soft_filters)

    return {"results": matching_tutors}


@courses.route("/algorithm", methods=["GET"])
@authenticate(admin_auth)
@body(TutorMatchSchema)
@other_responses({401: 'Bad request: error in body.'})
def algorithm(filters):
    """
    Algorithmic tutor match.
    """

    # Get data for algorithm
    hard_filters = filters["hard_filters"]  # DICTIONARY OF HARD FILTERS
    soft_filters = filters["soft_filters"]  # DICTIONARY OF SOFT FILTERS

    # Adding hard filters
    hard_filters["subjects"] = filters["subjects"]  # LIST OF SUBJECTS
    hard_filters["status"] = "active"
    hard_filters["open_for_new_students"] = True

    matching_tutors = get_matching_tutors(hard_filters, soft_filters)

    return {"results": matching_tutors}


@courses.route("/change_course_status", methods=["PUT"])
@authenticate(admin_auth)
@body(UpdateCourseStatusSchema)
@response(UpdateCourseStatusSchema)
@other_responses({401: 'Bad request: error in body.'})
def change_course_status(data):
    hashed_id = data["hashed_id"]
    status = data["status"]

    course = Course.query.filter_by(hashed_id=hashed_id).first()

    if not course:
        abort(404, "Course not found.")

    Course.change_status(course.uid, status)

    return {"id": id, "status": status}


@courses.route("/update_course", methods=["PUT"])
@authenticate(admin_auth)
@body(UpdateCourseSchema)
@response(UpdateCourseSchema)
@other_responses({401: 'Bad request: error in body.'})
def update_course(data):
    """ Update Course"""
    course = Course.query.filter_by(hashed_id=data["id"]).first()
    if not course:
        abort(404, "Course not found.")

    course.update(data)
    db.session.add(course)
    db.session.commit()
    return course
