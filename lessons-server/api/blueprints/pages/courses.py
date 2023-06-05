from flask import Blueprint, render_template, current_app, redirect, url_for, request, session

from models.teacher import Teacher
from models.course import Course
from api.utils.routes_utils import render_page_404, course_teacher_search
from api.services import zoho_crm
from api import db

courses = Blueprint('courses', __name__)


@courses.route("/<hashed_id>/<tutor_id>", methods=["GET"])
def view_course(hashed_id, tutor_id):
    try:
        tutor = Teacher.get_teacher_by_id(tutor_id)
        if tutor is None:
            return render_page_404()
        course = Course.in_db(hashed_id)

        # Set taken by to False as default and check if the tutor checking is the one that took it.
        taken_by_tutor = False
        if course.taken_by and int(course.taken_by) == int(tutor_id):
            taken_by_tutor = True

        if tutor and course:
            return render_template("course/display_course.html", course=course, tutor=tutor, taken_by_tutor=taken_by_tutor)

    except Exception:
        return render_page_404()


@courses.route("/<hashed_id>/<tutor_id>/accept", methods=["GET"])
def accept_course(hashed_id, tutor_id):
    tutor = Teacher.get_teacher_by_id(tutor_id)

    course = Course.in_db(hashed_id)

    # If course is already taken by either this tutor or someone else
    if not course.taken_by:
        course.taken_by = tutor_id
        course.status = "Taken"
        db.session.add(course)
        db.session.commit()

        if current_app.config.get("ENV_NAME") == "production":
            current_app.task_queue.enqueue_call(
                func=zoho_crm.tutor_accepted_course_webhook,
                args=(course.tutor.user_id, course.crm_deal_id, tutor.email),
                result_ttl=5000,
            )
    # redirect course/<hashed_id>/<tutor_id>
    return redirect(url_for("courses.view_course", hashed_id=hashed_id, tutor_id=tutor_id))


@courses.route("/", methods=['GET', 'POST'])
def signup_to_tutor():
    """
    Route handler for the signup page.
    """

    # Check if tutor is in session.
    try:
        tutor = session["teacher"]
    except Exception:
        tutor = None

    # No tutor and no tutor email submitted.
    if tutor is None and request.method != 'POST':
        return render_template("course/elever.html", found_courses=None, tutor=None)

    courses = Course.query.filter(Course.status == 'Pending', Course.hidden.isnot(True)).order_by(
        Course.created_at.desc()).all()

    returnObject = course_teacher_search(
        request.form['email'], courses)

    if returnObject is None:
        return render_template("course/elever.html", found_courses=None, tutor=None)

    return render_template("course/elever.html", found_courses=returnObject['found_courses'], tutor=returnObject['tutor'])
