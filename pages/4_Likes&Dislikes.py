import streamlit as st
from mysql.connector import Error
from utils.db_utils import load_likes_dislikes, load_profiles_from_ids
from utils.converters import gender_num2text
from utils.db_connection import connect2db
import pandas as pd

st.set_page_config(
    page_title='QPID - Matches',
    page_icon="utils/logo.png",
    initial_sidebar_state="expanded"
)

def load_likes(likes_dislikes) :
    likes = likes_dislikes.loc[likes_dislikes['like_dislike'] == 1]

    if likes.empty :
        st.warning("No likes yet...")
    else:
        profiles = load_profiles_from_ids(likes['ID_other'].tolist())

        likes['is_match'].replace(1, "The user liked your profile too! 🤩", inplace=True)
        likes['is_match'].replace(0, "", inplace=True)

        profiles['gender'] = profiles['gender'].apply(gender_num2text)

        likes = likes.reset_index(drop=True)
        profiles = profiles.reset_index(drop=True)

        df = pd.concat([profiles['name'], profiles['age'], profiles['gender'], likes['is_match']], axis=1)

        st.table(df)

def load_dislikes(likes_dislikes) :
    dislikes = likes_dislikes.loc[likes_dislikes['like_dislike'] == 0]

    if dislikes.empty :
        st.warning("No dislikes yet...")
    else:
        profiles = load_profiles_from_ids(dislikes['ID_other'].tolist())

        profiles['gender'] = profiles['gender'].apply(gender_num2text)

        profiles = profiles.reset_index(drop=True)

        df = pd.concat([profiles['name'], profiles['age'], profiles['gender']], axis=1)

        st.table(df)

def callback() :
    conn = connect2db()
    cursor = conn.cursor()

    try:
        cursor.execute(f"DELETE FROM likes WHERE ID = {st.session_state['user_ID']}")
        conn.commit()

        #st.success("The new account has been created!", icon="💚")
    except Error as e:
        st.error(f"An error occurred while inserting data into the database: {e}", icon="❌")
    finally:
        cursor.close()
        conn.close()

if 'user_login' not in st.session_state:
    st.warning("You must log in to continue!", icon="⚠️")

else:
    likes_dislikes = load_likes_dislikes(st.session_state['user_ID'])

    st.header("Likes and Dislikes")
    st.text("Here you can find all the profile that you liked or disliked!")

    st.subheader("Profiles that you LIKED")

    load_likes(likes_dislikes)

    st.subheader("Profiles that you DISLIKED")
    st.text("Remember: these profiles will not appear in your proposed profiles anymore!")

    load_dislikes(likes_dislikes)

    with st.form(key='reset'):
        st.form_submit_button(label='Reset Likes & Dislikes', on_click=callback, type="primary", icon="🗑️", use_container_width=True)