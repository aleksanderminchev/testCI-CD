import boto3
from decouple import config
from botocore.exceptions import ClientError

SENDER = config("AWS_SES_SENDER")
CONFIG_NAME = config("CONFIG_NAME")
CHARSET = "UTF-8"

client = boto3.client("ses", region_name="us-east-2", aws_access_key_id=config('AWS_ACCESS_KEY'), aws_secret_access_key=config('AWS_SECRET_KEY'))


def send_email(to_list, subject, template):
    """Sends an email.
    to_list is a list of strings of mail addresses.
    """
    if CONFIG_NAME != 'testing':
        try:
            response = client.send_email(
                Destination={"ToAddresses": to_list},
                Message={
                    "Body": {
                        "Html": {
                            "Charset": CHARSET,
                            "Data": template,
                        },
                    },
                    "Subject": {"Charset": CHARSET, "Data": subject},
                },
                Source=f"TopTutors <{SENDER}>",
            )
        except ClientError as e:
            print(e.response["Error"]["Message"])
        else:
            print("Email sent! Message ID:"),
            print(response["MessageId"])


def send_error_mail_to_admin(
    error, subject="UNKOWN ERROR IN WEB APP", config_name="production"
):
    """Sends an email to admins."""
    if config_name == "production":
        to = "elmar@toptutors.dk"
    else:
        to = config("ADMIN_TEST_EMAIL")

    try:
        response = client.send_email(
            Destination={"ToAddresses": [to]},
            Message={
                "Body": {
                    "Html": {
                        "Charset": CHARSET,
                        "Data": error,
                    },
                },
                "Subject": {"Charset": CHARSET, "Data": subject},
            },
            Source=f"TopTutors <{SENDER}>",
        )
    except ClientError as e:
        print(e.response["Error"]["Message"])
    # else:
        # print("Email sent! Message ID:"),
        # print(response["MessageId"])
