from flask import redirect, url_for, request
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from decouple import config

import pickle
import os
import matplotlib.pyplot as plt
import json
import pprint


from models.subjects import Subjects
from models.order import Order
from models.teacher import Teacher
from models.higher_education_institution import HigherEducationInstitution
from models.higher_education_programme import HigherEducationProgramme
from models.high_school import HighSchool
from models.qualification import Qualification
from models.interest import Interest
from models.language import Language
class UserModelView(ModelView):
    """How the User table is viewed on the admin page."""

    page_size = 100
    column_display_pk = True
    column_searchable_list = [
        "email",
    ]

    column_filters = [
        "uid",
        "created_at",
        "last_updated",
        "is_verified",
        "verified_time",
        "email",
        "phone",
        "first_name",
        "last_name"
    ]

    can_export = True
    column_exclude_list = ["password_hash"]

    form_widget_args = {
        'created_at': {
            'disabled': True
        },
        'last_updated': {
            'disabled': True
        },
        'password_hash': {
            'disabled': True
        }
    }

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to index page if user doesn't have access
        return redirect(url_for("main.index", next=request.url))


class HigherEducationInstitutionModelView(ModelView):
    page_size = 100
    column_display_pk = True
    can_export = True
    form_widget_args = {
        'created_at': {
            'disabled': True
        },
        'last_updated': {
            'disabled': True
        },
        'teachers': {
            'disabled': True
        }
    }

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to index page if user doesn't have access
        return redirect(url_for("main.index", next=request.url))


class HigherEducationProgrammeModelView(ModelView):
    page_size = 100
    column_display_pk = True
    can_export = True
    form_widget_args = {
        'created_at': {
            'disabled': True
        },
        'last_updated': {
            'disabled': True
        },
    }

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to index page if user doesn't have access
        return redirect(url_for("main.index", next=request.url))


class QualificationsModelView(ModelView):
    page_size = 100
    column_display_pk = True
    can_export = True
    form_widget_args = {
        'created_at': {
            'disabled': True
        },
        'last_updated': {
            'disabled': True
        },
    }

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to index page if user doesn't have access
        return redirect(url_for("main.index", next=request.url))


class LessonsModelView(ModelView):
    page_size = 100
    column_display_pk = True
    can_export = True
    form_widget_args = {
        'created_at': {
            'disabled': True
        },
        'last_updated': {
            'disabled': True
        },
    }

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to index page if user doesn't have access
        return redirect(url_for("main.index", next=request.url))


class HighSchoolModelView(ModelView):
    page_size = 100
    column_display_pk = True
    can_export = True
    form_widget_args = {
        'created_at': {
            'disabled': True
        },
        'last_updated': {
            'disabled': True
        },
    }

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to index page if user doesn't have access
        return redirect(url_for("main.index", next=request.url))


class LanguagesModelView(ModelView):
    page_size = 100
    column_display_pk = True
    can_export = True
    form_widget_args = {
        'created_at': {
            'disabled': True
        },
        'last_updated': {
            'disabled': True
        },
    }

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to index page if user doesn't have access
        return redirect(url_for("main.index", next=request.url))


class ProgramsModelView(ModelView):
    page_size = 100
    column_display_pk = True
    can_export = True
    form_widget_args = {
        'created_at': {
            'disabled': True
        },
        'last_updated': {
            'disabled': True
        },
    }

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to index page if user doesn't have access
        return redirect(url_for("main.index", next=request.url))


class SubjectsModelView(ModelView):
    page_size = 100
    column_display_pk = True
    can_export = True
    form_widget_args = {
        'created_at': {
            'disabled': True
        },
        'last_updated': {
            'disabled': True
        },
    }

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to index page if user doesn't have access
        return redirect(url_for("main.index", next=request.url))


class InterestModelView(ModelView):
    page_size = 100
    column_display_pk = True
    can_export = True
    form_widget_args = {
        'created_at': {
            'disabled': True
        },
        'last_updated': {
            'disabled': True
        },
    }

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to index page if user doesn't have access
        return redirect(url_for("main.index", next=request.url))
        
class ReferralModelView(ModelView):
    page_size = 100
    column_display_pk = True
    can_export = True
    form_widget_args = {
        'created_at': {
            'disabled': True
        },
        'last_updated': {
            'disabled': True
        },
    }

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to index page if user doesn't have access
        return redirect(url_for("main.index", next=request.url))

class CustomerModelView(ModelView):
    """How the User table is viewed on the admin page."""

    page_size = 100
    column_display_pk = True
    column_searchable_list = [
        "user_id",
        "customer_type"
    ]

    can_export = True

    form_widget_args = {
        'created_at': {
            'disabled': True
        },
        'last_updated': {
            'disabled': True
        },
        'password_hash': {
            'disabled': True
        }
    }

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to index page if user doesn't have access
        return redirect(url_for("main.index", next=request.url))


class ContactFormLeadModelView(ModelView):
    """ How the form leads table is viewed on the admin page."""

    page_size = 100
    column_display_pk = True
    column_searchable_list = [
        "uid",
        "email",
        "name",
        "phone",
        "terms_accepted",
        "newsletter_accepted",
        "message",
        "zip_code",
        "adresse",
    ]
    column_filters = [
        "uid",
        "created_at",
        "last_updated",
        "email",
        "name",
        "phone",
        "terms_accepted",
        "newsletter_accepted",
        "message",
        "zip_code",
        "adresse",
    ]
    can_export = True

    form_widget_args = {
        'created_at': {
            'disabled': True
        },
        'last_updated': {
            'disabled': True
        }
    }

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to index page if user doesn't have access
        return redirect(url_for("main.index", next=request.url))


class PhoneLeadsModelView(ModelView):
    """ How the Phone Leads table is viewed on the admin page."""

    page_size = 100
    column_display_pk = True
    column_searchable_list = [
        "uid",
        "created_at",
        "phone",
    ]
    column_filters = [
        "uid",
        "created_at",
        "phone",
    ]
    can_export = True

    form_widget_args = {
        'created_at': {
            'disabled': True
        },
        'last_updated': {
            'disabled': True
        }
    }

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to index page if user doesn't have access
        return redirect(url_for("main.index", next=request.url))


class TeacherModelView(ModelView):
    """How the Teachers table is viewed on the admin page"""
    page_size = 100
    column_display_pk = True
    can_export = True
    column_searchable_list = [
        "user_id",
        "id"
    ]
    form_widget_args = {
        'created_at': {
            'disabled': True
        },
        'last_updated': {
            'disabled': True
        }
    }

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to index page if user doesn't have access
        return redirect(url_for("main.index", next=request.url))


class GeneralModelView(ModelView):
    """ How a general table is viewed on the admin page."""

    page_size = 100
    column_display_pk = True
    can_export = True

    form_widget_args = {
        'created_at': {
            'disabled': True
        },
        'last_updated': {
            'disabled': True
        }
    }

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to index page if user doesn't have access
        return redirect(url_for("main.index", next=request.url))


class TutorMapView(BaseView):
    @expose("/")
    def index(self):

        tutor_list = []
        subject_list = []
        #lessons_list = []
        interests_list = []
        uni_list = []
        gym_list = []
        qualification_list = []
        languages_list = []
        gmaps_key = config("GOOGLE_MAPS_API_KEY")

        # We set our tutor_list to the data in our tutor pickle
        # if the file is there, and it has data

        tutor_list = Teacher.all_tutors()
        subject_list = [i.to_tutormap() for i in Subjects.query.all()]
        # subject_list.sort()


        uni_list = [i.to_tutormap() for i in HigherEducationProgramme.query.all()]
        # uni_list.sort()
        qualification_list = [i.to_tutormap() for i in Qualification.query.all()]
        # qualification_list.sort()
        # gym_list.sort()

        languages_list = [i.to_tutormap() for i in Language.query.all()]      
        interests_list = [i.to_tutormap() for i in Interest.query.all()]

        return self.render(
            "tutormap.html",
            tutor_list=tutor_list,
            gmaps_key=gmaps_key,
            subject_list=subject_list,
            lst=uni_list,
            language_list=languages_list,
            qualification_list=qualification_list,
            interests=interests_list
        )

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to index page if user doesn't have access
        return redirect(url_for("main.index", next=request.url))


class RQDashboardView(BaseView):
    @expose("/")
    def index(self):
        return redirect("/admin/rq")

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to index page if user doesn't have access
        return redirect(url_for("main.index", next=request.url))


class AnalyticsView(BaseView):
    @expose("/")
    def index(self):

        booking_data = Order.booking_sum()
        circle_diagrams = Order.circle_diagrams()
        
        return self.render(
            "analytics.html",
            booking_data=booking_data, formatted_data=circle_diagrams
        )
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to index page if user doesn't have access
        return redirect(url_for("main.index", next=request.url))


class RegisterNewAdmin(BaseView):
    @expose("/")
    def index(self):
        return self.render("registeradmin.html")

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin 

    def inaccessible_callback(self, name, **kwargs):
        # redirect to index page if user doesn't have access
        return redirect(url_for("main.index", next=request.url))
