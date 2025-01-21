import streamlit as st
from streamlit_cookies_controller import CookieController

import utils.db.queries as db


# ====================

def registration():
    cookie = CookieController()

    # ===== FORM CALLBACK =====

    def callback():
        if not st.session_state['username'] or not st.session_state['password'] or not st.session_state['email']:
            st.error("You must fill all fields to continue!", icon="❌")
        elif st.session_state['password'] != st.session_state['password2']:
            st.error("The two passwords do not correspond!", icon="❌")
        elif not st.session_state['policy']:
            st.error("You must accept the policy!", icon="❌")
        elif '@' not in st.session_state['email']:
            st.error("You need to provide a correct email address!", icon="❌")
        else:
            db.registration(st.session_state['username'], st.session_state['password'], st.session_state['email'])

    # ===== END of CALLBACK =====

    st.header("Registration:")
    st.markdown("If you don't have an account, you can create one!")

    with st.form(key='reg_form'):
        st.text_input('Username', key="username")
        st.text_input('E-Mail', key="email")
        st.text_input('Password', key="password", type="password")
        st.text_input('Repeat Password', key="password2", type="password")

        st.checkbox('I accept to share my email address with other users', key="policy")

        st.form_submit_button(label='Create Account', on_click=callback)
