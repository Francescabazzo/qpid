import hydralit_components as hc
import streamlit as st

from streamlit_cookies_controller import CookieController
from pages.profile.profile_me import input_me
from pages.profile.profile_intos import input_other

st.set_page_config(
    page_title='QPID - Profile',
    page_icon="utils/logo.png",
    initial_sidebar_state="expanded"
)

cookie = CookieController()



if not cookie.get('user_login') :
    st.warning("You must log in to continue!", icon="⚠️")
else:

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
        input_me(cookie)

    elif chosen_tab == INPUT_OTHER:
        input_other(cookie)

    for i in range(4):
        st.markdown('#')