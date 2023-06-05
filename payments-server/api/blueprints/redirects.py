from flask import Blueprint, redirect, url_for

redirects = Blueprint('redirects', __name__)


@redirects.route("/bliv-topTutor", strict_slashes=False)
@redirects.route("/job", strict_slashes=False)
def redirect_bliv_tutor():
    return redirect(url_for("main.bliv_tutor"), code=301)


@redirects.route("/tak-for-ansøgning", strict_slashes=False)
def redirect_bliv_tutor_confirmation():
    return redirect(url_for("main.conformation_tutor_application"), code=301)


@redirects.route("/ansøg", strict_slashes=False)
def job_redirect():
    return redirect("https://toptutors.teachworks.com/form/bliv-toptutor")


@redirects.route("/nykode", strict_slashes=False)
def nykode_redirect():
    return redirect("https://toptutors.teachworks.com/accounts/password/new")


@redirects.route("/lektiehjælper", strict_slashes=False)
@redirects.route("/lektiehjælper/<keyword>", strict_slashes=False)
@redirects.route("/lektiehjælper/<keyword>/<keyword2>", strict_slashes=False)
@redirects.route("/lektiehjælp/<keyword>/<keyword2>", strict_slashes=False)
def seopage_lektiehjælper(keyword=None, keyword2=None):
    if keyword is None:
        return redirect(url_for("main.lektiehjælp_page"), code=301)
    else:
        return redirect(f"/lektiehjælp/{keyword}", code=301)


@redirects.route("/hjælp", strict_slashes=False)
@redirects.route("/hjælp/<keyword>", strict_slashes=False)
@redirects.route("/hjælp/<keyword>/<keyword2>", strict_slashes=False)
def seopage_hjælp(keyword=None, keyword2=None):
    if keyword is None:
        return redirect(url_for("main.lektiehjælp_page"), code=301)
    else:
        return redirect(f"/lektiehjælp/{keyword}", code=301)


@redirects.route("/privatundervisning", strict_slashes=False)
@redirects.route("/privatundervisning/<keyword>", strict_slashes=False)
@redirects.route("/privatundervisning/<keyword>/<keyword2>", strict_slashes=False)
def seopage_privatundervisning(keyword=None, keyword2=None):
    if keyword is None:
        return redirect(url_for("main.lektiehjælp_page"), code=301)
    else:
        return redirect(f"/lektiehjælp/{keyword}", code=301)


@redirects.route("/større-opgaver", strict_slashes=False)
def seopage_opgaver():
    return redirect(url_for("main.seopage_srp"), code=301)


@redirects.route("/undervisning", strict_slashes=False)
@redirects.route("/undervisning/<keyword>", strict_slashes=False)
@redirects.route("/undervisning/<keyword>/<keyword2>", strict_slashes=False)
def seopages_undervisning(keyword=None, keyword2=None):
    if keyword is None:
        return redirect(url_for("main.lektiehjælp_page"), code=301)
    else:
        return redirect(f"/lektiehjælp/{keyword}", code=301)


@redirects.route("/tutor", strict_slashes=False)
@redirects.route("/tutor/<keyword>", strict_slashes=False)
@redirects.route("/tutor/<keyword>/<keyword2>", strict_slashes=False)
def seopage_tutor(keyword=None, keyword2=None):
    if keyword is None:
        return redirect(url_for("main.lektiehjælp_page"), code=301)
    else:
        return redirect(f"/lektiehjælp/{keyword}", code=301)


@redirects.route("/mentor", strict_slashes=False)
@redirects.route("/mentor/<keyword>", strict_slashes=False)
@redirects.route("/mentor/<keyword>/<keyword2>", strict_slashes=False)
def seopage_mentor(keyword=None, keyword2=None):
    if keyword is None:
        return redirect(url_for("main.lektiehjælp_page"), code=301)
    else:
        return redirect(f"/lektiehjælp/{keyword}", code=301)


@redirects.route("/privatunderviser", strict_slashes=False)
@redirects.route("/privatunderviser/<keyword>", strict_slashes=False)
@redirects.route("/privatunderviser/<keyword>/<keyword2>", strict_slashes=False)
def seopages_privatunderviser(keyword=None, keyword2=None):
    if keyword is None:
        return redirect(url_for("main.lektiehjælp_page"), code=301)
    else:
        return redirect(f"/lektiehjælp/{keyword}", code=301)


@redirects.route("/eksamenshjælp/<keyword>", strict_slashes=False)
@redirects.route("/eksamenshjælp/<keyword>/<keyword2>", strict_slashes=False)
def seopage_eksamen(keyword=None, keyword2=None):
    if keyword is None:
        return redirect(url_for("main.lektiehjælp_page"), code=301)
    else:
        return redirect(f"/lektiehjælp/{keyword}", code=301)


@redirects.route("/afleveringshjælp", strict_slashes=False)
@redirects.route("/afleveringshjælp/<keyword>", strict_slashes=False)
@redirects.route("/afleveringshjælp/<keyword>/<keyword2>", strict_slashes=False)
def seopage_aflevering(keyword=None, keyword2=None):
    if keyword is None:
        return redirect(url_for("main.lektiehjælp_page"), code=301)
    else:
        return redirect(f"/lektiehjælp/{keyword}", code=301)


@redirects.route("/folkeskole", strict_slashes=False)
def folkeskole_redirect():
    return redirect(url_for("main.folkeskole"), code=301)


@redirects.route("/gymnasiet", strict_slashes=False)
def gymnasiet_redirect():
    return redirect(url_for("main.gymnasiet"), code=301)


@redirects.route("/folkeskole/<keyword>", strict_slashes=False)
@redirects.route("/gymnasiet/<keyword>", strict_slashes=False)
def redirect_keyword(keyword):  # redirect these pages.
    return redirect(f"/lektiehjælp/{keyword}", code=301)


@redirects.route("/logind")
@redirects.route("/tutors")
@redirects.route("/tutor-logind")
@redirects.route("/tutor-login")  # teachworks login
def redirect_tw_login():  # redirect these pages.
    return redirect(url_for("login"), code=301)
