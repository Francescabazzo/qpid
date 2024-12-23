import streamlit as st
from mysql.connector import Error
from utils.db_connection import connect2db


def login():
    st.header("Login:")

    if 'user_login' not in st.session_state:
        st.warning("You must log in to continue!", icon="⚠️")

        def form_callback():
            conn = connect2db()
            cursor = conn.cursor()

            try:
                query = f"SELECT ID, username from users WHERE username='{st.session_state['username']}' AND password='{st.session_state['password']}'"

                cursor.execute(query)

                users = cursor.fetchall()

                if len(users):
                    st.session_state['user_login'] = st.session_state['username']
                    st.session_state['user_ID'] = users[0][0]
                else:
                    st.error("Wrong username or password!", icon="❌")  # todo POSIZIONAMENTO ALERT
            except Error as e:
                st.error(f"An error occurred while reading data from database: {e}", icon="❌")
            finally:
                cursor.close()
                conn.close()

        with st.form(key='login_form'):
            st.text_input('Username', key="username", )
            st.text_input('Password', key="password", type="password")

            st.form_submit_button(label='Login', on_click=form_callback)
    else:
        st.success("You are logged in! You can navigate to other pages", icon="💚")
