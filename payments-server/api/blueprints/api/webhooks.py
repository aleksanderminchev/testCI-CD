from flask import Blueprint
# Internal imports
from api.email import send_error_mail_to_admin
from api.services.stripe_api import handle_stripe_webhook


webhooks = Blueprint('webhooks', __name__)


# STRIPE SUBSCRIPTION EVENTS
@webhooks.route("/stripewebhook", methods=["POST"])
def stripe_webhook():
    try:
        handle_stripe_webhook()
    except Exception as e:
        send_error_mail_to_admin(
            error="Stripe Webhook Error"
            + str(e),
            subject="⚠️ STRIPE API Webhook Error",
        )
    return dict(success=True)
