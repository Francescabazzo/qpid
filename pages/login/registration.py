import streamlit as st
from mysql.connector import Error

from utils.db_connection import connect2db


def registration():
    st.header("Registration:")
    st.markdown("If you don't have an account, you can create one!")

    # st.warning("You must log in to continue!", icon="⚠️")

    def form_callback():
        if not st.session_state['reg_username'] or not st.session_state['reg_password'] or not st.session_state[
            'reg_email']:
            st.error("You must fill all fields to continue!", icon="❌")  # todo POSIZIONAMENTO ALERT
        elif st.session_state['reg_password'] != st.session_state['reg_password2']:
            st.error("The two passwords do not correspond!", icon="❌")  # todo POSIZIONAMENTO ALERT
        elif '@' not in st.session_state['reg_email']:
            st.error("You need to provide a correct email address!", icon="❌")  # todo POSIZIONAMENTO ALERT
        else:
            conn = connect2db()
            cursor = conn.cursor()

            # TODO GESTIRE TUTTE CASISTICHE PER NUOVO UTENTE

            try:
                query = f"INSERT INTO users SET username='{st.session_state['reg_username']}', password='{st.session_state['reg_password']}', email='{st.session_state['reg_email']}'"

                cursor.execute(query)
                conn.commit()

                st.success("The new account has been created!", icon="💚")
            except Error as e:
                st.error(f"An error occurred while inserting data into the database: {e}", icon="❌")
            finally:
                cursor.close()
                conn.close()

    with st.form(key='reg_form'):
        input_username = st.text_input('Username', key="reg_username", )
        input_email = st.text_input('E-Mail', key="reg_email", )
        input_password = st.text_input('Password', key="reg_password", type="password")
        input_password2 = st.text_input('Repeat Password', key="reg_password2", type="password")

        submit_button = st.form_submit_button(label='Create Account', on_click=form_callback)
