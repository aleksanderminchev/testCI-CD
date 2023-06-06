from flask import request, Blueprint, render_template, abort
from apifairy import authenticate, other_responses, body, response
from api.decorators import paginated_response

from api.email import send_email
from api.auth import admin_auth, token_auth, limit_user_to_own_routes_decorator
from api.utils.stripe_utils import StripeCustomer
from api.utils.utils import get_date
from models.order import Order
from models.balance import Balance
from api.schemas import OrderSchema, UpdateOrderSchema
from api.schema.orders import VoidOrderSchema
orders = Blueprint('Orders', __name__)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)


@orders.route("/add_order", methods=["POST"])
@authenticate(admin_auth)
@body(order_schema)
@other_responses({401: 'Bad request: error in body.'})
def add_order(user):
    """
    Add order
    Adds an order to the DB and creates an invoice URL, so the customer can pay the invoice.

    Package has to be the Stripe ID of the package. E.g. "single-399" for hours or "3-months-249" for packages

    Discount has to be the number percentage wanted, where the following values are supported: 5, 10, 15, and 20.
    Otherwise, the discount can be the Stripe ID for the coupon.
    """
    try:
        order = request.json

        order_total_hours = order.get("total_hours", 0)
        order_package = order.get("package")
        order_installments = order.get("installments", 1)
        order_crm_deal_id = order.get("crm_deal_id")
        order_email = order.get("email")
        order_name = order.get("name")
        order_send_email = order.get("email_sent", False)
        order_discount = order.get("discount")
        order_stripe_customer_id = order.get("stripe_customer")
        order_extra_student = order.get("extra_student")
        upsell = order.get("upsell")

        # Calculate the total price for the package.
        total_price = StripeCustomer.get_total_package_price(
            order_package, order_total_hours)

        # Get the price per hour
        unit_price = StripeCustomer.get_package_price(order_package)

        if order_discount:
            # If there is a discount, calculate the price after discount and update the total price.
            price_after_discount = total_price * \
                StripeCustomer.get_discount(order_discount)
            total_price = round(price_after_discount, 2)
            unit_discount = unit_price * \
                StripeCustomer.get_discount(order_discount)
            unit_discount = unit_price - unit_discount

        if order_extra_student:
            # Calculate extra student fees if there are extra students.
            extra_student_fee_per_installment = order_total_hours / order_installments
            # 50 kr. is the fee per extra student.
            extra_student_fee_per_installment *= 50
            extra_student_fee_per_installment *= order_extra_student
            extra_student_fee_per_installment = round(
                extra_student_fee_per_installment, 2)
            total_price += extra_student_fee_per_installment * order_installments

        # Create Stripe Customer.
        customer = StripeCustomer(
            order_total_hours,
            total_price,
            unit_price,
            order_package,
            order_installments,
            order_crm_deal_id,
            order_extra_student,
            order_discount,
            order_stripe_customer_id,
            order_email,
            order_name,
            upsell
        )

        if order_stripe_customer_id is None:
            # Check if a Stripe account with the given email already exists.
            customer.get_customer_id()

        order = Order.add_new(customer, order_send_email)
        order.update_url(f"toptutors.dk/order/{order.hashed_id}")

        if order_send_email:
            send_email([order_email], "Din TopTutors ordre", render_template(
                "email/invoice.html", url=order.stripe_url))

        return {"order_id": order.hashed_id}

    except Exception:
        import traceback
        customer = StripeCustomer(
            order_total_hours,
            total_price,
            unit_price,
            order_package,
            order_installments,
            order_crm_deal_id,
            order_extra_student,
            order_discount,
            order_stripe_customer_id,
            order_email,
            order_name,
            upsell
        )
        customer.crm_log_error("FEJL: Fakturen blev ikke oprettet!")
        print(traceback.format_exc())
        return {400: f"Bad request: error in body: {traceback.format_exc()}"}


@orders.route('/order/<int:id>', methods=['GET'])
@authenticate(token_auth)
@response(order_schema, 201)
@other_responses({404: 'Order not found'})
def get(id):
    """Retrieve a order by id"""
    order = Order.get_order_by_id(id) or abort(404)
    print(order.to_dict())
    return order.to_dict()


@orders.route('/order', methods=['GET'])
@authenticate(admin_auth)
@paginated_response(schema=orders_schema)
def all():
    """Retrieve all orders"""
    return Order.query


@orders.route('/orders_customer/<int:id>', methods=['GET'])
@limit_user_to_own_routes_decorator
@authenticate(token_auth)
@paginated_response(schema=orders_schema)
def all_customer_orders(id):
    """Retrieve all customer orders"""
    return Order.query.filter_by(customer_id=id)


@orders.route('/all_inactive_orders', methods=['GET'])
@authenticate(token_auth)
@response(OrderSchema(many=True), 201)
def all_inactive_orders():
    """Retrieve all inactive orders"""
    return Order.get_inactive_orders()


@orders.route('/update_orders', methods=['PUT'])
@authenticate(admin_auth)
@response(OrderSchema(), 201)
@body(UpdateOrderSchema())
def put_order(data):
    """Edit orders information
     Fields given get updated all other ones don't"""
    order = Order.update_order(**data)
    if 'email_sent' in data.keys():
        order_send_email = data['email_sent']
    else:
        order_send_email = None
    if order_send_email:
        send_email([order.customer.user.email], "Din TopTutors ordre",
                   render_template("email/invoice.html", url=order.stripe_url))
    return order.to_dict()


@orders.route('send_order_email', methods=['POST'])
@authenticate(admin_auth)
@response(OrderSchema(), 201)
@body(VoidOrderSchema())
def send_order_email(data):
    """Send the order email again to the customer"""
    order = Order.get_order_by_id(data['id'])
    send_email([order.customer.user.email],
               "Din TopTutors ordre",
               render_template("email/invoice.html", url=order.stripe_url))
    return order.to_dict()


@orders.route('/void_order', methods=['PUT'])
@authenticate(admin_auth)
@response(OrderSchema(), 201)
@body(VoidOrderSchema())
def void_order(data):
    """Makes an order void"""
    void_data = {'uid': data['id'], 'status': 'void'}
    order = Order.update_order(**void_data)
    # reduce the balance by the total order price and hours
    if order.balance:
        Balance.void_order(order)
    return order


@orders.route('/order/<int:id>', methods=['DELETE'])
@authenticate(admin_auth)
@response(order_schema)
@other_responses({404: 'order not found'})
def delete_order(id):
    """Delete a order by id"""
    order = Order.delete_order(id) or abort(404)
    return order
