import streamlit as st
from utils.db_utils import load_likes_dislikes

st.set_page_config(
    page_title='QPID - Matches',
    page_icon="utils/logo.png",
    initial_sidebar_state="expanded"
)


if 'user_login' not in st.session_state:
    st.warning("You must log in to continue!", icon="⚠️")

else:
    st.header("Likes and Dislikes")
    st.text("Here you can find all the profile that you liked or disliked!")

    likes_dislikes = load_likes_dislikes(st.session_state['user_ID'])

    st.dataframe(likes_dislikes, hide_index=True)

