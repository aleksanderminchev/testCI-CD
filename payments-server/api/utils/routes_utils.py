from datetime import datetime, timedelta

from flask import current_app, render_template, flash, redirect, url_for, session

from api import db
from api.services import zoho_crm, partner_ads, meta_ads
from api.utils.keywords import SEO_KEYWORDS
from api.utils.utils import check_captcha
from api.email import send_email
from models.phonelead import PhoneLead
from models.course import Course
from models.tutor import Tutor
from models.teacher import Teacher


def get_sitemap_pages(include_seo_pages=True):
    """ Generates all of the possible SEO combinations as a default.
     If you don't want that then use include_seo_pages=False """
    pages = []

    # get static routes
    # use arbitary 10 days ago as last modified date
    lastmod = datetime.datetime.now() - datetime.timedelta(days=10)
    lastmod = lastmod.strftime("%Y-%m-%d")
    for rule in current_app.url_map.iter_rules():
        # omit auth and admin routes and if route has parameters. Only include if route has GET method
        if (
            "GET" in rule.methods  # type: ignore
            and len(rule.arguments) == 0
            and not rule.rule.startswith("/admin")
            and not rule.rule.startswith("/dashboard")
            and not rule.rule.startswith("/confirm")
            and not rule.rule.startswith("/api")
            and not rule.rule.startswith("/admin-login")
            and not rule.rule.startswith("/afleveringshjælp")
            and not rule.rule.startswith("/privatundervisning")
            and not rule.rule.startswith("/tak")
            and not rule.rule.startswith("/tak-for-ansøgning")
            and not rule.rule.startswith("/dk/privatundervisning")
            and not rule.rule.startswith("/dk/lektiehjælp")
            and not rule.rule.startswith("/privatunderviser")
            and not rule.rule.startswith("/større-opgaver")
            and not rule.rule.startswith("/lektiehjælper")
            and not rule.rule.startswith("/undervisning")
            and not rule.rule.startswith("/tutor-logind")
            and not rule.rule.startswith("/tutor-login")
            and not rule.rule.startswith("/folkeskole")
            and not rule.rule.startswith("/gymnasiet")
            and not rule.rule.startswith("/logout")
            and not rule.rule.startswith("/mentor")
            and not rule.rule.startswith("/nykode")
            and not rule.rule.startswith("/succes")
            and not rule.rule.startswith("/tutors")
            and not rule.rule.startswith("/ansøg")
            and not rule.rule.startswith("/hjælp")
            and not rule.rule.startswith("/job")
            and not rule.rule.startswith("/bliv-topTutor")
            and not rule.rule.startswith("/course")
            and not rule.rule.startswith("/pay")
            and not rule.rule.startswith("/order")
            and not rule.rule.startswith("/confirmation")
            and not rule.rule.startswith("/customer-portal")
            and not rule.rule.startswith("/logind")
        ):
            # add SEO pages for mainword/keyword if enabled
            if include_seo_pages is True:
                for keyword in SEO_KEYWORDS:
                    pages.append([f"https://www.toptutors.dk/lektiehjælp/{keyword.lower()}", lastmod])

    # add SEO pages for mainword/keyword
    for keyword in SEO_KEYWORDS:
        pages.append(
            [f"https://www.toptutors.dk/lektiehjælp/{keyword.lower()}", lastmod])

    # divides them in groups of 20.000 each.
    # n = 20000
    # pages = [pages[i:i+n] for i in range(0, len(pages), n)]
    return pages


def render_page_404():
    return render_template('404.html'), 404


def format_phone_number_as_arguments(phone):
    return (
        "",
        "",
        phone,
        "",
        "1",
        "",
        "",
        "",
        "",
        "",
        "",
        "Udfyldt tlf. nr. via hjemmesiden",
    )


def process_phonelead_form(request):
    # Phone input has been submitted trough POST
    # get phone number submitted and captcha response.
    phone = request.form["fulltlf"]
    if phone == "" or phone is None:
        flash("Ugyldigt nummer. Prøv igen eller tag kontakt os.")
        return redirect(url_for("main.index"))
    # else:
    #    if "0045" in phone[0:4]:
    #       phone = phone[4:]
    #  elif "+45" in phone[0:3]:
    #        phone = phone[3:]

    human = check_captcha(request)
    # Phone number is good and they pass captcha, so we redirect them to confirmation page.
    if human:
        if current_app.config.get("ENV_NAME") == "production":
            # Insert student data to crm
            name, email, phone, zip_code, num_people, help_types, education, course_subject, online_session, note, school_level, lead_type = format_phone_number_as_arguments(
                phone)
            current_app.task_queue.enqueue_call(  # type:ignore
                func=zoho_crm.add_contact_and_deal,
                args=(name, email, phone, zip_code, num_people, help_types, education,
                      course_subject, online_session, note, school_level, lead_type),
                result_ttl=5000,
            )

            email_info = {"phone_number": phone, "LEAD_TYPE": lead_type}
            html_admin = render_template(
                "email/error-mail.html", error=email_info
            )

            current_app.task_queue.enqueue_call(  # type:ignore
                func=send_email,
                args=(["elmar@toptutors.dk"], "NEW LEAD", html_admin),
                result_ttl=5000,
            )
            phone_lead = PhoneLead(phone=phone)
            db.session.add(phone_lead)
            db.session.commit()

            # if the cookies for partner-ads exist then we add it to partner-ads.
            if request.cookies.keys() >= {"paid", "pacid"}:
                # add to partner-ads.
                current_app.task_queue.enqueue_call(  # type:ignore
                    func=partner_ads.add_lead,
                    args=(request.cookies.get("paid"), request.cookies.get(
                        "pacid"), "phone_lead_" + str(phone_lead.uid)),
                    result_ttl=5000,
                )
            elif "asclid" in request.cookies:
                # add to adservice
                current_app.task_queue.enqueue_call(  # type:ignore
                    func=partner_ads.add_lead_adservice,
                    args=(request.cookies.get("asclid"),),
                    result_ttl=5000,
                )

            # Facebook Offline conversions API
            user_data = {"ph": [phone], "client_ip_address": request.remote_addr,
                         "client_user_agent": request.headers.get('User-Agent')}

            # Get fbc
            if "_fbc" in request.cookies:
                user_data["fbc"] = request.cookies.get("_fbc")

            # Get fbp
            if "_fbp" in request.cookies:
                user_data["fbp"] = request.cookies.get("_fbp")

            current_app.task_queue.enqueue_call(  # type:ignore
                func=meta_ads.add_event,
                args=("Lead", user_data, ""),
                result_ttl=5000,
            )

        else:  # DEVELOPMENT VERSION
            # zoho_crm.add_contact_and_deal(*format_phone_number_as_arguments(phone))
            # partner_ads.add_lead_adservice(request.cookies.get("asclid"))
            # user_data = {"ph": [phone]}
            # meta_ads.add_event("Lead", request, user_data, "", True)

            # phone_lead = PhoneLead(phone=phone)
            # db.session.add(phone_lead)
            # db.session.commit()
            pass

        if phone.startswith("00"):
            phone = "+" + phone[2:]
        elif phone.startswith("+"):
            pass
        else:
            phone = "+45" + phone

        email = phone + "@dummy.com"

        session["form_email"] = email
        session["form_phone"] = phone
        return redirect(url_for("main.confirmation"))
    flash("Fejl. Prøv igen eller tag kontakt os.")
    return redirect(url_for("main.index"))


def seopage(mainword, keyword, desc, tutor_list, synonynom="tutor", synonynom_plural="tutors"):
    """ Generates our SEO pages based on keywords
    """
    if keyword is None:
        return render_template(
            "seopages.html", mainword=mainword, desc=desc, subject=keyword, subject_city_class="", synonynom=synonynom, synonynom_plural=synonynom_plural, tutor_list=tutor_list, opening_hours=True,
        )

    # want to capitalize everything except gym types and I want to remove the dash in grades.
    if keyword.upper() not in ["HHX", "STX", "HTX", "HF", "EUX"]:
        keyword = keyword.capitalize()
    else:
        keyword = keyword.upper()

    if keyword in SEO_KEYWORDS:  # make sure that it's an approve keyword
        if ".-klasse" in keyword:  # check if that keyword is a class level.s
            # as it is a class then replace the dash with a space.
            keyword = keyword.replace("-", " ")
        return render_template(
            "seopages.html", mainword=mainword + " i " + keyword, subject=keyword, desc=desc, subject_city_class="i " + keyword, synonynom=synonynom, synonynom_plural=synonynom_plural, keyword=keyword, tutor_list=tutor_list, opening_hours=True,
        )
    else:
        return render_page_404()


def course_teacher_search(email, courses):
    """
    Search for a teacher by email and return a dictionary of the found courses and the tutor.

    :param email: The email of the tutor to search for.
    :param courses: The list of all courses.
    :return: A dictionary with the found courses and the tutor.
    """

    # Case insensitive query:
    tutor = Teacher.get_teacher_by_email(email, False) or flash('Indsæt en gyldig email')
    # tutor = Tutor.query.filter_by(email=email).first() or flash('Please enter correct tutor email')

    if not tutor:
        return None

    # Create Session
    session['tutor'] = {"tutor_email": tutor.user.email, "tutor_id": tutor.user_id}

    # Set default to False
    has_prio_subject = False

    # List of all subjects
    priority_subjects = {"Bioteknologi A", "Biologi A", "Fransk A", "Fysik A", "Tysk A", "Kemi A",
                         "Virksomhedsøkonomi A", "International økonomi A", "Afsætningsøkonomi A", "Matematik A", "Math A"}

    # Check if a priority subject is in tutor profile.
    for i in tutor.subjects:
        if i.name in priority_subjects:
            has_prio_subject = True

    # Set defaults to empty List
    courses_can_teach = []
    priority_courses = []

    for i in courses:
        subject_list = {subj for subj in i.subjects.split(',')}
        courses_can_teach = courses_can_teach + [i for j in tutor.subjects if j.name in subject_list]
        priority_courses = priority_courses + [i for j in subject_list if j in priority_subjects]

    # Combine all courses
    all_courses = set(priority_courses).union(courses_can_teach)

    # Filter courses 3 days old or older
    three_days_ago = datetime.now() - timedelta(days=3)
    filtered_courses = [course for course in all_courses if course.created_at <= three_days_ago]

    if has_prio_subject:
        # Prioritized teacher to show prioritized subjects he can teach in the front,
        # then the rest of the prioritized subjects,
        # non-prio teacher courses he can teach in,
        # and then all others
        courses_can_teach = set(filtered_courses).intersection(priority_courses)
        courses = set(priority_courses).difference(courses_can_teach).union(filtered_courses)
    else:
        courses = filtered_courses

    tutor_info = {"tutor_email": tutor.user.email, "tutor_id": tutor.user_id}

    return {"found_courses": {"all_courses": courses, "match": courses_can_teach}, "tutor": tutor_info}
