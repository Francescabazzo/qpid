import streamlit as st
from sqlalchemy.exc import DBAPIError as exc
from sqlalchemy import text

from utils.db_connection import connect2db_NEW


def registration():
    st.header("Registration:")
    st.markdown("If you don't have an account, you can create one!")

    def form_callback():
        if not st.session_state['reg_username'] or not st.session_state['reg_password'] or not st.session_state[
            'reg_email']:
            st.error("You must fill all fields to continue!", icon="❌")
        elif st.session_state['reg_password'] != st.session_state['reg_password2']:
            st.error("The two passwords do not correspond!", icon="❌")
        elif not st.session_state['reg_policy'] :
            st.error("You must accept the policy!", icon="❌")
        elif '@' not in st.session_state['reg_email']:
            st.error("You need to provide a correct email address!", icon="❌")
        else:
            with connect2db_NEW() as conn:
                try:
                    query = f"INSERT INTO users SET username='{st.session_state['reg_username']}', password='{st.session_state['reg_password']}', email='{st.session_state['reg_email']}'"

                    conn.execute(text(query))

                    # Creates entries in the other DB tables

                    query = f"SELECT ID FROM users WHERE username='{st.session_state['reg_username']}'"

                    user_id = conn.execute(text(query)).fetchall()[0][0]

                    query2 = f"INSERT INTO profiles SET ID='{user_id}'"
                    query3 = f"INSERT INTO intos SET ID='{user_id}'"

                    conn.execute(text(query2))
                    conn.execute(text(query3))

                    conn.commit()

                    # -----------

                    st.success("The new account has been created!", icon="💚")
                except exc as e:
                    conn.rollback()
                    st.error(f"An error occurred while inserting data into the database: {e}", icon="❌")

    with st.form(key='reg_form'):
        st.text_input('Username', key="reg_username")
        st.text_input('E-Mail', key="reg_email")
        st.text_input('Password', key="reg_password", type="password")
        st.text_input('Repeat Password', key="reg_password2", type="password")

        st.checkbox('I accept to share my email address with other users', key="reg_policy")

        st.form_submit_button(label='Create Account', on_click=form_callback)
