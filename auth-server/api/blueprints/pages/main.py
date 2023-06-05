from flask import Blueprint, render_template, current_app, request, redirect, url_for, flash, session
from sqlalchemy.sql.expression import func

from api import db  # type: ignore
from models.tutor import Tutor
from models.teacher import Teacher, TeacherStatus
from models.subjects import Subjects
from models.contactformleads import ContactFormLead
from api.email import send_email
from api.services import zoho_crm, ghost_api, partner_ads, meta_ads
from api.utils.utils import check_captcha
from api.utils.routes_utils import process_phonelead_form, seopage

from api.utils.keywords import SEO_SUBJECTS


main = Blueprint('main', __name__)


@main.route("/", methods=["GET", "POST"])
def index():
    """
    The Index page
    """
    if request.method == "GET":
        return render_template("index.html", opening_hours=True)
    return process_phonelead_form(request)


@main.route("/priser", methods=["GET", "POST"], strict_slashes=False)
def priser():
    if request.method == "GET":
        return render_template("priser.html", opening_hours=True)
    return process_phonelead_form(request)


@main.route("/om-os", strict_slashes=False)  # about page
def about_page():
    return render_template("about.html", opening_hours=True)


@main.route("/bliv-tutor", strict_slashes=False)
def bliv_tutor():
    return render_template("bliv-topTutor.html", opening_hours=True)


@main.route("/betingelser", strict_slashes=False)  # terms of service
def terms():
    return render_template("terms.html", opening_hours=True)


@main.route("/privatlivspolitik", strict_slashes=False)  # privacy policy
def privacy():
    return render_template("privacy.html", opening_hours=True)


@main.route("/succes", strict_slashes=False)
def conformation_tutor_application():

    if current_app.config.get("ENV_NAME") == "production":
        user_data = {"client_ip_address": request.remote_addr,
                     "client_user_agent": request.headers.get('User-Agent')}

        # Get fbc
        if "_fbc" in request.cookies:
            user_data["fbc"] = request.cookies.get("_fbc")
        # Get fbp
        if "_fbp" in request.cookies:
            user_data["fbp"] = request.cookies.get("_fbp")

        current_app.task_queue.enqueue_call(  # type:ignore
            func=meta_ads.add_event,
            args=("SubmitApplication", user_data, ""),
            result_ttl=5000,
        )
    return render_template("confirmation-tutor.html", opening_hours=True)


@main.route("/tak", strict_slashes=False)  # form confirmation
def confirmation():
    try:
        email = session["form_email"]
    except Exception:
        email = ""

    try:
        phone = session["form_phone"]
    except Exception:
        phone = ""

    return render_template("confirmation.html", email=email, phone=phone, opening_hours=True)


@main.route("/lektiehjælp", strict_slashes=False)
def lektiehjælp_page():
    desc = "Få den helt rette lektiehjælper, der øger din motivation, faglighed og selvtillid i skolen."
    tutor_list = Teacher.query.filter(Teacher.photo != "", Teacher.bio != "", Teacher.status ==
                                      TeacherStatus.ACTIVE, Teacher.marketing_consent == "True").order_by(func.random()).limit(15).all()
    return render_template(
        "seo_pages/lektiehjælp.html", mainword="Lektiehjælp", desc=desc, subject_city_class="", synonynom="tutor", synonynom_plural="tutors", tutor_list=tutor_list, opening_hours=True,
    )


@main.route("/lektiehjælp/matematik", strict_slashes=False)
def matematik():
    tutor_list = Teacher.query.join(Teacher.subjects).filter(
        Subjects.name.like("%Math%"),
        Teacher.photo != "",
        Teacher.bio != "",
        Teacher.status == TeacherStatus.ACTIVE,
        Teacher.marketing_consent == True
    ).order_by(func.random()).limit(15).all()

    keyword = "matematik"
    desc = "Knæk koden i matematik med en engageret tutor, der hjælper med at gøre komplekse koncepter enkle. Prøv en gratis lektion i dag."

    return render_template(
        "seo_pages/matematik.html",
        subject=keyword,
        mainword=f"Lektiehjælp i {keyword}",
        desc=desc,
        subject_city_class="i " + keyword,
        synonynom="lektiehjælper",
        synonynom_plural="lektiehjælpere",
        tutor_list=tutor_list,
        opening_hours=True,
    )


@main.route("/lektiehjælp/dansk", strict_slashes=False)
def dansk():
    tutor_list = Teacher.query.join(Teacher.subjects).filter(
        Subjects.name.like("%Dansk%"),
        Teacher.photo != "",
        Teacher.bio != "",
        Teacher.status == TeacherStatus.ACTIVE,
        Teacher.marketing_consent == True
    ).order_by(func.random()).limit(15).all()

    keyword = "dansk"
    desc = f"Styrk dine danske sprog- og skrivefærdigheder med en personlig tutor. Tilmeld dig og få en gratis prøvetime i dag."

    return render_template(
        "seo_pages/dansk.html",
        subject=keyword,
        mainword=f"Lektiehjælp i {keyword}",
        desc=desc,
        subject_city_class="i " + keyword,
        synonynom="lektiehjælper",
        synonynom_plural="lektiehjælpere",
        tutor_list=tutor_list,
        opening_hours=True
    )


@main.route("/lektiehjælp/engelsk", strict_slashes=False)
def engelsk():
    tutor_list = Teacher.query.join(Teacher.subjects).filter(
        Subjects.name.like("%Engelsk%"),
        Teacher.photo != "",
        Teacher.bio != "",
        Teacher.status == TeacherStatus.ACTIVE,
        Teacher.marketing_consent == True
    ).order_by(func.random()).limit(15).all()

    keyword = "engelsk"
    desc = "Boost dine engelsk sprogfærdigheder med en tutor, der imødekommer dine unikke behov. Start i dag med en gratis prøvetime."
    return render_template(
        "seo_pages/engelsk.html",
        subject=keyword,
        mainword=f"Lektiehjælp i {keyword}",
        desc=desc,
        subject_city_class="i " + keyword,
        synonynom="lektiehjælper",
        synonynom_plural="lektiehjælpere",
        tutor_list=tutor_list,
        opening_hours=True,
    )


@main.route("/lektiehjælp/tysk", strict_slashes=False)
def tysk():
    tutor_list = Teacher.query.join(Teacher.subjects).filter(
        Subjects.name.like("%Tysk%"),
        Teacher.photo != "",
        Teacher.bio != "",
        Teacher.status == TeacherStatus.ACTIVE,
        Teacher.marketing_consent == True
    ).order_by(func.random()).limit(15).all()

    keyword = "tysk"
    desc = f"Lær tysk med en engageret tutor, der fokuserer på dine behov, mål og intresser. Start med en gratis prøvetime i dag."

    return render_template(
        "seo_pages/tysk.html",
        subject=keyword,
        mainword=f"Lektiehjælp i {keyword}",
        desc=desc,
        subject_city_class="i " + keyword,
        synonynom="lektiehjælper",
        synonynom_plural="lektiehjælpere",
        tutor_list=tutor_list,
        opening_hours=True,
    )


@main.route("/lektiehjælp/billedkunst", strict_slashes=False)
def billedkunst():
    tutor_list = Teacher.query.join(Teacher.subjects).filter(
        Subjects.name.like("%Billedkunst%"),
        Teacher.photo != "",
        Teacher.bio != "",
        Teacher.status == TeacherStatus.ACTIVE,
        Teacher.marketing_consent == True
    ).order_by(func.random()).limit(15).all()

    keyword = "billedkunst"
    desc = "Lær billedkunstens teknikker og teorier med en erfaren tutor, der tilpasser undervisningen til dine mål. Tilmeld dig en gratis prøvetime."

    return render_template(
        "seo_pages/billedkunst.html",
        subject=keyword,
        mainword=f"Lektiehjælp i {keyword}",
        desc=desc,
        subject_city_class="i " + keyword,
        synonynom="lektiehjælper",
        synonynom_plural="lektiehjælpere",
        tutor_list=tutor_list,
        opening_hours=True,
    )


@main.route("/lektiehjælp/fransk", strict_slashes=False)
def fransk():
    tutor_list = Teacher.query.join(Teacher.subjects).filter(
        Subjects.name.like("%Fransk%"),
        Teacher.photo != "",
        Teacher.bio != "",
        Teacher.status == TeacherStatus.ACTIVE,
        Teacher.marketing_consent == True
    ).order_by(func.random()).limit(15).all()

    keyword = "fransk"
    desc = "Forbedr dine franske sprogfærdigheder og udforsk kulturen med en engageret tutor. Book en gratis prøvetime nu."

    return render_template(
        "seo_pages/fransk.html",
        subject=keyword,
        mainword=f"Lektiehjælp i {keyword}",
        desc=desc,
        subject_city_class="i " + keyword,
        synonynom="lektiehjælper",
        synonynom_plural="lektiehjælpere",
        tutor_list=tutor_list,
        opening_hours=True,
    )


@main.route("/lektiehjælp/spansk", strict_slashes=False)
def spansk():
    tutor_list = Teacher.query.join(Teacher.subjects).filter(
        Subjects.name.like("%Spansk%"),
        Teacher.photo != "",
        Teacher.bio != "",
        Teacher.status == TeacherStatus.ACTIVE,
        Teacher.marketing_consent == True
    ).order_by(func.random()).limit(15).all()

    keyword = "spansk"
    desc = "Bliv bedre til spansk og fordyb dig i sproget og kulturen med en engageret tutor, der imødekommer dine unikke behov. Start i dag med en gratis prøvetime."

    return render_template(
        "seo_pages/spansk.html",
        subject=keyword,
        mainword=f"Lektiehjælp i {keyword}",
        desc=desc,
        subject_city_class="i " + keyword,
        synonynom="lektiehjælper",
        synonynom_plural="lektiehjælpere",
        tutor_list=tutor_list,
        opening_hours=True,
    )


@main.route("/lektiehjælp/samfundsfag", strict_slashes=False)
def samfundsfafg():
    tutor_list = Teacher.query.join(Teacher.subjects).filter(
        Subjects.name.like("%Samfundsfag%"),
        Teacher.photo != "",
        Teacher.bio != "",
        Teacher.status == TeacherStatus.ACTIVE,
        Teacher.marketing_consent == True
    ).order_by(func.random()).limit(15).all()

    keyword = "samfundsfag"
    desc = "Få bedre styr på samfundsfag og få en bedre forståelse af politik, økonomi og kultur med skræddersyet lektiehjælp. Book en gratis prøvetime i dag."

    return render_template(
        "seo_pages/samfundsfag.html",
        subject=keyword,
        mainword=f"Lektiehjælp i {keyword}",
        desc=desc,
        subject_city_class="i " + keyword,
        synonynom="lektiehjælper",
        synonynom_plural="lektiehjælpere",
        tutor_list=tutor_list,
        opening_hours=True,
    )


@main.route("/lektiehjælp/virksomhedsøkonomi", strict_slashes=False)
def virksomhedsøkonomi():
    tutor_list = Teacher.query.join(Teacher.subjects).filter(
        Subjects.name.like("%Virksomhedsøkonomi%"),
        Teacher.photo != "",
        Teacher.bio != "",
        Teacher.status == TeacherStatus.ACTIVE,
        Teacher.marketing_consent == True
    ).order_by(func.random()).limit(15).all()

    keyword = "virksomhedsøkonomi"
    desc = "Få bedre styr på virksomhedsøkonomi fra en erfaren tutor, der tilpasser undervisningen til dine mål og behov. Tilmeld dig en gratis prøvetime i dag."

    return render_template(
        "seo_pages/virksomhedsoko.html",
        subject=keyword,
        mainword=f"Lektiehjælp i {keyword}",
        desc=desc,
        subject_city_class="i " + keyword,
        synonynom="lektiehjælper",
        synonynom_plural="lektiehjælpere",
        tutor_list=tutor_list,
        opening_hours=True,
    )


# @main.route("/lektiehjælp/virksomhedsøkonomi", strict_slashes=False)
# def virksomhedsøkonomi():
#     tutor_list = Tutor.query.filter(
#             Tutor.subjects.contains("Virksomhedsøkonomi"),
#             Tutor.photo != "",
#             Tutor.bio != "",
#             Tutor.status == "Active",
#             Tutor.marketing_consent == "True"
#         ).order_by(func.random()).limit(15).all()

#     keyword = "virksomhedsøkonomi"
#     desc = f"Vi har lektiehjælpere, der kan hjælpe i {keyword}."

#     return render_template(
#             "seo_pages/virksomhedsoko.html",
#             subject=keyword,
#             mainword=f"Lektiehjælp i {keyword}",
#             desc=desc,
#             subject_city_class="i " + keyword,
#             synonynom="lektiehjælper",
#             synonynom_plural="lektiehjælpere",
#             tutor_list=tutor_list
#         )


@main.route("/lektiehjælp/fysik-kemi", strict_slashes=False)
def fysikKemi():
    tutor_list = Teacher.query.join(Teacher.subjects).filter(
        Subjects.name.like("%Fysik-Kemi%"),
        Teacher.photo != "",
        Teacher.bio != "",
        Teacher.status == TeacherStatus.ACTIVE,
        Teacher.marketing_consent == True
    ).order_by(func.random()).limit(15).all()

    keyword = "fysik/kemi"
    desc = f"Få styr på fysik-kemi med en tutor, der tilpasser udervisningen til dine mål. Start med en gratis prøvetime i dag."

    return render_template(
        "seo_pages/fysik-kemi.html",
        subject=keyword,
        mainword=f"Lektiehjælp i {keyword}",
        desc=desc,
        subject_city_class="i " + keyword,
        synonynom="lektiehjælper",
        synonynom_plural="lektiehjælpere",
        tutor_list=tutor_list,
        opening_hours=True,
    )


@main.route("/lektiehjælp/biologi", strict_slashes=False)
def biologi():
    tutor_list = Teacher.query.join(Teacher.subjects).filter(
        Subjects.name.like("%Biologi%"),
        Teacher.photo != "",
        Teacher.bio != "",
        Teacher.status == TeacherStatus.ACTIVE,
        Teacher.marketing_consent == True
    ).order_by(func.random()).limit(15).all()

    keyword = "biologi"
    desc = "Boost dine færdigheder i biologi med en Top Tutor, der hjælper dig med at få bedre styr de komplekse emner. Start med en gratis prøvetime."

    return render_template(
        "seo_pages/biologi.html",
        subject=keyword,
        mainword=f"Lektiehjælp i {keyword}",
        desc=desc,
        subject_city_class="i " + keyword,
        synonynom="lektiehjælper",
        synonynom_plural="lektiehjælpere",
        tutor_list=tutor_list,
        opening_hours=True,
    )


@main.route("/lektiehjælp/bioteknologi", strict_slashes=False)
def biotek():
    tutor_list = Teacher.query.join(Teacher.subjects).filter(
        Subjects.name.like("%Bioteknologi%"),
        Teacher.photo != "",
        Teacher.bio != "",
        Teacher.status == TeacherStatus.ACTIVE,
        Teacher.marketing_consent == True
    ).order_by(func.random()).limit(15).all()

    keyword = "bioteknologi"
    desc = f"Få hjælp til bioteknologi med en erfaren tutor. Prøv en gratis prøvetime i dag."

    return render_template(
        "seo_pages/bioteknologi.html",
        subject=keyword,
        mainword=f"Lektiehjælp i {keyword}",
        desc=desc,
        subject_city_class="i " + keyword,
        synonynom="lektiehjælper",
        synonynom_plural="lektiehjælpere",
        tutor_list=tutor_list,
        opening_hours=True,
    )


@main.route("/lektiehjælp/international-økonomi", strict_slashes=False)
def internationaløkonomi():
    tutor_list = Teacher.query.join(Teacher.subjects).filter(
        Subjects.name.like("%International Økonomi%"),
        Teacher.photo != "",
        Teacher.bio != "",
        Teacher.status == TeacherStatus.ACTIVE,
        Teacher.marketing_consent == True
    ).order_by(func.random()).limit(15).all()

    keyword = "International Økonomi"
    desc = "Bliv bedre til international økonomi med en tutor, der hjælper dig med at få styr på de komplekse teorier og koncepter. Start med en gratis prøvetime."

    return render_template(
        "seo_pages/internationaløkonomi.html",
        subject=keyword,
        mainword=f"Lektiehjælp i {keyword}",
        desc=desc,
        subject_city_class="i " + keyword,
        synonynom="lektiehjælper",
        synonynom_plural="lektiehjælpere",
        tutor_list=tutor_list,
        opening_hours=True,
    )


@main.route("/lektiehjælp/afsætning", strict_slashes=False)
def afsætning():
    tutor_list = Teacher.query.join(Teacher.subjects).filter(
        Subjects.name.like("%Afsætning%"),
        Teacher.photo != "",
        Teacher.bio != "",
        Teacher.status == TeacherStatus.ACTIVE,
        Teacher.marketing_consent == True
    ).order_by(func.random()).limit(15).all()

    keyword = "afsætning"
    desc = "Lær afsætningsstrategier og -teorier med en erfaren tutor, der tilpasser undervisningen til dine mål og interesser. Få en gratis prøvetime i dag."

    return render_template(
        "seo_pages/afsætning.html",
        subject=keyword,
        mainword=f"Lektiehjælp i {keyword}",
        desc=desc,
        subject_city_class="i " + keyword,
        synonynom="lektiehjælper",
        synonynom_plural="lektiehjælpere",
        tutor_list=tutor_list
    )


@main.route("/lektiehjælp/københavn", strict_slashes=False)
def kobenhavn():
    tutor_list = Teacher.query.join(Teacher.subjects).filter(
        Teacher.photo != "",
        Teacher.bio != "",
        Teacher.status == TeacherStatus.ACTIVE,
        Teacher.marketing_consent == True
    ).order_by(func.random()).limit(15).all()

    keyword = "København"
    desc = f"Få skræddersyet lektiehjælp i København i alle skolefag i folkeskolen og gymnasiet. Start i dag med en gratis prøvetime."

    return render_template(
        "seo_pages/københavn.html",
        subject=keyword,
        mainword=f"Lektiehjælp i {keyword}",
        desc=desc,
        subject_city_class="i " + keyword,
        synonynom="lektiehjælper",
        synonynom_plural="lektiehjælpere",
        tutor_list=tutor_list,
        opening_hours=True
    )


@main.route("/lektiehjælp/<keyword>", strict_slashes=False)
def seopage_lektiehjælp(keyword="",):
    desc = f"Få skræddersyet lektiehjælp i {keyword}, der øger din faglige selvtillid. Start i dag med en gratis prøvetime."
    if keyword.capitalize() in SEO_SUBJECTS:
        if keyword.lower() != keyword:
            return redirect(f"/lektiehjælp/{keyword.lower()}", code=301)

        tutor_list = Tutor.query.filter(
            Tutor.subjects.contains(
                keyword.capitalize().replace("-", "/")
            ),
            Tutor.photo != "",
            Tutor.bio != "",
            Tutor.status == "Active",
            Tutor.marketing_consent == "True"
        ).order_by(func.random()).limit(20).all()
        tutor_list = Teacher.query.join(Teacher.subjects).filter(
            Subjects.name.like(f"{keyword.capitalize().replace('-','/')}"),
            Teacher.photo != "",
            Teacher.bio != "",
            Teacher.status == TeacherStatus.ACTIVE,
            Teacher.marketing_consent == True
        ).order_by(func.random()).limit(15).all()

        # if tutor list is empty or less than 25 then just get some random tutors to have some more content.
        return render_template(
            "seopages.html",
            subject=keyword,
            mainword=f"Lektiehjælp i {keyword}",
            desc=desc,
            subject_city_class="i " + keyword,
            synonynom="lektiehjælper",
            synonynom_plural="lektiehjælpere",
            tutor_list=tutor_list,
            opening_hours=True,
        )
    else:
        tutor_list = Teacher.query.filter(Teacher.photo != "", Teacher.bio != "", Teacher.status ==
                                          TeacherStatus.ACTIVE, Teacher.marketing_consent == True).order_by(func.random()).limit(15).all()
        return seopage("Lektiehjælp", keyword, desc, synonynom="lektiehjælper", synonynom_plural="lektiehjælpere", tutor_list=tutor_list)


@main.route("/SRP-hjælp", strict_slashes=False)
def seopage_srp():
    tutor_list = Teacher.query.filter(Teacher.photo != "", Teacher.bio != "", Teacher.status ==
                                      TeacherStatus.ACTIVE, Teacher.marketing_consent == True).order_by(func.random()).limit(15).all()
    desc = "Få styr på dine større skriftlige opgaver, som SRP, SRO, SOP og DHO."
    return render_template(
        "seo_pages/srp.html", mainword="SRP hjælp", desc=desc, subject_city_class="", synonynom="tutor", synonynom_plural="tutors", tutor_list=tutor_list, opening_hours=True,
    )


@main.route("/eksamenshjælp", strict_slashes=False)
def eksamenshjælp():
    tutor_list = Teacher.query.filter(Teacher.photo != "", Teacher.bio != "", Teacher.status ==
                                      TeacherStatus.ACTIVE, Teacher.marketing_consent == True).order_by(func.random()).limit(15).all()
    desc = "Bliv forberedt til eksamen og få bedre styr på pensum."

    return render_template(
        "seo_pages/eksamenshjælp.html", mainword="Eksamenshjælp", desc=desc, subject_city_class="", synonynom="tutor", synonynom_plural="tutors", tutor_list=tutor_list, opening_hours=True,
    )


@main.route("/lektiehjælp/folkeskole", strict_slashes=False)
def folkeskole():
    tutor_list = Teacher.query.filter(Teacher.photo != "", Teacher.bio != "", Teacher.status ==
                                      TeacherStatus.ACTIVE, Teacher.marketing_consent == True).order_by(func.random()).limit(15).all()
    return render_template("folkeskole.html", tutor_list=tutor_list, subject="folkeskolefag", opening_hours=True,)


@main.route("/lektiehjælp/gymnasiet", strict_slashes=False)
def gymnasiet():
    tutor_list = Teacher.query.filter(Teacher.photo != "", Teacher.bio != "", Teacher.status ==
                                      TeacherStatus.ACTIVE, Teacher.marketing_consent == True).order_by(func.random()).limit(15).all()
    return render_template("gymnasiet.html", tutor_list=tutor_list, subject="gymnasiefag", opening_hours=True,)


@main.route("/dk/privatundervisning", strict_slashes=False)
def privatundervisning_landingpage():
    return render_template("landing_page2.html", opening_hours=True,)


@main.route("/dk/lektiehjælp", strict_slashes=False)
def lektiehjælp_landingpage():
    return render_template("landing_page1.html", opening_hours=True,)


@main.route("/kontakt", methods=["GET", "POST"])
def kontakt():
    """
    Inserting filled contact form to database and sending an email to admins.
    """
    if request.method == "GET":
        return render_template("kontakt.html")

    # METHOD = POST
    # get the results from the form.
    form_results = request.form.to_dict()
    form_keys = list(form_results.keys())

    # honeypot detector
    honeypot = request.form["hidden_field"]
    if honeypot != "" and not None:  # then it's a bot and just redirect.
        flash("Bad Captcha. Prøv igen eller tag kontakt os.")
        return render_template("kontakt.html")

    else:  # passed the honeypot
        human = check_captcha(request)
        if human:
            # form values for Customer
            user_data = {}
            try:
                name = request.form["navn"]
            except Exception:
                name = ""
            try:
                email = request.form["email"].lower()
                user_data["em"] = email
            except Exception:
                email = ""

            try:
                phone = request.form["fulltlf"]
                if phone:
                    user_data["ph"] = [phone]
            except Exception:
                phone = ""

            # blacklisted bot names
            if name in ["HenryLaumb"]:
                flash("Fejl. Prøv igen eller tag kontakt til os.")
                return render_template("kontakt.html")
            elif email == "" and phone == "":
                flash("Fejl. Prøv igen eller tag kontakt til os.")
                return render_template("kontakt.html")

            try:
                first_name = name.split(" ", 1)[0].capitalize()
                user_data["fn"] = first_name.lower()
            except Exception:
                first_name = ""

            if current_app.config.get("ENV_NAME") == "production":
                # Insert student data to CRM
                current_app.task_queue.enqueue_call(  # type:ignore
                    func=zoho_crm.add_contact_and_deal,
                    args=(
                        name,
                        email,
                        phone,
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "Kontaktformular lead",
                    ),
                    result_ttl=5000,
                )

            else:  # don't use RQ when we're not in producton.
                zoho = zoho_crm.add_contact_and_deal(
                    name,
                    email,
                    phone,
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "Kontaktformular lead",
                )
                print(phone)
                print(zoho)
                pass

            if email != "":
                # SEND EMAIL TO LEAD
                html = render_template(
                    "email/customer-confirmation.html", first_name=first_name
                )
                subject = "Velkommen til TopTutors: de næste skridt"

                if current_app.config.get("ENV_NAME") == "production":
                    current_app.task_queue.enqueue_call(  # type:ignore
                        func=send_email,
                        args=([email], subject, html),
                        result_ttl=5000,
                    )

            # UPLOAD LEAD TO DB
            lead = ContactFormLead(name=name, email=email)

            # Add phone number if we have it
            if phone != "" and not None:
                lead.phone = phone

            # Marketing consent
            if "marketing" in form_keys:
                lead.newsletter_accepted = True

            # Commit to DB.
            db.session.add(lead)
            db.session.commit()

            # if production then add lead to partner-ads.
            if current_app.config.get("ENV_NAME") == "production":
                # if the cookies for partner-ads exist then we add it to partner-ads.
                if request.cookies.keys() >= {"paid", "pacid"}:

                    # add to partner-ads.
                    current_app.task_queue.enqueue_call(  # type:ignore
                        func=partner_ads.add_lead,
                        args=(request.cookies.get("paid"), request.cookies.get(
                            "pacid"), "customer_" + str(customer.uid)),
                        result_ttl=5000,
                    )

                elif "asclid" in request.cookies:
                    # add to adservice
                    current_app.task_queue.enqueue_call(  # type:ignore
                        func=partner_ads.add_lead_adservice,
                        args=(request.cookies.get("asclid"),),
                        result_ttl=5000,
                    )

                if "marketing" in form_keys:
                    body = {
                        "members": [
                            {
                                "email": email,
                            }
                        ]
                    }
                    current_app.task_queue.enqueue_call(  # type:ignore
                        func=ghost_api.request_without_token,
                        args=(
                            "POST", "https://toptutors.ghost.io/ghost/api/admin/members/", body),
                        result_ttl=5000,
                    )

                # FACEBOOK CONVERSION API
                user_data["client_ip_address"] = request.remote_addr
                user_data["client_user_agent"] = request.headers.get(
                    'User-Agent')
                # Get fbc
                if "_fbc" in request.cookies:
                    user_data["fbc"] = request.cookies.get("_fbc")
                # Get fbp
                if "_fbp" in request.cookies:
                    user_data["fbp"] = request.cookies.get("_fbp")

                current_app.task_queue.enqueue_call(  # type:ignore
                    func=meta_ads.add_event,
                    args=("Lead", user_data, f"customer_{str(customer.uid)}"),
                    result_ttl=5000,
                )

            if phone != "" or phone is not None:
                if phone.startswith("00"):
                    phone = "+" + phone[2:]
                elif phone.startswith("+"):
                    pass
                else:
                    phone = "+45" + phone

            if email is None or email == "":
                email = phone + "@dummy.com"

            session["form_email"] = email
            session["form_phone"] = phone
            # Everythins is done, so we redirect user to confirmation page.
            return redirect(url_for("main.confirmation"))
        else:  # did not pass the captcha
            flash("Fejl. Prøv igen eller tag kontakt til os.")
            return render_template("kontakt.html", opening_hours=True,)
