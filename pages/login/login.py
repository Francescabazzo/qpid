import streamlit as st
from streamlit_cookies_controller import CookieController
from utils.db_connection import connect2db
from sqlalchemy.exc import DBAPIError as exc
from sqlalchemy import text
from utils.logger import log


# ====================


def login():
    cookie = CookieController()

    # ===== FORM CALLBACKS =====

    def login_callback():
        with connect2db() as conn:
            try:
                query = f"SELECT ID, username from users WHERE username='{st.session_state['username']}' AND password='{st.session_state['password']}'"

                users = conn.execute(text(query)).fetchall()

                if len(users):
                    cookie.set('user_login', st.session_state['username'])
                    cookie.set('user_ID', users[0][0])

                    log(f"Log-IN")
                else:
                    st.error("Wrong username or password!", icon="❌")
            except exc as e:
                st.error(f"An error occurred while reading data from database: {e}", icon="❌")

                log(f"LOG-IN of {st.session_state['username']} ERROR: {e}")

    def logout_callback():
        log(f"Log-OUT")

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
