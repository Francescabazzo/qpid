from datetime import datetime as dt
from streamlit_cookies_controller import CookieController
import logging

def log(message, level=0, name=None):
    cookie = CookieController()

    logger = logging.getLogger(name)

    if cookie.get('user_login'):
        user = f"<{cookie.get('user_login')}>"
    else:
        user = "<NONE>"

    message = f"{user} @ {dt.now()}: {message}"

    match level :
        case 0:
            logger.info(message)
        case 1:
            logger.warning(message)
        case 2:
            logger.error(message)

    print(message)