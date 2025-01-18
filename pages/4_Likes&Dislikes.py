import streamlit as st
from streamlit_cookies_controller import CookieController
import pandas as pd
from utils.db_connection import connect2db
from sqlalchemy.exc import DBAPIError as exc
from sqlalchemy import text
from utils.db_utils import load_likes_dislikes, load_profiles_from_ids
from utils.converters import pronoun_num2text
from utils.logger import log

st.set_page_config(
    page_title='QPID - Matches',
    page_icon="utils/images/logo.png",
    initial_sidebar_state="expanded"
)

# ====================

cookie = CookieController()


# ===== UTILS FUNCTIONS =====

def load_likes(_likes_dislikes):
    likes = _likes_dislikes.loc[_likes_dislikes['like_dislike'] == 1]

    log(f"LIKES LOADING: {len(likes)} ENTRIES FOUND", 0, __name__)

    if likes.empty:
        st.warning("No likes yet...")
    else:
        profiles = load_profiles_from_ids(likes['ID_other'].tolist())

        likes = likes.reset_index(drop=True)
        profiles = profiles.reset_index(drop=True)

        df = pd.concat([profiles['name'], profiles['age'], profiles['gender'], likes['is_match'], profiles['email']],
                       axis=1)

        df['email'] = df['email'].where(df['is_match'] == 1, "")

        df['is_match'] = df['is_match'].replace(1, "The user liked your profile too! 🤩")
        df['is_match'] = df['is_match'].replace(0, "This user have not liked your profile (so far...)")

        df['gender'] = df['gender'].apply(pronoun_num2text)

        df.rename(
            columns={'name': 'Name', 'gender': 'Gender', 'age': 'Age', 'is_match': 'Reciprocal Like', 'email': 'Email'},
            inplace=True)

        st.table(df)


def load_dislikes(_likes_dislikes):
    dislikes = _likes_dislikes.loc[_likes_dislikes['like_dislike'] == 0]

    log(f"DISLIKES LOADING: {len(dislikes)} ENTRIES FOUND", 0, __name__)

    if dislikes.empty:
        st.warning("No dislikes yet...")
    else:
        profiles = load_profiles_from_ids(dislikes['ID_other'].tolist())

        profiles = profiles.reset_index(drop=True)

        df = pd.concat([profiles['name'], profiles['age'], profiles['gender']], axis=1)

        df['gender'] = df['gender'].apply(pronoun_num2text)

        df.rename(columns={'name': 'Name', 'gender': 'Gender', 'age': 'Age'}, inplace=True)

        st.table(df)


# ===== END of UTILS FUNCTIONS =====
# ===== CALLBACK =====

def callback():
    with connect2db() as conn:
        try:
            conn.execute(text(f"DELETE FROM likes WHERE ID = {cookie.get('user_ID')}"))
            conn.commit()

            log("LIKES DISLIKES RESET", 0, __name__)

        except exc as e:
            st.error(f"An error occurred while inserting data into the database: {e}", icon="❌")

            log(f"LIKES DISLIKES RESET ERROR: {e}", 2, __name__)


# ===== END of CALLBACK =====
# ===== MAIN PAGE =====

if not cookie.get('user_login'):
    st.warning("You must log in to continue!", icon="⚠️")
else:
    likes_dislikes = load_likes_dislikes(cookie.get('user_ID'))

    st.header("Likes and Dislikes")
    st.text("Here you can find all the profile that you liked or disliked!")

    st.subheader("Profiles that you LIKED")
    st.markdown(
        "Notice that in case of a **RECIPROCAL LIKE** the E-Mail address of the other user will become visible to you, so you can start know each other better!")

    load_likes(likes_dislikes)

    st.subheader("Profiles that you DISLIKED")
    st.text("Remember: these profiles will not appear in your proposed profiles anymore!")

    load_dislikes(likes_dislikes)

    with st.form(key='reset'):
        st.form_submit_button(label='Reset Likes & Dislikes', on_click=callback, type="primary", icon="🗑️",
                              use_container_width=True)
