import streamlit as st
from streamlit_cookies_controller import CookieController
from utils.logger import log
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError as exc
import pandas as pd

from utils.db.connection import connect2db

# ========== LOGIN ==========

def login(_username, _password):
    cookie = CookieController()

    with connect2db() as conn:
        try:
            query = f"SELECT ID, username from users WHERE username='{_username}' AND password='{_password}'"

            users = conn.execute(text(query)).fetchall()

            if len(users):
                cookie.set('user_login', _username)
                cookie.set('user_ID', users[0][0])

                log("Log-IN", 0)
            else:
                st.error("Wrong username or password!", icon="❌")
        except exc as e:
            st.error(f"An error occurred while reading data from database: {e}", icon="❌")

            log(f"LOG-IN of {st.session_state['username']} ERROR: {e}", 2)

# ========== REGISTRATION ==========

def registration(_username, _password, _email):
    with connect2db() as conn:
        try:
            query = f"INSERT INTO users SET username='{_username}', password='{_password}', email='{_email}'"
            conn.execute(text(query))

            # Creates entries in the other DB tables (due to unavailability of Triggers)
            query = f"SELECT ID FROM users WHERE username='{_username}'"
            user_id = conn.execute(text(query)).fetchall()[0][0]

            query2 = f"INSERT INTO profiles SET ID='{user_id}'"
            query3 = f"INSERT INTO intos SET ID='{user_id}'"
            conn.execute(text(query2))
            conn.execute(text(query3))

            conn.commit()

            # -----------

            st.success("The new account has been created!", icon="💚")

            log(f"REGISTRATION of user <{_username}>", 0)
        except exc as e:
            conn.rollback()
            st.error(f"An error occurred while inserting data into the database: {e}", icon="❌")

            log(f"REGISTRATION of user <{_username}> ERROR: {e}", 2)

# ========== OTHER ==========



def load_likes_dislikes(user_id):
    with connect2db() as conn:
        df = pd.read_sql(f"SELECT ID_other, like_dislike, is_match from likes_bidirectional WHERE ID = '{user_id}'",
                         conn)

    return df


def load_profiles_from_ids(ids):
    ids_list = ', '.join(map(str, ids))

    with connect2db() as conn:
        df = pd.read_sql(
            f"SELECT * from full_profiles WHERE ID IN ({ids_list}) ORDER BY CASE ID {' '.join([f'WHEN {_id} THEN {i}' for i, _id in enumerate(ids)])} ELSE {len(ids)} END",
            conn)

    return df
