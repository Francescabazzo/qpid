import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd
from mysql.connector import Error

from utils.db_connection import connect2db
from utils.converters import pronoun_num2text
from utils.utils import calcLatLonRange
from backend.backend import get_matches, calculate_scores
from utils.db_utils import load_likes_dislikes, load_profiles_from_ids

from streamlit_cookies_controller import CookieController

st.set_page_config(
    page_title='QPID - Matches',
    page_icon="utils/logo.png",
    initial_sidebar_state="expanded"
)

cookie = CookieController()


def loadMe():
    df = pd.read_sql(f"SELECT * from full_profiles WHERE ID='{cookie.get('user_ID')}'", connect2db())

    return df


def loadProfiles(user, likes_dislikes):
    user = user.iloc[0]
    query = f"SELECT * FROM full_profiles WHERE ID <> {cookie.get('user_ID')} "
    if user['age_flag_other'] == 1:
        query += f"AND age >= {user['age_other'] - user['age_radius_other']} AND age <= {user['age_other'] + user['age_radius_other']} "

    if user['distance_flag_other'] == 1:
        lat_min, lat_max, lon_min, lon_max = calcLatLonRange(user['latitude'], user['longitude'],
                                                             user['distance_km_other'])
        query += f"AND latitude >= {lat_min} AND latitude <= {lat_max} AND longitude >= {lon_min} AND longitude <= {lon_max} "

    # GENRES
    cases = {
        ('1', '1'): f"AND ((gender = '1' AND gender_other = '1') OR (gender = '1' AND gender_other = '3'))",
        ('1', '2'): f"AND ((gender = '2' AND gender_other = '1') OR (gender = '2' AND gender_other = '3'))",
        ('1',
         '3'): f"AND ((gender = '1' AND gender_other = '1') OR (gender = '2' AND gender_other = '1')OR (gender = '3' AND gender_other = '1')OR (gender = '1' AND gender_other = '3')OR (gender = '2' AND gender_other = '3')OR (gender = '3' AND gender_other = '3'))",
        ('2', '1'): f"AND ((gender = '1' AND gender_other = '2') OR (gender = '1' AND gender_other = '3'))",
        ('2', '2'): f"AND ((gender = '2' AND gender_other = '2') OR (gender = '2' AND gender_other = '3'))",
        ('2',
         '3'): f"AND ((gender = '1' AND gender_other = '2') OR (gender = '2' AND gender_other = '2')OR (gender = '3' AND gender_other = '2')OR (gender = '1' AND gender_other = '3')OR (gender = '2' AND gender_other = '3')OR (gender = '3' AND gender_other = '3'))",
        ('3', '1'): f"AND (gender = '1' AND gender_other = '3')",
        ('3', '2'): f"AND (gender = '2' AND gender_other = '3')",
        ('3',
         '3'): f"AND ((gender = '1' AND gender_other = '3')OR (gender = '2' AND gender_other = '3')OR (gender = '3' AND gender_other = '3'))",
    }

    query += cases.get((user['gender'], user['gender_other']), "")

    df = pd.read_sql(query, connect2db())

    # FILTERS OUT DISLIKES

    dislikes = likes_dislikes[likes_dislikes['like_dislike'] == 0]['ID_other'].tolist()

    return df[~df['ID'].isin(dislikes)]


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


def profile_card(user, accuracy_score, likes_dislikes):
    with st.expander(f"{user['name']}", expanded=True):
        st.progress(text=f"Match Score: {accuracy_score:.1f} %", value=int(accuracy_score))

        tab1, tab2 = st.columns([1, 2], gap='large')

        with tab1:
            st.image("utils/profile_pic.png", width=100)

        with tab2:
            st.write(f"**Name**: {user['name']}")
            st.write(f"**Age**: {user['age']}")
            st.write(f"**Pronouns**: {pronoun_num2text(user['gender'])}")
            st.write(f"**Bio**: *{user['bio']}*")

        geo_map = folium.Map(location=[user['latitude'], user['longitude']], zoom_start=9)
        folium.Marker(location=[user['latitude'], user['longitude']]).add_to(geo_map)
        st_folium(geo_map, width=700, height=200)

        st.divider()

        btn1, btn2, btn3 = st.columns([2, 1, 1], gap='large')

        with btn1:
            if st.button("More Details", icon="🔍", key=user['ID']):
                user_details(user)

        if not likes_dislikes.loc[(likes_dislikes['ID_other'] == user['ID']), 'like_dislike'].empty:
            with btn2:
                st.write(f"You already set a **like** to this profile.")
        else:
            with btn2:
                if st.button("LIKE", icon="👍", key=f"like_{user['ID']}"):
                    set_like_dislike(cookie.get('user_ID'), user['ID'], 1)

            with btn3:
                if st.button("DISLIKE", icon="👎", key=f"dislike_{user['ID']}"):
                    set_like_dislike(cookie.get('user_ID'), user['ID'], 0)


def find_matches(df_me, likes_dislikes):
    df_intos = loadProfiles(df_me, likes_dislikes)

    if df_intos.empty:
        st.warning("No matches found. Maybe you might want to change your preferences...")
        st.snow()
    else:
        if df_intos.size < 5:
            matches = df_intos

        else:
            matches = get_matches(df_intos, df_me)

        df_matches = load_profiles_from_ids(matches)
        accuracy_scores = calculate_scores(df_matches, df_me)

        for index, row in df_matches.iterrows():
            profile_card(row, accuracy_scores[index], likes_dislikes)


def set_like_dislike(id_me, id_other, like_dislike):
    conn = connect2db()
    cursor = conn.cursor()

    try:
        query = f"INSERT INTO likes SET ID='{id_me}', ID_other='{id_other}', like_dislike='{like_dislike}'"

        cursor.execute(query)
        conn.commit()

        if like_dislike:
            st.balloons()
        else:
            st.snow()
    except Error as e:
        st.error(f"An error occurred while updating your likes/dislikes in the database: {e}", icon="❌")
    finally:
        cursor.close()
        conn.close()


def callback():
    st.session_state['matches_found'] = True


if not cookie.get('user_login'):
    st.warning("You must log in to continue!", icon="⚠️")

else:
    st.header("Matching Profiles")
    st.text("Here you can find your 5 best matches, among all the users that you have not seen yet!")
    st.markdown(
        "For each profile, you can set a **LIKE** or a **DISLIKE**: "
        "\n - You can use a **LIKE** to inform the other profile that you are interested in it: if the like is mutual, you can start chat together! "
        "\n - You can use a **DISLIKE** to remove a profile from the list: at the next search, this profile will not be proposed to you anymore!")

    st.markdown("Please notice that the **match score** could not follow the descending order of the matches proposal, due to the internal calculation mechanism.")
    df_me = loadMe()
    likes_dislikes = load_likes_dislikes(cookie.get('user_ID'))

    if not df_me.iloc[0]['gender'] or not df_me.iloc[0]['gender_other']:
        st.warning("You must complete your profile before proceeding. Remember also to confirm your intos!")
    elif 'matches_found' not in st.session_state or not st.session_state['matches_found']:
        with st.form(key='matches_form'):
            submit_button = st.form_submit_button(label='Find Matches', on_click=callback, type="primary", icon="😍",
                                                  use_container_width=True)
    else:
        find_matches(df_me, likes_dislikes)
