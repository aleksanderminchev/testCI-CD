import stripe
import requests
import locale

from decouple import config
from flask import jsonify

locale.setlocale(locale.LC_ALL, 'da_DK')
stripe.api_key = config("STRIPE_TEST_API")
endpoint_secret = config("STRIPE_ENDPOINT_SECRET_DEV")


class StripeCustomer:
    def __init__(self, total_hours, total_price, unit_price, package, installments, crm_deal_id, extra_student, discount=None, stripe_customer_id=None, email=None, name=None, upsell=None):
        self.total_hours = total_hours
        self.total_price = total_price
        self.unit_price = unit_price
        self.package = package
        self.installments = installments
        self.crm_deal_id = crm_deal_id
        self.extra_student = extra_student
        self.discount = discount
        self.stripe_customer_id = stripe_customer_id
        self.email = email
        self.name = name
        self.upsell = upsell

    def get_customer_id(self):
        """ Get the customer id with same email or create new customer."""
        customer = stripe.Customer.list(email=self.email)
        # if no stripe account with said mail exists then craete one.
        if len(customer["data"]) == 0:
            customer_id = stripe.Customer.create(
                email=self.email, name=self.name)
            customer_id = customer_id["id"]
            self.update_stripe_url_on_crm()
        # else just take the first stripe account and use that from now on.
        else:
            customer_id = customer["data"][0]["id"]

        # update the objects stripe_id
        self.stripe_customer_id = customer_id
        return customer_id

    @staticmethod
    def get_email_by_id(customer_id):
        customer = stripe.Customer.retrieve(customer_id)
        return customer.email

    @staticmethod
    def get_total_package_price(package, total_hours):
        """ Calculates the total price for the package by taking the price per hour (from in the package string) times total hours."""
        price = int(package[-3:]) * total_hours

        return price

    @staticmethod
    def get_package_price(package):
        """ Gets the hourly price for the given package. """
        price = int(package[-3:])
        return price

    def get_duration_of_package(self):
        return self.installments

    @staticmethod
    def get_discount(discount):
        """  Use the Stripe Coupon ID to find the discount percentage. """

        if discount == "5":
            coupon = "5-percent"
        elif discount == "10":
            coupon = "10-percent"
        elif discount == "15":
            coupon = "15-percent"
        elif discount == "20":
            coupon = "20-percent"
        else:
            coupon = discount

        stripe_coupon = stripe.Coupon.retrieve(coupon)
        percentage = 100 - stripe_coupon["percent_off"]
        percentage /= 100
        return percentage

    @staticmethod
    def calculate_extra_student_fee(extra_student, total_hours, installments):
        price = total_hours / installments
        price *= 50
        price *= extra_student

        price = round(price, 2)

        amount_to_be_added = price * installments

        return amount_to_be_added

    def update_stripe_url_on_crm(self):
        """Updates the STRIPE URL on the customers CRM profile"""

        requests.post(config("ZOHO_ADD_STRIPE_ID_TO_DEAL"), params={
                      "stripe_id": self.stripe_customer_id, "crm_id": self.crm_deal_id})

    def crm_log_error(self, subject):
        """Triggers a function on crm, that adds a task to the deal, with a task."""

        requests.post(config("ZOHO_ADD_TASK_ERROR"), params={
                      "deal_id": self.crm_deal_id, "subject": subject})


def get_order_info(order):
    # Info about product
    unit_discount = 0
    unit_fee_extra_student = 0
    monthly_fee_extra_student = 0
    discount_percentage = 0
    unit_price = order.unit_price

    if order.discount:
        stripe_discount = StripeCustomer.get_discount(order.discount)
        discount_percentage = 100.0 - (stripe_discount * 100)
        unit_discount = unit_price - (unit_price * stripe_discount)
        # Round the unit prices & format it.
        unit_discount = round(unit_discount, 2)

    if order.extra_student:
        unit_fee_extra_student = 50 * order.extra_student
        monthly_fee_extra_student = order.total_hours * \
            unit_fee_extra_student / order.installments
        monthly_fee_extra_student = locale.currency(
            monthly_fee_extra_student, grouping=True, symbol=False)
        unit_fee_extra_student = locale.currency(
            unit_fee_extra_student, grouping=True, symbol=False)

    # Formatting to currency
    per_rate_price = round((unit_price - unit_discount)
                           * order.total_hours / order.installments, 2)
    price_per_month = round(order.total_price / order.installments, 2)
    price_per_month = locale.currency(
        price_per_month, grouping=True, symbol=False)
    unit_price = locale.currency(unit_price, grouping=True, symbol=False)
    per_rate_price = locale.currency(
        per_rate_price, grouping=True, symbol=False)
    unit_discount = locale.currency(unit_discount, grouping=True, symbol=False)

    return unit_fee_extra_student, unit_price, unit_discount, discount_percentage, per_rate_price, monthly_fee_extra_student, price_per_month


def requestRefund(stripe_id):
    try:
        print(stripe_id)
        stripe.Refund.create(payment_intent=stripe_id)
    except Exception as e:
        print(e)
        return jsonify(error=500, text=str(e)), 500
