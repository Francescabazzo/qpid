import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd

from utils.db_connection import connect2db
from utils.converters import gender_num2text
from utils.utils import calcLatLonRange
from backend.backend import get_matches

st.set_page_config(
    page_title='QPID - Matches',
    page_icon="utils/logo.png",
    initial_sidebar_state="expanded"
)



def loadMe():
    df = pd.read_sql(f"SELECT * from full_profiles WHERE ID='{st.session_state['user_ID']}'", connect2db())

    return df

def loadProfiles(user):
    user = user.iloc[0]
    query = f"SELECT * FROM full_profiles WHERE ID > 0 "  # ID > 0 serve solo da placeholder per poi concatenare AND
    if user['age_flag_other'] == 1:
        query += f"AND age >= {user['age_other'] - user['age_radius_other']} AND age <= {user['age_other'] + user['age_radius_other']} "

    if user['distance_flag_other'] == 1:
        lat_min, lat_max, lon_min, lon_max = calcLatLonRange(user['latitude'], user['longitude'],
                                                             user['distance_km_other'])
        query += f"AND latitude >= {lat_min} AND latitude <= {lat_max} AND longitude >= {lon_min} AND longitude <= {lon_max} "

    # GENERI
    cases = {
        ('1', '1'): f"AND ((gender = '1' AND gender_other = '1') OR (gender = '1' AND gender_other = '3'))",
        ('1', '2'): f"AND ((gender = '2' AND gender_other = '1') OR (gender = '2' AND gender_other = '3'))",
        ('1','3'): f"AND ((gender = '1' AND gender_other = '1') OR (gender = '2' AND gender_other = '1')OR (gender = '3' AND gender_other = '1')OR (gender = '1' AND gender_other = '3')OR (gender = '2' AND gender_other = '3')OR (gender = '3' AND gender_other = '3'))",
        ('2', '1'): f"AND ((gender = '1' AND gender_other = '2') OR (gender = '1' AND gender_other = '3'))",
        ('2', '2'): f"AND ((gender = '2' AND gender_other = '2') OR (gender = '2' AND gender_other = '3'))",
        ('2', '3'): f"AND ((gender = '1' AND gender_other = '2') OR (gender = '2' AND gender_other = '2')OR (gender = '3' AND gender_other = '2')OR (gender = '1' AND gender_other = '3')OR (gender = '2' AND gender_other = '3')OR (gender = '3' AND gender_other = '3'))",
        ('3', '1'): f"AND (gender = '1' AND gender_other = '3')",
        ('3', '2'): f"AND (gender = '2' AND gender_other = '3')",
        ('3', '3'): f"AND ((gender = '1' AND gender_other = '3')OR (gender = '2' AND gender_other = '3')OR (gender = '3' AND gender_other = '3'))",
    }

    query += cases.get((user['gender'], user['gender_other']), "")

    df = pd.read_sql(query, connect2db())

    return df

def loadMatches(matches):
    list = ', '.join(map(str, matches))

    df = pd.read_sql(f"SELECT * from full_profiles WHERE ID IN ({list})", connect2db())

    return df

@st.dialog("User details", width="large")
def user_details(user):
    st.header(user['name'])

    tab1, tab2 = st.columns(2, gap='large')

    with tab1:
        st.subheader("Personal Evaluation")
        st.write(f"**- Attractiveness**: {user['attractiveness']}")
        st.write(f"**- Sincerity**: {user['sincerity']}")
        st.write(f"**- Intelligence**: {user['intelligence']}")
        st.write(f"**- Funniness**: {user['funniness']}")
        st.write(f"**- Ambition**: {user['ambition']}")

    with tab2:
        st.subheader("Interests")
        st.write(f"**-Sports**: {user['sports']}")
        st.write(f"**-TV Sports**: {user['tv_sports']}")
        st.write(f"**-Exercise**: {user['exercise']}")
        st.write(f"**-Dining**: {user['dining']}")
        st.write(f"**-Art**: {user['art']}")
        st.write(f"**-Hiking**: {user['hiking']}")
        st.write(f"**-Gaming**: {user['gaming']}")
        st.write(f"**-Clubbing**: {user['clubbing']}")
        st.write(f"**-Reading**: {user['reading']}")
        st.write(f"**-TV**: {user['tv']}")
        st.write(f"**-Theater**: {user['theater']}")
        st.write(f"**-Movies**: {user['movies']}")
        st.write(f"**-Music**: {user['music']}")
        st.write(f"**-Shopping**: {user['shopping']}")
        st.write(f"**-Yoga**: {user['yoga']}")


def profile_card(user):
    with st.expander(f"{user['name']}", expanded=True):
        tab1, tab2 = st.columns([1, 2], gap='large')

        with tab1:
            st.image("utils/profile_pic.png", width=100)

        with tab2:
            st.write(f"**Name**: {user['name']}")
            st.write(f"**Age**: {user['age']}")
            st.write(f"**Gender**: {gender_num2text(user['gender'])}")
            st.write(f"**Bio**: *{user['bio']}*")

        geo_map = folium.Map(location=[user['latitude'], user['longitude']], zoom_start=9)
        folium.Marker(location=[user['latitude'], user['longitude']]).add_to(geo_map)
        st_folium(geo_map, width=700, height=200)

        st.divider()

        btn1, btn2, btn3 = st.columns([2, 1, 1], gap='large')

        with btn1:
            if st.button("More Details", icon="🔍", key=user['ID']):
                user_details(user)

        with btn2:
            if st.button("LIKE", icon="👍", key=f"like_{user['ID']}"):
                st.balloons()

        with btn3:
            if st.button("DISLIKE", icon="👎", key=f"dislike_{user['ID']}"):
                st.snow()


def find_matches():
    df_me = loadMe()
    df_intos = loadProfiles(df_me)

    #df = pd.read_sql("SELECT * FROM profiles WHERE ID <= 5", connect2db())

    matches = get_matches(df_intos, df_me)

    df_matches = loadMatches(matches)

    for index, row in df_matches.iterrows():
        profile_card(row)

def callback() :
    st.session_state['matches_found'] = True

if 'user_login' not in st.session_state:
    st.warning("You must log in to continue!", icon="⚠️")

elif 'matches_found' not in st.session_state:
    with st.form(key='matches_form'):
        submit_button = st.form_submit_button(label='Find Matches', on_click=callback())
else:
    st.header("Matching Profiles")
    st.text("Here you can find your 5 best matches!")

    find_matches()
