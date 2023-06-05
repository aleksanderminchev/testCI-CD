from models.wagepayment import WagePayment
from flask import Blueprint, abort, send_file, render_template, request
from apifairy import authenticate, other_responses, body, response

from api.decorators import paginated_response
from api.utils.payslips import createCSV
from api.auth import admin_auth, token_auth, limit_user_to_own_routes_decorator
from api.schema.wagepayments import AddBulkWagePayments, WagePaymentSchema, CalculateWagePayments
from models.teacher import Teacher


wagepayments = Blueprint('wagepayments', __name__)


@wagepayments.route('/wagepayment/<int:id>', methods=['GET'])
@limit_user_to_own_routes_decorator
@authenticate(token_auth)
@response(WagePaymentSchema(), 201)
@other_responses({404: 'Wage payment not found'})
def get_wagepayments(id):
    """Get wagepayment by id"""
    wagepayment = WagePayment.get_wagepayment_by_id(id) or abort(404)
    return wagepayment.to_dict()


@wagepayments.route('/wagepayments', methods=['GET'])
@limit_user_to_own_routes_decorator
@authenticate(token_auth)
@paginated_response(schema=WagePaymentSchema(many=True))
def all():
    """Retrieves all wage payments"""
    return WagePayment.query


@wagepayments.route('/wagepayment', methods=['POST'])
@authenticate(admin_auth)
@body(WagePaymentSchema())
@response(WagePaymentSchema(), 201)
def create_wagepayments(args):
    """ Create a new WagePayment. 
    Calculates the wage payment between two dates. 
    If the calculated payment equals 0 it returns an empty dict. 
    """
    from models.teacher import Teacher
    teacher = Teacher.get_teacher_by_id(args['teacher_id'])
    wagepayment = WagePayment.create_wagepayment(
        teacher, args['start_date'], args['end_date'], args['payment_date'])
    return wagepayment


@wagepayments.route('/bulk_wagepayments', methods=['POST'])
@authenticate(admin_auth)
@body(AddBulkWagePayments())
@response(WagePaymentSchema(many=True), 201)
def create_bulk_wagepayments(args):
    """Creates bulk wage payments"""
    from models.teacher import Teacher
    teacher_ids = Teacher.query.all()
    wagepayments_for_return = []
    for teacher in teacher_ids:
        wagepayment = WagePayment.create_wagepayment(
            teacher, args['start_date'], args['end_date'], args['payment_date'])
        wagepayments_for_return.append(wagepayment)
        html = render_template("email/payslip.html",
                               teacher=teacher, wage_info=wagepayment)
        # send_email([teacher.user.email], "Din TopTutors Ordre er godkendt!", html)
    createCSV(teacher_ids, wagepayments_for_return,
              args['start_date'], args['end_date'])
    return wagepayments_for_return


@wagepayments.route('/wagepayment/<int:id>', methods=['DELETE'])
@authenticate(admin_auth)
@response(WagePaymentSchema())
def delete_wagepayment(id):
    """Delete a wagepayment"""
    wagepayment = WagePayment.delete_wagepayment(id)
    return wagepayment.to_dict()


@wagepayments.route('/update_wagepayment', methods=['PUT'])
@authenticate(admin_auth)
@body(WagePaymentSchema)
@response(WagePaymentSchema)
def update_wagepayment(args):
    """Update a wagepayment"""
    wagepayment = WagePayment.update_wagepayment(**args)
    return wagepayment.to_dict()


@wagepayments.route('/tutor_wagepayments/<id>', methods=['GET'])
@authenticate(token_auth)
@limit_user_to_own_routes_decorator
@response(WagePaymentSchema(many=True))
def get_wagepayments_by_tutor_id(id):
    """Get all wagepayments for a teacher by his ID."""
    wagepayments = WagePayment.get_tutor_wagepayments_by_id(id) or abort(404)
    return wagepayments


@wagepayments.route('/calculate_wages_hours', methods=['POST'])
@authenticate(admin_auth)
@body(CalculateWagePayments)
@response(CalculateWagePayments(many=True))
def calculate_wages_hours(args):
    """Calculates the paid/unpaid wage and paid/unpaid hours of a teacher 
    between 2 given dates
    """
    teachers = Teacher.query.all()
    calculatedWages = [WagePayment.calculate_teacher_payment(
        teacher, args['start_date'], args['end_date']) for teacher in teachers]
    print(calculatedWages)
    # createCSVForPreviousMonth(teachers,calculatedWages)
    return calculatedWages


@wagepayments.route('/download', methods=['POST'])
@authenticate(admin_auth)
def download_excell():
    """Download the excel payslip that was generated"""
    # stream the response as the data is generated
    start_date = request.json['start_date']
    end_date = request.json['end_date']
    return send_file(f'D:\\Work\\TopTutors\\toptutors-flask-react-app\\toptutors-api\\wages_{start_date}_{end_date}.xlsx')
