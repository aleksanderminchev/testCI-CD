from flask import Blueprint, send_from_directory, redirect, url_for, render_template, make_response
from api.utils.routes_utils import get_sitemap_pages

from api.utils.routes_utils import get_sitemap_pages
from flask import render_template
from api.utils.keywords import SEO_LOCATIONS, SEO_SUBJECTS, SEO_LEVELS
misc = Blueprint('misc', __name__)


# robots.txt
@misc.route("/robots.txt", methods=["GET"])
def robots():
    return send_from_directory("static", "robots.txt")


@misc.route("/sitemap.xml", methods=["GET"])
def sitemap():
    """
    Route to generate all the sitemaps of the website.
    """
    list_of_sitemap_pages = get_sitemap_pages()
    print(len(list_of_sitemap_pages))
    sitemap_template = render_template("sitemap/sitemap_template.xml", pages=list_of_sitemap_pages)
    response = make_response(sitemap_template)
    response.headers["Content-Type"] = "application/xml"
    return response

@misc.route('/sitemap')
def htmlsitemap():
    # general_pages = get_sitemap_pages(include_seo_pages=False)

    # gemeral_pages_formatted = []

    # # Format the general pages to be a list of dicts with name and url
    # for page in general_pages:
    #     # We already have the URL
    #     url = page[0]
    #     # We need to get the name as the last part of the URL
    #     page = url.strip("/")
    #     last_slash = page.rfind("/")
    #     last_part = page[last_slash + 1:]

    #     # Add the formatted page to the list
    #     gemeral_pages_formatted.append({"url": url, "name": last_part})

    subject_pages = [f'/lektiehjælp/{fag}' for fag in SEO_SUBJECTS]
    subject_pages = []
    for fag in SEO_SUBJECTS:
    # Extract the grade name from the SEO_LEVELS
        subject = fag.split(",")[0].strip()
    # Construct the URL using the city name
        url = f"/lektiehjælp/{subject.lower()}"
    # Add the page to the SEO_LEVELS list
        subject_pages.append({"url": url, "name": subject})



    location_pages = []
    for location in SEO_LOCATIONS:
    # Extract the city name from the location
        city = location.split(",")[0].strip()
    # Construct the URL using the city name
        url = f"/lektiehjælp/{city.lower()}"
    # Add the page to the location_pages list
        location_pages.append({"url": url, "name": city})

    level_pages = []
    for level in SEO_LEVELS:
    # Extract the grade name from the SEO_LEVELS
        niveauer = level.split(",")[0].strip()
    # Construct the URL using the city name
        url = f"/lektiehjælp/{niveauer.lower()}"
    # Add the page to the SEO_LEVELS list
        niveauer = niveauer.replace("-", " ")
    # Replace all - from "(niveau).-klasse" to a space.  
        level_pages.append({"url": url, "name": niveauer})


    return render_template('sitemap.html', subject_pages=subject_pages, location_pages=location_pages, level_pages=level_pages)