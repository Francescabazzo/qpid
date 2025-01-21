import streamlit as st
from streamlit_cookies_controller import CookieController
from utils.logger import log
import utils.db.queries as db


# ====================


def login():
    cookie = CookieController()

    # ===== FORM CALLBACKS =====

    def login_callback():
        db.login(st.session_state['username'], st.session_state['password'])

    def logout_callback():
        log("Log-OUT", 0)

        cookie.remove('user_login')

        for key in st.session_state.keys():
            del st.session_state[key]

    # ===== END of CALLBACKS =====

    st.header("Login:")

    if not cookie.get('user_login'):
        st.warning("You must log in to continue!", icon="⚠️")

        with st.form(key='login_form'):
            st.text_input('Username', key="username")
            st.text_input('Password', key="password", type="password")

            st.form_submit_button(label='Login', on_click=login_callback)
    else:
        with st.form(key='logout_form'):
            st.success("You are logged in! You can navigate to other pages", icon="💚")

            st.form_submit_button(label='Logout', type="primary", on_click=logout_callback)
