from apifairy.decorators import other_responses
from flask import Blueprint, abort, request
from apifairy import authenticate, body, response
from models.user import User
from models.customer import Customer
from models.balance import Balance
from api.auth import token_auth, limit_user_to_own_routes_decorator, admin_auth
from api.schema.customers import UpdateCustomerSchema, AddFamilyWithStudent, CustomerSchema, AddStudentToFamilySchema, ChangeStatusSchema, StudentIndependToFamily
from api.decorators import paginated_response
from api.schemas import CustomerStringPaginationSchema

customers = Blueprint('customers', __name__)

customer_schema = CustomerSchema()
add_student_schema = AddStudentToFamilySchema()
change_status_schema = ChangeStatusSchema()


@customers.route('/independent', methods=['POST'])
@authenticate(admin_auth)
@body(customer_schema)
@response(customer_schema, 201, description="An independent customer account was created with a user account and a student account. Note the student does not have a user account.")
@other_responses({
    401: 'Bad request: error in body.',
    400: 'Bad request: email provided already exists.'
})
def add_independent(args):
    """Add independent student.
    Adds a new Independent Customer with an user account and associated student.
    Note that the associated student does not have a user account.
    """
    email = args["email"]
    password = ''
    user = User(**args)
    independent = Customer.add_independent_customer_with_student(
        email=email,
        password=password,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone,
        customer_type='independent')
    balance = Balance.create_balance(independent['customer'].id)
    return independent['customer'].to_dict()


@customers.route('/customers', methods=['GET'])
@authenticate(admin_auth)
@paginated_response(CustomerSchema(many=True))
def all():
    """Retrieve all customers"""
    return Customer.query.filter_by(status='active')


@customers.route('/customers_filter', methods=['GET'])
@authenticate(token_auth)
@limit_user_to_own_routes_decorator
@paginated_response(CustomerSchema(many=True), pagination_schema=CustomerStringPaginationSchema)
def all_filter(*args, **kwargs):
    """Filter on some params and retrieve all customers"""
    status = request.args.get('status')
    customer_type = request.args.get('customer_type')
    name = request.args.get('name')
    if (status is None and customer_type is None and name is None):
        return Customer.query
    filterDict = {**request.args}
    filterDict.pop('limit', None)
    filterDict.pop('offset', None)
    print(filterDict)
    return Customer.query.filter_by(**filterDict)


@customers.route("/customer/<int:id>", methods=['GET'])
@authenticate(token_auth)
@response(CustomerSchema(), 201)
def get(id):
    """Get a customer by id."""
    customer = Customer.get_customer_by_id(id) or abort(404)
    return customer.to_dict()


@customers.route("/customer/<email>", methods=['GET'])
@authenticate(token_auth)
@response(CustomerSchema(), 201)
def get_with_email(email):
    """Get a customer by email."""
    customer = Customer.get_customer_by_email(email) or abort(404)
    return customer.customer.to_dict()


@customers.route('/customer', methods=['PUT'])
@authenticate(token_auth)
@body(UpdateCustomerSchema())
@response(UpdateCustomerSchema())
@other_responses({404: 'Customer has no user account.'})
def put(data):
    """Update Customer.
    Returns the updated customer.

    Note that you can also update fields related to the User profile.
    Note that Status and Customer Type are not updatable here.
    """
    customer = Customer.update_customer(**data) or abort(404)
    return customer.to_dict()


@customers.route('/customer/<int:id>', methods=['DELETE'])
@authenticate(admin_auth)
@response(CustomerSchema)
@other_responses({404: 'Customer not found'})
def delete_customer(id):
    """Delete a customer by customer_id"""
    customer = Customer.delete_customer(id) or abort(404)
    return customer.to_dict()


@customers.route('/convert_to_family_student', methods=['POST'])
@authenticate(admin_auth)
@body(StudentIndependToFamily())
@response(StudentIndependToFamily(), 201)
def convert_to_family_student(args):
    """Customer attached to student (independent), but now we want:
    Customer (to be the family) attached to the student.
    The user account was previously attached to the customer, but should now be attached to the student. 
    And a new user account should be made for the customer (family)
"""
    return_values = Customer.convert_to_family_student(**args)
    return return_values.to_dict()


@customers.route('/family', methods=['POST'])
@authenticate(admin_auth)
@body(customer_schema)
@response(customer_schema, 201, description="A family user account was created successfully")
@other_responses({401: 'Bad request: error in body.',
                  400: 'Bad request: email provided already exists.'})
def new(args):
    """Register a new family user"""
    email = request.json["email"]
    password = ''
    user = User(**args)
    customer = Customer.add_customer_user(
        email=email,
        password=password,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone,
        customer_type='family'
    )
    balance = Balance.create_balance(customer['customer'].id)
    return customer['customer'].to_dict()


@customers.route('/family_with_student', methods=['POST'])
@authenticate(admin_auth)
@body(AddFamilyWithStudent())
@response(AddFamilyWithStudent(), 201, description="A family user with a student attached was added to the family successfully")
@other_responses({401: 'Bad request: error in body.',
                  400: 'Bad request: email provided already exists.'})
def add_family_with_student(args):
    """Register a new family user with student attached
    Provide a family email address if it does not match returns a validation error
    else returns the added family(user and student is attached) data.
    """
    email = request.json["email"]
    student_data = {
        "first_name": args['student_first_name'],
        "last_name": args['student_last_name'],
        'gender': args['gender'],
        'student_type': 'child'
    }
    customer = Customer.add_customer_user(email=email,
                                          password='',
                                          first_name=args['first_name'],
                                          last_name=args['last_name'],
                                          phone=args['phone'],
                                          customer_type='family')
    student = Customer.add_student_to_family(
        email=email, student_data=student_data)
    balance = Balance.create_balance(customer['customer'].id)
    return customer['customer'].to_dict()


@customers.route('/add_student_to_family', methods=['POST'])
@authenticate(admin_auth)
@body(add_student_schema)
@response(add_student_schema, 201, description="A student was added to the family successfully")
@other_responses({401: 'Bad request: error in body.',
                  400: 'Bad request: email provided already exists.'})
def add_student_to_family(args):
    """Add a new student to a family user
    Provide a family email address if it does not match returns a validation error
    else returns the added student data.
    """
    student_data = {'first_name': args['first_name'],
                    "last_name": args['last_name'],
                    'gender': args['gender'],
                    'student_type': 'child'}
    added_student = Customer.add_student_to_family(
        args['email'], student_data=student_data)
    return added_student['student'].to_dict()


@customers.route('/change_customer_status', methods=['PUT'])
@authenticate(admin_auth)
@body(change_status_schema)
@response(change_status_schema, 200, description="The status of the account was changed successfully")
@other_responses({401: 'Bad request: error in body.',
                  400: 'Bad request: email provided already exists.'})
def change_status(args):
    """Change the status of the customer and attached students
    Provide an email address of the customer if it does not match returns a validation error
    else returns the updated status and customer data
    """
    user = Customer.change_status(**args)
    print(args['email'])
    print(user)
    return user.to_dict()
