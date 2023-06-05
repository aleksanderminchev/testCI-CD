from werkzeug.urls import url_parse
from flask import Blueprint, redirect, url_for, render_template, request, flash
from flask_login import current_user, login_user, logout_user, login_required

from models.user import User
from api.utils.utils import check_captcha

logins = Blueprint('logins', __name__)


@logins.route("/admin-login", methods=["GET", "POST"], strict_slashes=False)
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    else:
        if request.method == "GET":
            return render_template("login.html")

        email = request.form["email"].lower()
        password = request.form["password"]

        human = check_captcha(request)
        if not human:
            flash("Bad Captcha. Prøv igen eller tag kontakt os.")
            return redirect(url_for("login"))

        user = User.get_user(email, password)

        if user is None:
            flash("Brugernavn eller adgangskoden er forkert. Prøv igen.")
            return redirect(url_for("login"))
        else:
            login_user(user, remember=True)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('main.index')
            return redirect(next_page)
        # flash('Logged in successfully')


@logins.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@logins.route("/apikey", methods=["GET"])
@login_required
def show_apikey():
    """
    Checks if logged in user is admin.
    If so it show api key else it redirects them to the login page.
    """
    if current_user.is_admin:
        apikey = current_user.generate_jwt_auth_token()
        return render_template("api_html/apikey.html", apikey=apikey)
    return redirect(url_for("main.index"))
