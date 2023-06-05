
import requests
import json
import stripe
import datetime
import time

from dateutil.relativedelta import relativedelta
from flask import render_template, request, jsonify
from decouple import config

from api.email import send_email, send_error_mail_to_admin
from models.order import Order
from models.transaction import Transaction
from models.customer import Customer
from models.balance import Balance
from api.services.tw.tw_headers import tw_headers
from api.utils.utils import get_date
from api.app import db
from ..utils.stripe_utils import StripeCustomer


if config("CONFIG_NAME") == "production":
    stripe.api_key = config("STRIPE_LIVE_API")
    endpoint_secret = config("STRIPE_ENDPOINT_SECRET")
else:
    stripe.api_key = config("STRIPE_TEST_API")
    endpoint_secret = config("STRIPE_ENDPOINT_SECRET_DEV")


def fetch_stripe_info(event, is_subscription):
    """Retrieves customer data from a stripe event
    :param event: stripe event object
    :param: is_subscription: bool
    :returns: dict containing: name, email, phone,
    :product, currency, amount, date, subscription, stripe_id
    :rtype: dict
    """
    customer = event["data"]["object"]["customer"]
    customer_data = stripe.Customer.retrieve(customer)
    customer_phone = customer_data["phone"]
    customer_email = customer_data["email"]
    customer_name = customer_data["name"]
    payment_amount = None
    amount_formatted = None

    if event["object"] != "subscription_schedule":
        payment_amount = event["data"]["object"]["amount_paid"]
        # we receive the amount as one long integer not double, fx. 1500 instead of 15.00
        # here we inrt a "." before the last two indexes
        amount_formatted = str(payment_amount)[
            :-2] + "." + str(payment_amount)[-2:]

    product = event["data"]["object"]["lines"]["data"][0]["price"]["product"]
    currency = event["data"]["object"]["lines"]["data"][0]["currency"]

    date = datetime.datetime.now()
    date = f"{date.day}/{date.month}/{date.year}"
    stripe_id = event["data"]["object"]["payment_intent"]
    subscription = "one_time"

    if is_subscription:
        subscription = "subscription"

    return {
        "name": customer_name,
        "email": customer_email,
        "phone": customer_phone,
        "product": product,
        "currency": currency,
        "amount": amount_formatted,
        "date": date,
        "subscription": subscription,
        "stripe_id": stripe_id,
    }


def fetch_stripe_info_refund(event, is_subscription):
    """Retrieves customer data from a stripe event
    :param event: stripe event object
    :param: is_subscription: bool
    :returns: dict containing: name, email, phone,
    :product, currency, amount, date, subscription, stripe_id
    :rtype: dict
    """
    customer = event["data"]["object"]["customer"]
    customer_data = stripe.Customer.retrieve(customer)
    customer_phone = customer_data["phone"]
    customer_email = customer_data["email"]
    customer_name = customer_data["name"]
    payment_amount = event["data"]["object"]["amount_refunded"]
    # we receive the amount as one long integer not double, fx. 1500 instead of 15.00
    # here we inrt a "." before the last two indexes
    amount_formatted = str(payment_amount)[
        :-2] + "." + str(payment_amount)[-2:]

    product = event["data"]["object"]["refunds"]["data"][0]["object"]
    currency = event["data"]["object"]["refunds"]["data"][0]["currency"]

    date = datetime.datetime.now()
    date = f"{date.day}/{date.month}/{date.year}"
    stripe_id = event["data"]["object"]["payment_intent"]
    subscription = "one_time"

    if is_subscription:
        subscription = "subscription"

    return {
        "name": customer_name,
        "email": customer_email,
        "phone": customer_phone,
        "product": product,
        "currency": currency,
        "amount": amount_formatted,
        "date": date,
        "subscription": subscription,
        "stripe_id": stripe_id,
    }


def add_payment_to_tw(customer):
    """
    Adds payment to TW
    :param customer: dict
    :returns: json status code
    :rtype: json
    """

    # Find TW user with identical mail as received payment.
    stripe_mail = {"email": customer["email"]}
    student = requests.get(
        "https://api.teachworks.com/v1/customers",
        headers=tw_headers,
        json=stripe_mail,
    )

    n = 0
    # retry 5 times if status code is not 200
    while student.status_code != 200 and n < 5:
        n += 1
        time.sleep(3)  # try waiting and retry
        student = requests.get(
            "https://api.teachworks.com/v1/customers",
            headers=tw_headers,
            json=stripe_mail,
        )

    try:  # try to get mail
        student_tw_data = student.json()
        tw_mail = student_tw_data[0]["email"]
    except Exception as e:
        send_error_mail_to_admin(
            error="STRIPE/TW ERROR POSTING SUB PAYMENT RECEIVED TO TW."
            + "This error usually happens if the mail is not found on TW."
            + f"  Student TW Data from API request: {student.json()}"
            + f"  STATUS CODE: {student.status_code}"
            + "  Stripe customer data: "
            + str(customer)
            + "  Python Error code:"
            + str(e),
            subject="⚠️ STRIPE API ERROR: POSTING SUB PAYMENT TO TW.",
        )

    # make sure that if stripe email matches the email on TW
    if stripe_mail["email"] == tw_mail:
        # create payment on TW
        data = {
            "payment": {
                "date": customer["date"],
                "customer_id": student_tw_data[0]["id"],
                "amount": customer["amount"],
                "payment_method": "Other",
                "description": f"Stripe subscription: {customer['stripe_id']}",
            }
        }

        payment_results = requests.post(
            "https://api.teachworks.com/v1/payments",
            headers=tw_headers,
            data=json.dumps(data),
        )

        n = 0
        # retry 5 times
        while payment_results.status_code != 201 and n < 5:
            n += 1
            time.sleep(3)  # try waiting and retry
            payment_results = requests.post(
                "https://api.teachworks.com/v1/payments",
                headers=tw_headers,
                data=json.dumps(data),
            )
        if payment_results.status_code != 201:
            send_error_mail_to_admin(
                error="STRIPE/TW ERROR POSTING SUB PAYMENT RECEIVED TO TW."
                + "This error happens if the POST request of the payment to TW failed."
                + f"  Payment request Data from API request: {payment_results.json()}"
                + f"  STATUS CODE: {payment_results.status_code}"
                + "  Stripe customer data: "
                + str(customer)
                + "Passed data in Payment Request:"
                + str(data),
                subject="⚠️ Subscription payment successful, but Error inserting payment onto TW"
            )
    else:
        html_internal = render_template(
            "email/subscription-email.html", information=customer
        )
        # We didnt find a matching email with TW, notfying admins via email
        send_email(
            ["hej@toptutors.dk"],
            "⚠️ Subscription payment successful, but Email not found on TW and is not inserted to TW yet.",
            html_internal,
        )

    # has to return 200 status code or else it will give us a 500 internal server error
    return jsonify(success=True)


def handle_subscription_payment_failed(customer):
    """Notifies Toptutors that a subscription payment has failed
    :param customer: dict
    :returns: json status code
    :rtype: json
    """
    html_internal = render_template(
        "email/subscription-email.html", information=customer
    )
    subject_internal = "Subscription payment failed"
    if customer["email"] in [
        "elmarjens@gmail.com",
    ]:
        send_email(
            [customer["email"]],
            subject_internal,
            html_internal,
        )
    else:
        send_email(
            ["hej@toptutors.dk"],
            subject_internal,
            html_internal,
        )
    # has to return 200 status code or else it will give us a 500 internal server error
    return jsonify(success=True)


def handle_order(order, subscription_id):
    """ Modifies the Stripe Subscription and adds the cancel date."""

    package_month = int(order.installments)

    # Cancel date is calculated as today + monthly installments - 1 day
    today = datetime.date.today()
    cancel_date = today + relativedelta(months=package_month)
    cancel_date -= relativedelta(days=1)

    # Change cancel date to the format that Stripe wants.
    cancel_date = time.mktime(cancel_date.timetuple())
    cancel_date = int(cancel_date)

    # update the cancel date on Stripe
    stripe.Subscription.modify(subscription_id, cancel_at=cancel_date)


def handle_subscription_ended(customer):
    """Notifies Toptutors that a subscription has ended
    :param customer: dict
    :returns: json status code
    :rtype: json
    """

    html_internal = render_template(
        "email/subscription-email.html", information=customer
    )
    subject_internal = "Subscription has ended"
    if customer["email"] in [
        "elmarjens@gmail.com",
    ]:
        send_email(
            [customer["email"]],
            subject_internal,
            html_internal,
        )
    else:
        send_email(
            ["hej@toptutors.dk"],
            subject_internal,
            html_internal,
        )
    # has to return 200 status code or else it will give us a 500 internal server error
    return jsonify(success=True)


def get_customer_from_mail(email):
    """
    Gets customers Stripe data from e-mail.
    Returns
    If there are multiple results then it returns the most recent
    as the stripe api is sorted by creation date.
    See more here: https://stripe.com/docs/api/customers/list
    """
    customers = stripe.Customer.list(email=email)
    length = len(customers["data"])
    if length == 0:
        return "Mail does not exist"
    else:
        return customers["data"][0]


def handle_stripe_webhook():
    """ Handles stripe webhooks.

    Supported Stripe Events: (remember to also enable events on Stripe)
    - checkout.session.completed
    - invoice.payment_succeeded
    - charge.refunded
    """

    # Check signature is valid
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        send_error_mail_to_admin(
            error="STRIPE PAYLOAD ERROR" + str(e),
            subject="⚠️ STRIPE WEBHOOK ERROR: invalid paylod.",
        )
        print(e)
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        send_error_mail_to_admin(
            error="STRIPE SIGNATURE VERIFICATION ERROR" + str(e),
            subject="⚠️ STRIPE WEBHOOK ERROR: Invalid Stripe Signature Verification",
        )
        print(e)
        raise e

    # Handle the events
    if event['type'] == 'charge.failed' and event['data']['object']['failure_code'] != 'insufficient_funds':
        handle_payment_failed(event)

    # checkout.session.completed event
    # Updates the order in DB, Emails the customer, handles the order on Stripe, and updates the CRM.

    if event and event["type"] == "checkout.session.completed":
        try:
            # Get the needed data from the event.
            subscription_id = event["data"]["object"]["subscription"]
            uid = event["data"]["object"]["metadata"]["uid"]
            email = event["data"]["object"]["customer_details"]["email"]
            # URL for the order
            url = "https://www.toptutors.dk/order/" + str(uid)

            # Update the order
            order = Order.get_by_hashed_id(uid)
            order.update_status(False)
            order.booking_date = get_date()
            db.session.commit()

            # Send Email to Customer
            html = render_template("email/payment_completed.html", url=url)
            send_email([email], "Din TopTutors Ordre er godkendt!", html)

            # Handle the order on Stripe
            handle_order(order, subscription_id)

            if order.crm_deal_id != "":
                requests.post(config("ZOHO_PACKAGE_PAID"), params={
                              "crm_id": order.crm_deal_id, "stripe_id": order.stripe_customer_id})

            return jsonify(success=True)

        except Exception as e:
            import traceback
            send_error_mail_to_admin(
                error="STRIPE ERROR HANDLING checkout session completed. " +
                str(traceback.format_exc()),
                subject="⚠️ STRIPE WEBHOOK ERROR: checkout.session.completed.",
            )
            print(str(e))
            return jsonify(error=500, text=str(e)), 500

    # invoice.payment_succeeded event
    elif event and event["type"] == "invoice.payment_succeeded":
        # If it's a subscription type
        if event["data"]["object"]["lines"]["data"][0]["type"] == "subscription":
            try:
                # Get Customer
                customer = fetch_stripe_info(event, True)
                customer_transaction = Customer.get_customer_by_email(
                    customer['email']).customer

                # Add new transaction in DB
                transaction = Transaction.add_new_transaction(
                    type_transaction='payment',
                    customer_id=customer_transaction.id,
                    balance_id=customer_transaction.balance[0].id,
                    currency=customer['currency'].upper(),
                    amount=customer['amount'],
                    void=False,
                    method='stripe',
                    stripe_transaction_id=customer['stripe_id']
                )
                # Add transaction to the balance.
                Balance.add_transaction(
                    transaction, customer_transaction.balance[0]
                )

                # Add payment to TW
                add_payment_to_tw(customer)

            except Exception as e:
                send_error_mail_to_admin(
                    error="STRIPE ERROR HANDLING SUB PAYMENT RECEIVED." +
                    str(e),
                    subject="⚠️ STRIPE API ERROR: HANDLING SUB PAYMENT.",
                )
                return jsonify(error=500, text=str(e)), 500

    # charge.refunded event
    elif event and event["type"] == "charge.refunded":
        try:
            # Get Customer
            customer = fetch_stripe_info_refund(event, False)
            customer_transaction = Customer.get_customer_by_email(
                customer['email']).customer

            # Add Transaction
            transaction = Transaction.add_new_transaction(
                type_transaction='refund',
                customer_id=customer_transaction.id,
                balance_id=customer_transaction.balance[0].id,
                currency=customer['currency'].upper(),
                amount=customer['amount'],
                void=False,
                method='stripe',
                stripe_transaction_id=customer['stripe_id']
            )

            # Add transaction to balance
            Balance.add_transaction(
                transaction, customer_transaction.balance[0])

        except Exception as e:
            send_error_mail_to_admin(
                error="STRIPE ERROR: Type charge.refunded" +
                str(e),
                subject="⚠️ STRIPE API ERROR: HANDLING REFUND EVENT.",
            )
            return jsonify(error=500, text=str(e)), 500
    else:
        send_error_mail_to_admin(
            error="Unhandled event type {}".format(event["type"]),
            subject="⚠️ STRIPE API ERROR: Unhandled event type.",
        )
        return jsonify(error=500, text=str("ERROR")), 500
    return jsonify(success=True)

def handle_payment_failed(event):
    # Handle the logic for an expired card charge failure event

    # Access the relevant information from the event
    charge_id = event['data']['object']['id']
    customer_id = event['data']['object']['customer']

    # Perform the necessary actions
    send_notification_to_customer(charge_id, customer_id)

def send_notification_to_customer(charge_id, customer_id):
    # Replace with your notification logic
    customer_email = StripeCustomer.get_email_by_id(customer_id)
    print(customer_email)
    #send_email([email], "Din TopTutors Ordre er godkendt!", html) # TODO 

