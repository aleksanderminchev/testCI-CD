
import requests


def add_lead(paid, pacid, variable_id):
    """
    Adds lead to partner-ads. Gets called after the user reaches the confirmation page.

    PROGRAM_ID = Id'en for det program du har oprettet (ikke annoncørid)
    PAID = Den partnerid som du gemte i cookien i step 1 (variablen paid)
    PACID = Den unikke klik id som du gemte i cookieen i step 1 (variable pacid).
    VARIABEL = En unik identifikation af leadet (skal være en id, som du også registrerer hos dig)
    """

    program_id = "9554"

    result = requests.get(
        f"https://www.partner-ads.com/dk/leadtracks2s.php?programid={program_id}&type=lead&partnerid={paid}&pacid={pacid}&uiv={variable_id}")
    return result


def add_lead_adservice(asclid):
    """
    Adds lead to adservice.com
    """
    result = requests.get(
        f"https://www.aservice.cloud/trc/mastertag/conv?asclid={asclid}")
    return result
