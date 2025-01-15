import streamlit as st
import hydralit_components as hc

st.set_page_config(
    page_title='QPID - Homepage',
    page_icon="utils/logo.png",
    initial_sidebar_state="expanded"
)

from pages.login.login import login
from pages.login.registration import registration

# ===== MAIN PAGE =====

st.title("QPID - Find your perfect match!")

st.markdown(
    "Welcome to **QPID**, the innovative web application for finding your perfect match based on your interests!")
st.markdown(
    "Fill the questionnaire and navigate between dozens of people close to your selections: one of them is your perfect match!")

st.info(
    "**This is a Proof-of-Concept Application!** We do not guarantee security standards, privacy policies compliance and constant bug fixing, so please do not consider using this software as a professional tool.")

# ===== TABS =====

LOGIN = 'Login'
REGISTRATION = 'Register'

tabs = [
    LOGIN,
    REGISTRATION
]

option_data = [
    {'icon': "🔐", 'label': LOGIN},
    {'icon': "🖋️", 'label': REGISTRATION}
]

over_theme = {'txc_inactive': 'black', 'menu_background': '#F5B7B1', 'txc_active': 'white', 'option_active': '#CD5C5C'}

chosen_tab = hc.option_bar(
    option_definition=option_data,
    title='',
    key='PrimaryOptionx',
    override_theme=over_theme,
    horizontal_orientation=True)

if chosen_tab == LOGIN:
    login()

elif chosen_tab == REGISTRATION:
    registration()

for i in range(4):
    st.markdown('#')

# ===== SIDEBAR =====

# st.sidebar.image("utils/ChickenAI.png",width=500)

st.sidebar.title("Welcome to QPID!")
st.sidebar.image("utils/logo.png", width=50)
st.sidebar.markdown("**QPID** is a dating app, where you can find your perfect match based on your interests!")
