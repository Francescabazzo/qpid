import streamlit as st
import hydralit_components as hc

st.set_page_config(
    page_title='QPID - Homepage',
    page_icon="utils/logo.png",
    initial_sidebar_state="expanded"
)

# This imports must be located here (after Streamlit page configuration) due to Streamlit policies (set_page_config must be the first statement)
# The comments next to the two lines are used for avoiding errors to be thrown by smoke tests that require the imports to be on top of the document
from pages.login.login import login  # noqa: E402
from pages.login.registration import registration  # noqa: E402

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

# Just a shortcut for introducing a vertical space
for i in range(4):
    st.markdown('#')

# ===== SIDEBAR =====

st.sidebar.title("Welcome to QPID!")
st.sidebar.image("utils/logo.png", width=50)
st.sidebar.markdown("**QPID** is a dating app, where you can find your perfect match based on your interests!")
