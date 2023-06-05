from decouple import config

tw_api_key = config("TW_API")

tw_headers = {
    "Authorization": "Token token=" + tw_api_key,
    "Content-Type": "application/json; charset=utf8",
}
