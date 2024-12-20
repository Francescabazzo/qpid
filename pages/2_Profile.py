import hydralit_components as hc
import streamlit as st
# import streamlit_analytics
# from streamlit_modal import Modal
# import streamlit_lottie
import time
import json

# from utils.components import footer_style, footer

from pages.navigation.input_me import input_me
from pages.navigation.input_other import input_other

import os

st.set_page_config(
    page_title='QPID - Profile',
    page_icon="utils/logo.png",
    initial_sidebar_state="expanded"
)

if 'user_login' not in st.session_state:
    st.warning("You must log in to continue!", icon="⚠️")
else:
    # Footer

    # st.markdown(footer_style, unsafe_allow_html=True)

    # NavBar

    INPUT_ME = 'My Profile'
    INPUT_OTHER = 'My Interests'

    tabs = [
        INPUT_ME,
        INPUT_OTHER
    ]

    option_data = [
        {'icon': "📃", 'label': INPUT_ME},
        {'icon': "💭", 'label': INPUT_OTHER}

    ]

    over_theme = {'txc_inactive': 'black', 'menu_background': '#F5B7B1', 'txc_active': 'white',
                  'option_active': '#CD5C5C'}
    font_fmt = {'font-class': 'h3', 'font-size': '50%'}

    chosen_tab = hc.option_bar(
        option_definition=option_data,
        title='',
        key='PrimaryOptionx',
        override_theme=over_theme,
        horizontal_orientation=True)

    if chosen_tab == INPUT_ME:
        input_me()

    elif chosen_tab == INPUT_OTHER:
        input_other()

    for i in range(4):
        st.markdown('#')

    # st.markdown(footer, unsafe_allow_html=True)
