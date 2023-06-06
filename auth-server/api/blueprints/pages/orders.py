from flask import Blueprint, render_template, redirect

from models.order import Order
from api.utils.routes_utils import render_page_404
from api.utils.stripe_utils import get_order_info, stripe
from api.utils.utils import get_date

orders = Blueprint('orders', __name__)


@orders.route("/<uid>", methods=["GET"])
def show_order(uid):
    """Show order overview for order page"""
    try:
        order = Order.get_by_hashed_id(uid)
        unit_fee_extra_student, unit_price, unit_discount, discount_percentage, per_rate_price, monthly_fee_extra_student, price_per_month = get_order_info(
            order)

        return render_template(
            "order/order.html",
            order=order,
            unit_fee_extra_student=unit_fee_extra_student,
            unit_price=unit_price,
            unit_discount=unit_discount,
            discount_percentage=discount_percentage,
            per_rate_price=per_rate_price,
            monthly_fee_extra_student=monthly_fee_extra_student,
            price_per_month=price_per_month
        )
    except Exception:
        import traceback
        print(traceback.format_exc())
        return render_page_404()


@orders.route("/pay/<uid>", methods=["GET"])
def pay_order(uid):
    """ Creates the stripe payment link based on the specific order data. """
    try:
        order = Order.get_by_hashed_id(uid)
        # If a order with given hash ID from the URL exists.
        if order.hashed_id and order.active is True:
            # Check if it's a one time payment or a reccuring subscription
            if "single-" in order.package:
                mode = "payment"
                line_items = [{"price": order.package,
                               "quantity": order.total_hours}]
            elif order.package[:-4] == "1-months":
                mode = "payment"
                line_items = [{"price": order.package, "quantity": 1}]
            else:
                mode = "subscription"
                line_items = [{"price": order.package, "quantity": 1}]

            if order.discount == "5":
                coupon = "5-percent"
            elif order.discount == "10":
                coupon = "10-percent"
            elif order.discount == "15":
                coupon = "15-percent"
            elif order.discount == "20":
                coupon = "20-percent"
            else:
                coupon = order.discount

            # If there are extra students we add the charge.
            if order.extra_student is not None:
                # we calculate the extra student fee and time it with 100, because that's how Stripe wants it.
                extra_student_fee = round(
                    order.total_hours * 50 * order.extra_student / order.installments, 2) * 100
                # Based on the student fee we create a new stripe object.
                new_extra_student_fee = stripe.Price.create(
                    unit_amount=int(extra_student_fee),
                    currency="dkk",
                    product="prod_MH2jgQTbIKPMUO",
                    recurring={"interval": "month"},
                )
                line_items.append(
                    {"price": new_extra_student_fee["id"], "quantity": 1})

            checkout_session = stripe.checkout.Session.create(
                success_url=f"https://localhost:5000/order/confirmation/{uid}",
                cancel_url=f"https://localhost:5000/order/{uid}",
                customer=order.stripe_customer_id,
                line_items=line_items,
                metadata={
                    "uid": order.hashed_id,
                },
                billing_address_collection="required",
                mode=mode,
                discounts=[{
                    'coupon': coupon,
                }],
            )
        else:
            # order is already paid, so we redirect them to the order page.
            return redirect(f"/order/{uid}")
    except Exception as e:
        print(e)
        return redirect(f"/order/{uid}")

    return redirect(checkout_session.url, code=303)


@orders.route("/confirmation/<uid>", methods=["GET"])
def order_recieved(uid):
    order = Order.get_by_hashed_id(uid)
    if order.active:
        return redirect(f"/order/{uid}")
    return render_template("order/confirmation.html", order=order)


@orders.route("/customer/<id>", methods=["GET"])
def customer_portal(id):
    """ Must be Stripe customer id without the "cus_" prefix. """
    try:
        customer = stripe.Customer.retrieve("cus_" + id)
        print(customer.email)
        if customer["id"] is not None:
            session = stripe.billing_portal.Session.create(
                customer=customer["id"],
                return_url='https://localhost:5000',
            )
        return redirect(session.url)
    except Exception as e:
        print(e)
        return render_page_404()
