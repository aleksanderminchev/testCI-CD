import sentry_sdk
import rq_dashboard
import rq
import os
import sys
from redis import Redis
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.rq import RqIntegration
# Get the directory path of the external module
external_module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),"../../"))
# Add the directory path to the Python path
sys.path.append(external_module_dir)
from apifairy import APIFairy
from flask import Flask, request, g, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_mail import Mail
from flask_minify import minify
from flask_compress import Compress
from flask_login import LoginManager, current_user
from flask_admin import Admin
from config import config

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
cors = CORS()
mail = Mail()
apifairy = APIFairy()
compress = Compress()
login_manager = LoginManager()
login_manager.login_view = 'login'
admin = Admin(name='TopTutors Admin', template_mode='bootstrap3')


def create_app(config_name="development"):
    # logging production errors in sentry
    if config_name == "production":
        sentry_sdk.init(
            dsn="https://3ce6366cd61a4ddabc5b8a0ce7830642@o478493.ingest.sentry.io/5521105",
            integrations=[
                FlaskIntegration(), SqlalchemyIntegration(), RqIntegration()],
            traces_sample_rate=1.0,
        )

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config.from_object(rq_dashboard.default_settings)

    # extensions
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    mail.init_app(app)

    if app.config['USE_CORS']:  # pragma: no branch'
        cors.init_app(app, supports_credentials=True)

    if config_name == "development":
        apifairy.init_app(app)

    compress.init_app(app)
    minify(app=app, html=True, js=True, cssless=True)
    login_manager.init_app(app)
    admin.init_app(app)
    app.redis = Redis.from_url(app.config["RQ_DASHBOARD_REDIS_URL"])
    app.task_queue = rq.Queue("api_worker", connection=app.redis)
    # blueprints
    from api.blueprints.errors import errors
    app.register_blueprint(errors)
    from api.blueprints.fake import fake
    app.register_blueprint(fake)
    from api.blueprints.misc import misc
    app.register_blueprint(misc)
    from api.blueprints.redirects import redirects
    app.register_blueprint(redirects)

    # Page Routes
    from api.blueprints.pages.orders import orders
    app.register_blueprint(orders, url_prefix="/order")
    from api.blueprints.pages.courses import courses
    app.register_blueprint(courses, url_prefix="/course")

    # Page Routes
    from api.blueprints.pages.main import main
    app.register_blueprint(main)
    from api.blueprints.pages.logins import logins
    app.register_blueprint(logins)

    # api blueprints
    from api.blueprints.api.tokens import tokens
    app.register_blueprint(tokens, url_prefix='/api')
    from api.blueprints.api.users import users
    app.register_blueprint(users, url_prefix='/api')

    from api.blueprints.api.customers import customers
    app.register_blueprint(customers, url_prefix='/api')
    from api.blueprints.api.balances import balances
    app.register_blueprint(balances, url_prefix='/api')
    from api.blueprints.api.wagepayments import wagepayments
    app.register_blueprint(wagepayments, url_prefix='/api')
    from api.blueprints.api.transactions import transactions
    app.register_blueprint(transactions, url_prefix='/api')
    from api.blueprints.api.students import students
    app.register_blueprint(students, url_prefix='/api')
    from api.blueprints.api.teachers import teachers
    app.register_blueprint(teachers, url_prefix='/api')
    from api.blueprints.api.higher_education import higher_education
    app.register_blueprint(higher_education, url_prefix='/api')
    from api.blueprints.api.highschool import high_school
    app.register_blueprint(high_school, url_prefix='/api')
    from api.blueprints.api.lessons import lessons
    app.register_blueprint(lessons, url_prefix='/api')
    from api.blueprints.api.courses import courses
    app.register_blueprint(courses, url_prefix='/api')

    from api.blueprints.api.subjects import subjects as subjects
    app.register_blueprint(subjects, url_prefix='/api')
    from api.blueprints.api.languages import languages
    app.register_blueprint(languages, url_prefix='/api')
    from api.blueprints.api.referrals import referrals as referrals
    app.register_blueprint(referrals, url_prefix='/api')
    from api.blueprints.api.interests import interests
    app.register_blueprint(interests, url_prefix='/api')
    from api.blueprints.api.qualifications import qualifications
    app.register_blueprint(qualifications, url_prefix='/api')
    from api.blueprints.api.programs import programs
    app.register_blueprint(programs, url_prefix='/api')
    from api.blueprints.api.orders import orders
    app.register_blueprint(orders, url_prefix='/api')
    from api.blueprints.api.tutors import tutors
    app.register_blueprint(tutors, url_prefix='/api')
    from api.blueprints.api.teachworks import teachworks
    app.register_blueprint(teachworks, url_prefix='/api/tw')
    from api.blueprints.api.webhooks import webhooks
    app.register_blueprint(webhooks)

    from models.user import User
    from models.contactformleads import ContactFormLead
    from models.phonelead import PhoneLead
    from models.order import Order
    from models.course import Course
    from models.customer import Customer
    from models.teacher import Teacher
    from models.student import Student
    from models.lesson import Lesson
    from models.higher_education_institution import HigherEducationInstitution
    from models.higher_education_programme import HigherEducationProgramme
    from models.qualification import Qualification
    from models.high_school import HighSchool
    from models.language import Language
    from models.interest import Interest
    from models.referral import Referral
    from models.subjects import Subjects as TeacherSubjects
    from models.program import Program
    from models.wagepayment import WagePayment
    from .modelviews import (
        UserModelView,
        ContactFormLeadModelView,
        PhoneLeadsModelView,
        TutorMapView,
        RQDashboardView,
        TeacherModelView,
        GeneralModelView,
        CustomerModelView,
        HigherEducationInstitutionModelView,
        HigherEducationProgrammeModelView,
        QualificationsModelView,
        LessonsModelView,
        HighSchoolModelView,
        InterestModelView,
        LanguagesModelView,
        ProgramsModelView,
        SubjectsModelView,
        AnalyticsView
    )
    # Admin dashboard tabs
    admin.add_view(HigherEducationInstitutionModelView(
        HigherEducationInstitution, db.session))
    admin.add_view(HigherEducationProgrammeModelView(
        HigherEducationProgramme, db.session))
    admin.add_view(QualificationsModelView(Qualification, db.session))
    admin.add_view(LessonsModelView(Lesson, db.session))
    admin.add_view(LanguagesModelView(Language, db.session))
    admin.add_view(InterestModelView(Interest, db.session))
    admin.add_view(HighSchoolModelView(HighSchool, db.session))
    admin.add_view(ProgramsModelView(Program, db.session))
    admin.add_view(SubjectsModelView(TeacherSubjects, db.session))
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(CustomerModelView(Customer, db.session))
    admin.add_view(ContactFormLeadModelView(ContactFormLead, db.session))
    admin.add_view(GeneralModelView(Order, db.session))
    admin.add_view(RQDashboardView(name="RQ Dashboard"))
    admin.add_view(TutorMapView(name="Tutor Map"))
    admin.add_view(TeacherModelView(Teacher, db.session))
    admin.add_view(GeneralModelView(Course, db.session))
    admin.add_view(GeneralModelView(WagePayment, db.session))
    admin.add_view(PhoneLeadsModelView(PhoneLead, db.session))
    admin.add_view(AnalyticsView(name="Analytics"))

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from api.decorators import admin_role_required

    @ admin_role_required
    def rq_login_required():
        """ Used so we can decorate our dashboard with @login_required """
        return None

    rq_dashboard.blueprint.before_request(rq_login_required)
    app.register_blueprint(rq_dashboard.blueprint, url_prefix="/admin/rq")

    @ app.context_processor
    def captcha_sitekey():
        sitekey = app.config["CAPTCHA_SITE_KEY"]
        return dict(sitekey=sitekey)

    @ app.before_request
    def before_request():
        g.user = current_user

    @ app.after_request
    def after_request(response):
        # Werkzeug sometimes does not flush the request body so we do it here
        request.get_data()

        # Only if it's GET and not a static file
        if request.method == 'GET' and '.' not in request.path:
            paid = request.args.get('paid')
            if paid is not None:
                response.set_cookie("paid", value=paid)

            pacid = request.args.get('pacid')
            if pacid is not None:
                response.set_cookie("pacid", value=pacid)

            asclid = request.args.get('asclid')
            if asclid is not None:
                response.set_cookie("asclid", value=asclid)
        return response

    # Teachworks login
    @ app.route("/login")
    def login():
        return render_template("toptutor-login.html")

    # define the shell context
    @app.shell_context_processor
    def shell_context():  # pragma: no cover
        return dict(db=db, User=User, Order=Order, Course=Course,
                    Customer=Customer, Teacher=Teacher, Student=Student,
                    Lesson=Lesson, Interest=Interest, HigherEducationInstitution=HigherEducationInstitution,
                    HigherEducationProgramme=HigherEducationProgramme, Qualification=Qualification,
                    HighSchool=HighSchool, Language=Language, Referral=Referral,
                    Subjects=TeacherSubjects, Program=Program, WagePayment=WagePayment
                    )
    if config_name == 'production':
        @app.cli.command()
        @monitor(monitor_slug='data-migration-job')
        def sync_tw_data():
            """ Run scheduled jobs to synchronize TW data with DB. """
            from api.teachworks_cron import work_teachers, work_customer, work_student, work_lesson, work_payslips
            print("Running Teachworks data sync...")
            work_teachers()
            work_customer()
            work_student()
            work_lesson()
            work_payslips()

        @app.cli.command()
        @monitor(monitor_slug='expired-lessons')
        def expired_orders():
            """ Run scheduled job to expire lessons. """
            from api.expired_orders_cron import expire_orders
            expire_orders()

    with app.app_context():
        return app
