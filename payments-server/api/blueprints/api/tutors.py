from flask import request, Blueprint
from apifairy import authenticate, other_responses, body

from api.auth import admin_auth
from api.utils.matching_algorithm import get_matching_tutors
from api.schemas import TutorMatchSchema
from flask import Blueprint, request

tutors = Blueprint('Tutors', __name__)


