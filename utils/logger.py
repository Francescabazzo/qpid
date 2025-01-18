from datetime import datetime as dt
from streamlit_cookies_controller import CookieController

def log(message):
    cookie = CookieController()

    if cookie.get('user_login'):
        user = f"<{cookie.get('user_login')}>"
    else:
        user = "<NONE>"

    print(f"{user} @ {dt.now()}: {message}")