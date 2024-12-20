import streamlit as st
from streamlit_folium import st_folium
import folium

import pandas as pd
from mysql.connector import Error
from utils.db_connection import connect2db

from utils.converters import gender_text2num


def load_from_db():
    try:
        df = pd.read_sql(f"SELECT * from profiles WHERE ID='{st.session_state['user_ID']}'", connect2db())

        return df.iloc[0]
    except Error as e:
        st.error(f"An error occurred while reading data from database: {e}", icon="❌")

def load_to_db(data):
    conn = connect2db()
    cursor = conn.cursor()

    # todo CYBERSEC: castare a INT + castare FLOAT lat/lon + check checkbox + regex per nome
    # todo + Regex EDI per bio

    try:
        query = (f"UPDATE profiles SET "
                 f"name='{data['name']}',"
                 f"bio='{data['bio']}',"
                 f"gender='{gender_text2num(data['gender'])}',"
                 f"age='{data['age']}',"
                 f"longitude='{data['longitude']}',"
                 f"latitude='{data['latitude']}',"
                 f"attractiveness='{data['attractiveness']}',"
                 f"sincerity='{data['sincerity']}',"
                 f"intelligence='{data['intelligence']}',"
                 f"funniness='{data['funniness']}',"
                 f"ambition='{data['ambition']}',"
                 f"sports='{data['sports']}',"
                 f"tv_sports='{data['tv_sports']}',"
                 f"exercise='{data['exercise']}',"
                 f"dining='{data['dining']}',"
                 f"art='{data['art']}',"
                 f"hiking='{data['hiking']}',"
                 f"gaming='{data['gaming']}',"
                 f"clubbing='{data['clubbing']}',"
                 f"reading='{data['reading']}',"
                 f"tv='{data['tv']}',"
                 f"theater='{data['theater']}',"
                 f"movies='{data['movies']}',"
                 f"music='{data['music']}',"
                 f"shopping='{data['shopping']}',"
                 f"yoga='{data['yoga']}'"
                 f"WHERE ID='{st.session_state['user_ID']}'")

        cursor.execute(query)
        conn.commit()

        st.success("Your profile was correctly updated")
    except Error as e:
        st.error(f"An error occurred while updating your profile: {e}", icon="❌")
    finally:
        cursor.close()
        conn.close()

def input_me():
    data = {}

    user = load_from_db()

    st.header("My Profile:")

    cur_photo = st.image("utils/profile_pic.png", width=100)

    data['name'] = st.text_input("Name", key="name", placeholder="Enter your first name", value=user['name'])

    data['bio'] = st.text_area("Enter a short bio:", key="bio", height=100, placeholder=' Tell us about yourself...',
                       value=user['bio'])

    # photo = st.file_uploader("Upload your photograph", key="photo" type=["jpg", "png"])
    # if not photo:
    #    photo = None

    st.subheader("Personal information")

    tab1, tab2 = st.columns(2, gap='large')

    with tab1:
        data['gender'] = st.radio("Gender", ["Male", "Female", ":rainbow[Other]"], key="gender",
                          index=((int(user['gender']) - 1) if user['gender'] else 0))

        data['age'] = st.number_input("Age", key="age", min_value=18, max_value=99, step=1,
                              value=(user['age'] if (user['age']) else 30))

        st.caption("Where do you live?")

        data['longitude'] = user['longitude'] if user['longitude'] else None
        data['latitude'] = user['latitude'] if user['latitude'] else None

        geo_map = folium.Map(
            location=[data['latitude'] if data['latitude'] else 46,
                      data['longitude'] if data['longitude'] else 13],
            zoom_start=9)
        geo_map.add_child(folium.LatLngPopup())

        if data['latitude'] and data['longitude']:
            folium.Marker(
                location=[data['latitude'], data['longitude']],
                popup=f"Latitude: {data['latitude']}, Longitude: {data['longitude']}"
            ).add_to(geo_map)

        city = st_folium(geo_map, width=500, height=500)

        if city.get("last_clicked"):
            data['latitude']  = city["last_clicked"]["lat"]
            data['longitude'] = city["last_clicked"]["lng"]

    with tab2:
        st.text("Rate yourself about...")

        data['attractiveness'] = st.slider("Attractiveness", key="attractiveness", min_value=1, max_value=10,
                                   value=(user['attractiveness'] if user['attractiveness'] else 5), step=1)
        data['sincerity'] = st.slider("Sincerity", key="sincerity", min_value=1, max_value=10,
                              value=(user['sincerity'] if user['sincerity'] else 5), step=1)
        data['intelligence'] = st.slider("Intelligence", key="intelligence", min_value=1, max_value=10,
                                 value=(user['intelligence'] if user['intelligence'] else 5), step=1)
        data['funniness'] = st.slider("Funniness", key="funniness", min_value=1, max_value=10,
                              value=(user['funniness'] if user['funniness'] else 5), step=1)
        data['ambition'] = st.slider("Ambition", key="ambition", min_value=1, max_value=10,
                             value=(user['ambition'] if user['ambition'] else 5), step=1)

    st.divider()

    st.subheader("Your interests")

    data['sports'] = st.slider("Sports", key="sports", min_value=1, max_value=10, value=(user['sports'] if user['sports'] else 5),
                       step=1)
    data['tv_sports'] = st.slider("TV Sports", key="tv_sports", min_value=1, max_value=10,
                          value=(user['tv_sports'] if user['tv_sports'] else 5), step=1)
    data['exercise'] = st.slider("Exercise", key="exercise", min_value=1, max_value=10, value=(user['exercise'] if user['exercise'] else 5),
                         step=1)
    data['dining'] = st.slider("Dining", key="dining", min_value=1, max_value=10, value=(user['dining'] if user['dining'] else 5),
                       step=1)
    data['art'] = st.slider("Art", key="art", min_value=1, max_value=10, value=(user['art'] if user['art'] else 5), step=1)
    data['hiking'] = st.slider("Hiking", key="hiking", min_value=1, max_value=10, value=(user['hiking'] if user['hiking'] else 5),
                       step=1)
    data['gaming'] = st.slider("Gaming", key="gaming", min_value=1, max_value=10, value=(user['gaming'] if user['gaming'] else 5),
                       step=1)
    data['clubbing'] = st.slider("Clubbing", key="clubbing", min_value=1, max_value=10, value=(user['clubbing'] if user['clubbing'] else 5),
                         step=1)
    data['reading'] = st.slider("Reading", key="reading", min_value=1, max_value=10, value=(user['reading'] if user['reading'] else 5),
                        step=1)
    data['tv'] = st.slider("TV", key="tv", min_value=1, max_value=10, value=(user['tv'] if user['tv'] else 5), step=1)
    data['theater'] = st.slider("Theater", key="theater", min_value=1, max_value=10, value=(user['theater'] if user['theater'] else 5),
                        step=1)
    data['movies'] = st.slider("Movies", key="movies", min_value=1, max_value=10, value=(user['movies'] if user['movies'] else 5),
                       step=1)
    data['music'] = st.slider("Clubbing", key="music", min_value=1, max_value=10, value=(user['music'] if user['music'] else 5),
                      step=1)
    data['shopping'] = st.slider("Shopping", key="shopping", min_value=1, max_value=10, value=(user['shopping'] if user['shopping'] else 5),
                         step=1)
    data['yoga'] = st.slider("Yoga", key="yoga", min_value=1, max_value=10, value=(user['yoga'] if user['yoga'] else 5), step=1)

    # todo CAMBIARE PARAMETRI
    if data['name'] and data['bio'] and data['latitude'] and data['longitude']:
        button = False
    else:
        button = True

    if st.button("Save", use_container_width=True, disabled=button):
        load_to_db(data)
