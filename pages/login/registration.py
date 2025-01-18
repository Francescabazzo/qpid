import streamlit as st
from utils.db_connection import connect2db
from sqlalchemy.exc import DBAPIError as exc
from sqlalchemy import text
from utils.logger import log


# ====================

def registration():
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
            with connect2db() as conn:
                try:
                    query = f"INSERT INTO users SET username='{st.session_state['username']}', password='{st.session_state['password']}', email='{st.session_state['email']}'"
                    conn.execute(text(query))

                    # Creates entries in the other DB tables (due to unavailability of Triggers)
                    query = f"SELECT ID FROM users WHERE username='{st.session_state['username']}'"
                    user_id = conn.execute(text(query)).fetchall()[0][0]

                    query2 = f"INSERT INTO profiles SET ID='{user_id}'"
                    query3 = f"INSERT INTO intos SET ID='{user_id}'"
                    conn.execute(text(query2))
                    conn.execute(text(query3))

                    conn.commit()

                    # -----------

                    st.success("The new account has been created!", icon="💚")

                    log(f"REGISTRATION of user <{st.session_state['username']}>")
                except exc as e:
                    conn.rollback()
                    st.error(f"An error occurred while inserting data into the database: {e}", icon="❌")

                    log(f"REGISTRATION of user <{st.session_state['username']}> ERROR: {e}")

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
