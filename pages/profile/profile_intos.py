import streamlit as st

import pandas as pd
from mysql.connector import Error
from utils.db_connection import connect2db

from utils.converters import gender_text2num, boolean_text2num

#from streamlit_cookies_controller import CookieController
#cookie = CookieController()

def load_from_db(cookie):
    try:
        df = pd.read_sql(f"SELECT * from intos WHERE ID='{cookie.get('user_ID')}'", connect2db())

        return df.iloc[0]
    except Error as e:
        st.error(f"An error occurred while reading data from database: {e}", icon="❌")


def load_to_db(cookie, data):
    conn = connect2db()
    cursor = conn.cursor()

    try:
        query = (f"UPDATE intos SET "
                 f"gender='{gender_text2num(data['gender'])}',"
                 f"age='{data['age']}',"
                 f"age_flag='{boolean_text2num(data['age_flag'])}',"
                 f"age_radius='{data['age_radius']}',"
                 f"distance_flag='{boolean_text2num(data['distance_flag'])}',"
                 f"distance_km='{data['distance_km']}',"
                 f"attractiveness_important='{data['attractiveness_important']}',"
                 f"sincerity_important='{data['sincerity_important']}',"
                 f"intelligence_important='{data['intelligence_important']}',"
                 f"funniness_important='{data['funniness_important']}',"
                 f"ambition_important='{data['ambition_important']}',")

        if not data['same_interest']:
            query += (f"sports='{data['sports']}',"
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
                      f"yoga='{data['yoga']}', ")
        else:
            query += (f"sports=(SELECT sports FROM profiles WHERE ID ='{cookie.get('user_ID')}'),"
                      f"tv_sports=(SELECT tv_sports FROM profiles WHERE ID ='{cookie.get('user_ID')}'),"
                      f"exercise=(SELECT exercise FROM profiles WHERE ID ='{cookie.get('user_ID')}'),"
                      f"dining=(SELECT dining FROM profiles WHERE ID ='{cookie.get('user_ID')}'),"
                      f"art=(SELECT art FROM profiles WHERE ID ='{cookie.get('user_ID')}'),"
                      f"hiking=(SELECT hiking FROM profiles WHERE ID ='{cookie.get('user_ID')}'),"
                      f"gaming=(SELECT gaming FROM profiles WHERE ID ='{cookie.get('user_ID')}'),"
                      f"clubbing=(SELECT clubbing FROM profiles WHERE ID ='{cookie.get('user_ID')}'),"
                      f"reading=(SELECT reading FROM profiles WHERE ID ='{cookie.get('user_ID')}'),"
                      f"tv=(SELECT tv FROM profiles WHERE ID ='{cookie.get('user_ID')}'),"
                      f"theater=(SELECT theater FROM profiles WHERE ID ='{cookie.get('user_ID')}'),"
                      f"movies=(SELECT movies FROM profiles WHERE ID ='{cookie.get('user_ID')}'),"
                      f"music=(SELECT music FROM profiles WHERE ID ='{cookie.get('user_ID')}'),"
                      f"shopping=(SELECT shopping FROM profiles WHERE ID ='{cookie.get('user_ID')}'),"
                      f"yoga=(SELECT yoga FROM profiles WHERE ID ='{cookie.get('user_ID')}'),")

        query += (f"same_interest='{boolean_text2num(data['same_interest'])}' "
                  f"WHERE ID={cookie.get('user_ID')} ")

        cursor.execute(query)
        conn.commit()

        st.success("Your intos were correctly updated")
    except Error as e:
        st.error(f"An error occurred while updating your intos: {e}", icon="❌")
    finally:
        cursor.close()
        conn.close()


def input_other(cookie):
    data = {}

    intos = load_from_db(cookie)

    st.header("What are you looking for?")

    tab1, tab2 = st.columns(2, gap='medium')

    with tab1:

        data['gender'] = st.radio("Gender", ["Male", "Female", ":rainbow[All]"], key="gender",
                                  index=((int(intos['gender']) - 1) if intos['gender'] else 0))

        data['age'] = st.number_input("Age", key="age", min_value=18, max_value=100, step=1,
                                      value=(intos['age'] if (intos['age']) else 30))

        data['age_flag'] = st.checkbox("Specify a range for age", key="age_flag", value=intos['age_flag'])

        if data['age_flag']:
            data['age_radius'] = st.slider("Age Interval", key="age_radius", min_value=1, max_value=100,
                                           value=(intos['age_radius'] if intos['age_radius'] else 1), step=1)
        else:
            data['age_radius'] = 0

    with tab2:
        data['distance_flag'] = st.checkbox("Partners close to you", key="distance_flag", value=intos['distance_flag'])

        if data['distance_flag']:
            data['distance_km'] = st.slider("MAX Distance in km", key="distance_km", min_value=10, max_value=1000,
                                            value=(intos['distance_km'] if intos['distance_km'] else 10), step=10)
        else:
            data['distance_km'] = 0

    tab1, tab2 = st.columns(2, gap='large')

    with tab1:
        st.subheader("Are those features important for you?")
        st.text("1 means 'Not at all', 5 means 'Definitely yes'")

        data['attractiveness_important'] = st.slider("Attractiveness", key="attractiveness_important", min_value=1,
                                                     max_value=5, value=(
                intos['attractiveness_important'] if intos['attractiveness_important'] else 3), step=1)
        data['sincerity_important'] = st.slider("Sincerity", key="sincerity_important", min_value=1,
                                                max_value=5, value=(
                intos['sincerity_important'] if intos['sincerity_important'] else 3), step=1)
        data['intelligence_important'] = st.slider("Intelligence", key="intelligence_important", min_value=1,
                                                   max_value=5, value=(
                intos['intelligence_important'] if intos['intelligence_important'] else 3), step=1)
        data['funniness_important'] = st.slider("Funniness", key="funniness_important", min_value=1,
                                                max_value=5, value=(
                intos['funniness_important'] if intos['funniness_important'] else 3), step=1)
        data['ambition_important'] = st.slider("Ambition", key="ambition_important", min_value=1,
                                               max_value=5, value=(
                intos['ambition_important'] if intos['ambition_important'] else 3), step=1)

    with tab2:
        st.subheader("What should be the interests of your perfect partner?")

        data['same_interest'] = st.checkbox("Same as mine", key="same_interest", value=intos['same_interest'])

        if not data['same_interest']:
            data['sports'] = st.slider("Sports", key="sports", min_value=1, max_value=10,
                                       value=(intos['sports'] if intos['sports'] else 5), step=1)
            data['tv_sports'] = st.slider("TV Sports", key="tv_sports", min_value=1, max_value=10,
                                          value=(intos['tv_sports'] if intos['tv_sports'] else 5), step=1)
            data['exercise'] = st.slider("Exercise", key="exercise", min_value=1, max_value=10,
                                         value=(intos['exercise'] if intos['exercise'] else 5), step=1)
            data['dining'] = st.slider("Dining", key="dining", min_value=1, max_value=10,
                                       value=(intos['dining'] if intos['dining'] else 5), step=1)
            data['art'] = st.slider("Art", key="art", min_value=1, max_value=10,
                                    value=(intos['art'] if intos['art'] else 5), step=1)
            data['hiking'] = st.slider("Hiking", key="hiking", min_value=1, max_value=10,
                                       value=(intos['hiking'] if intos['hiking'] else 5), step=1)
            data['gaming'] = st.slider("Gaming", key="gaming", min_value=1, max_value=10,
                                       value=(intos['gaming'] if intos['gaming'] else 5), step=1)
            data['clubbing'] = st.slider("Clubbing", key="clubbing", min_value=1, max_value=10,
                                         value=(intos['clubbing'] if intos['clubbing'] else 5), step=1)
            data['reading'] = st.slider("Reading", key="reading", min_value=1, max_value=10,
                                        value=(intos['reading'] if intos['reading'] else 5), step=1)
            data['tv'] = st.slider("TV", key="tv", min_value=1, max_value=10,
                                   value=(intos['tv'] if intos['tv'] else 5), step=1)
            data['theater'] = st.slider("Theater", key="theater", min_value=1, max_value=10,
                                        value=(intos['theater'] if intos['theater'] else 5), step=1)
            data['movies'] = st.slider("Movies", key="movies", min_value=1, max_value=10,
                                       value=(intos['movies'] if intos['movies'] else 5), step=1)
            data['music'] = st.slider("Music", key="music", min_value=1, max_value=10,
                                      value=(intos['music'] if intos['music'] else 5), step=1)
            data['shopping'] = st.slider("Shopping", key="shopping", min_value=1, max_value=10,
                                         value=(intos['shopping'] if intos['shopping'] else 5), step=1)
            data['yoga'] = st.slider("Yoga", key="yoga", min_value=1, max_value=10,
                                     value=(intos['yoga'] if intos['yoga'] else 5), step=1)

    if st.button("Save", use_container_width=True):
        load_to_db(cookie, data)
