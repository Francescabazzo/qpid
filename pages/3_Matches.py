import streamlit as st
from streamlit_cookies_controller import CookieController
from streamlit_folium import st_folium
import folium
import pandas as pd
from utils.db_connection import connect2db
from sqlalchemy.exc import DBAPIError as exc
from sqlalchemy import text
from utils.converters import pronoun_num2text
from utils.utils import calc_lat_lon_range
from utils.db_utils import load_likes_dislikes, load_profiles_from_ids
from backend.importer import load_pickles

st.set_page_config(
    page_title='QPID - Matches',
    page_icon="utils/images/logo.png",
    initial_sidebar_state="expanded"
)

# ====================

cookie = CookieController()

calculate_scores, get_matches = load_pickles()


# ====================

# ===== UTILS FUNCTIONS =====

def load_personal_profile():
    with connect2db() as conn:
        df = pd.read_sql(f"SELECT * from full_profiles WHERE ID='{cookie.get('user_ID')}'", conn)

    return df


def load_profiles(_user, _likes_dislikes):
    _user = _user.iloc[0]

    query = f"SELECT * FROM full_profiles WHERE ID <> {cookie.get('user_ID')} "

    # Filters out profiles out-of-age-range
    if _user['age_flag_other'] == 1:
        query += f"AND age >= {_user['age_other'] - _user['age_radius_other']} AND age <= {_user['age_other'] + _user['age_radius_other']} "

    # Filters out profiles out-of-distance-range
    if _user['distance_flag_other'] == 1:
        lat_min, lat_max, lon_min, lon_max = calc_lat_lon_range(_user['latitude'], _user['longitude'],
                                                                _user['distance_km_other'])
        query += f"AND latitude >= {lat_min} AND latitude <= {lat_max} AND longitude >= {lon_min} AND longitude <= {lon_max} "

    # Selects only the profiles compatible with the gender and sexual orientation
    cases = {
        ('1', '1'): "AND ((gender = '1' AND gender_other = '1') OR (gender = '1' AND gender_other = '3'))",
        ('1', '2'): "AND ((gender = '2' AND gender_other = '1') OR (gender = '2' AND gender_other = '3'))",
        ('1',
         '3'): "AND ((gender = '1' AND gender_other = '1') OR (gender = '2' AND gender_other = '1')OR (gender = '3' AND gender_other = '1')OR (gender = '1' AND gender_other = '3')OR (gender = '2' AND gender_other = '3')OR (gender = '3' AND gender_other = '3'))",
        ('2', '1'): "AND ((gender = '1' AND gender_other = '2') OR (gender = '1' AND gender_other = '3'))",
        ('2', '2'): "AND ((gender = '2' AND gender_other = '2') OR (gender = '2' AND gender_other = '3'))",
        ('2',
         '3'): "AND ((gender = '1' AND gender_other = '2') OR (gender = '2' AND gender_other = '2')OR (gender = '3' AND gender_other = '2')OR (gender = '1' AND gender_other = '3')OR (gender = '2' AND gender_other = '3')OR (gender = '3' AND gender_other = '3'))",
        ('3', '1'): "AND (gender = '1' AND gender_other = '3')",
        ('3', '2'): "AND (gender = '2' AND gender_other = '3')",
        ('3',
         '3'): "AND ((gender = '1' AND gender_other = '3')OR (gender = '2' AND gender_other = '3')OR (gender = '3' AND gender_other = '3'))",
    }

    query += cases.get((_user['gender'], _user['gender_other']), "")

    with connect2db() as conn:
        df = pd.read_sql(query, conn)

    # Filters out already liked and disliked profiles
    dislikes = _likes_dislikes[_likes_dislikes['like_dislike'] == 0]['ID_other'].tolist()
    likes = _likes_dislikes[_likes_dislikes['like_dislike'] == 1]['ID_other'].tolist()

    df = df[~df['ID'].isin(dislikes)]
    df = df[~df['ID'].isin(likes)]

    return df


def build_profile_card(_user, _match_score):
    with st.expander(f"{_user['name']}", expanded=True):
        st.progress(text=f"Match Score: {_match_score:.1f} %", value=int(_match_score))

        tab1, tab2 = st.columns([1, 2], gap='large')

        with tab1:
            st.image("utils/images/profile_pic.png", width=100)

        with tab2:
            st.write(f"**Name**: {_user['name']}")
            st.write(f"**Age**: {_user['age']}")
            st.write(f"**Pronouns**: {pronoun_num2text(_user['gender'])}")
            st.write(f"**Bio**: *{_user['bio']}*")

        geo_map = folium.Map(location=[_user['latitude'], _user['longitude']], zoom_start=7, zoom_control=False,
                             dragging=False)
        folium.Marker(location=[_user['latitude'], _user['longitude']]).add_to(geo_map)
        st_folium(geo_map, width=700, height=200)

        st.divider()

        btn1, btn2, btn3 = st.columns([2, 1, 1], gap='large')

        with btn1:
            if st.button("More Details", icon="🔍", key=_user['ID']):
                user_details(_user)

        with btn2:
            if st.button("LIKE", icon="👍", key=f"like_{_user['ID']}"):
                set_like_dislike(cookie.get('user_ID'), _user['ID'], 1)

        with btn3:
            if st.button("DISLIKE", icon="👎", key=f"dislike_{_user['ID']}"):
                set_like_dislike(cookie.get('user_ID'), _user['ID'], 0)


def find_matches(_personal_profile):
    likes_dislikes = load_likes_dislikes(cookie.get('user_ID'))
    candidate_profiles = load_profiles(_personal_profile, likes_dislikes)

    if candidate_profiles.empty:
        st.warning("No matches found. Maybe you might want to change your preferences...")
        st.snow()
    else:
        if candidate_profiles.size <= 5:
            matches = candidate_profiles
        else:
            matches = get_matches(candidate_profiles, _personal_profile)

        df_matches = load_profiles_from_ids(matches)
        accuracy_scores = calculate_scores(df_matches, _personal_profile)

        for index, row in df_matches.iterrows():
            build_profile_card(row, accuracy_scores[index])


def set_like_dislike(id_personal_profile, _id_other_profile, _like_dislike):
    with connect2db() as conn:
        try:
            query = f"INSERT INTO likes SET ID='{id_personal_profile}', ID_other='{_id_other_profile}', like_dislike='{_like_dislike}'"

            conn.execute(text(query))
            conn.commit()

            if _like_dislike:
                st.balloons()
            else:
                st.snow()
        except exc as e:
            conn.rollback()
            st.error(f"An error occurred while updating your likes/dislikes in the database: {e}", icon="❌")


# ===== END of UTILS FUNCTIONS =====

# ===== MODAL =====

@st.dialog("User details", width="large")
def user_details(_user):
    st.header(_user['name'])

    tab1, tab2 = st.columns(2, gap='large')

    with tab1:
        st.subheader("Personal Evaluation")
        st.write(f"**- Attractiveness**: {_user['attractiveness']}")
        st.write(f"**- Sincerity**: {_user['sincerity']}")
        st.write(f"**- Intelligence**: {_user['intelligence']}")
        st.write(f"**- Funniness**: {_user['funniness']}")
        st.write(f"**- Ambition**: {_user['ambition']}")

    with tab2:
        st.subheader("Interests")
        st.write(f"**-Sports**: {_user['sports']}")
        st.write(f"**-TV Sports**: {_user['tv_sports']}")
        st.write(f"**-Exercise**: {_user['exercise']}")
        st.write(f"**-Dining**: {_user['dining']}")
        st.write(f"**-Art**: {_user['art']}")
        st.write(f"**-Hiking**: {_user['hiking']}")
        st.write(f"**-Gaming**: {_user['gaming']}")
        st.write(f"**-Clubbing**: {_user['clubbing']}")
        st.write(f"**-Reading**: {_user['reading']}")
        st.write(f"**-TV**: {_user['tv']}")
        st.write(f"**-Theater**: {_user['theater']}")
        st.write(f"**-Movies**: {_user['movies']}")
        st.write(f"**-Music**: {_user['music']}")
        st.write(f"**-Shopping**: {_user['shopping']}")
        st.write(f"**-Yoga**: {_user['yoga']}")


# ===== END of MODAL =====

# ===== CALLBACK =====

def callback():
    st.session_state['matches_found'] = True


# ===== END of CALLBACK =====

if not cookie.get('user_login'):
    st.warning("You must log in to continue!", icon="⚠️")

else:
    st.header("Matching Profiles")
    st.text("Here you can find your 5 best matches, among all the users that you have not seen yet!")
    st.markdown(
        "For each profile, you can set a **LIKE** or a **DISLIKE**: "
        "\n - You can use a **LIKE** to inform the other profile that you are interested in it: if the like is mutual, you can start chat together! "
        "\n - You can use a **DISLIKE** to remove a profile from the list: at the next search, this profile will not be proposed to you anymore!")

    st.markdown(
        "Please notice that the **match score** could not follow the descending order of the matches proposal, due to the internal calculation mechanism.")
    personal_profile = load_personal_profile()

    if not personal_profile.iloc[0]['gender'] or not personal_profile.iloc[0]['gender_other']:
        st.warning("You must complete your profile before proceeding. Remember also to confirm your intos!")
    elif 'matches_found' not in st.session_state or not st.session_state['matches_found']:
        with st.form(key='matches_form'):
            submit_button = st.form_submit_button(label='Find Matches', on_click=callback, type="primary", icon="😍",
                                                  use_container_width=True)
    else:
        find_matches(personal_profile)
        with st.form(key='matches_form_reload'):
            submit_button = st.form_submit_button(label='Reload Matches', on_click=callback, type="primary", icon="🔃",
                                                  use_container_width=True)
