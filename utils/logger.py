from datetime import datetime as dt
from streamlit_cookies_controller import CookieController
import logging

def log(message, level=0):
    cookie = CookieController()

    if cookie.get('user_login'):
        user = f"<{cookie.get('user_login')}>"
    else:
        user = "<NONE>"

    message = f"{user} @ {dt.now()}: {message}"

    match level :
        case 0:
            logging.info(message)
        case 1:
            logging.warning(message)
        case 2:
            logging.error(message)

    print(message)