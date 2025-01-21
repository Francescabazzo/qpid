import streamlit as st
from streamlit_cookies_controller import CookieController

from utils.converters import gender_text2num, boolean_text2num, pronoun_text2num
from utils.logger import log
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError as exc
import pandas as pd

from utils.db.connection import connect2db
from utils.utils import calc_lat_lon_range


# ========== LOGIN ==========

def login(_username, _password):
    cookie = CookieController()

    with connect2db() as conn:
        try:
            query = f"SELECT ID, username from users WHERE username='{_username}' AND password='{_password}'"

            users = conn.execute(text(query)).fetchall()

            if len(users):
                cookie.set('user_login', _username)
                cookie.set('user_ID', users[0][0])

                log("Log-IN", 0)
            else:
                st.error("Wrong username or password!", icon="❌")
        except exc as e:
            st.error(f"An error occurred while reading data from database: {e}", icon="❌")

            log(f"LOG-IN of {st.session_state['username']} ERROR: {e}", 2)


# ========== REGISTRATION ==========

def registration(_username, _password, _email):
    with connect2db() as conn:
        try:
            query = f"INSERT INTO users SET username='{_username}', password='{_password}', email='{_email}'"
            conn.execute(text(query))

            # Creates entries in the other DB tables (due to unavailability of Triggers)
            query = f"SELECT ID FROM users WHERE username='{_username}'"
            user_id = conn.execute(text(query)).fetchall()[0][0]

            query2 = f"INSERT INTO profiles SET ID='{user_id}'"
            query3 = f"INSERT INTO intos SET ID='{user_id}'"
            conn.execute(text(query2))
            conn.execute(text(query3))

            conn.commit()

            # -----------

            st.success("The new account has been created!", icon="💚")

            log(f"REGISTRATION of user <{_username}>", 0)
        except exc as e:
            conn.rollback()
            st.error(f"An error occurred while inserting data into the database: {e}", icon="❌")

            log(f"REGISTRATION of user <{_username}> ERROR: {e}", 2)


# ========== INTOS ==========

def load_intos(_id):
    with connect2db() as conn:
        try:
            df = pd.read_sql(f"SELECT * from intos WHERE ID='{_id}'", conn)

            log("INTOS RETRIEVAL", 0)

            return df.iloc[0]
        except exc as e:
            st.error(f"An error occurred while reading data from database: {e}", icon="❌")

            log(f"INTOS RETRIEVAL ERROR: {e}", 2)


def update_intos(_id, _data):
    with connect2db() as conn:
        try:
            query = (f"UPDATE intos SET "
                     f"gender='{gender_text2num(_data['gender'])}',"
                     f"age='{_data['age']}',"
                     f"age_flag='{boolean_text2num(_data['age_flag'])}',"
                     f"age_radius='{_data['age_radius']}',"
                     f"distance_flag='{boolean_text2num(_data['distance_flag'])}',"
                     f"distance_km='{_data['distance_km']}',"
                     f"attractiveness_important='{_data['attractiveness_important']}',"
                     f"sincerity_important='{_data['sincerity_important']}',"
                     f"intelligence_important='{_data['intelligence_important']}',"
                     f"funniness_important='{_data['funniness_important']}',"
                     f"ambition_important='{_data['ambition_important']}',")

            if not _data['same_interest']:
                query += (f"sports='{_data['sports']}',"
                          f"tv_sports='{_data['tv_sports']}',"
                          f"exercise='{_data['exercise']}',"
                          f"dining='{_data['dining']}',"
                          f"art='{_data['art']}',"
                          f"hiking='{_data['hiking']}',"
                          f"gaming='{_data['gaming']}',"
                          f"clubbing='{_data['clubbing']}',"
                          f"reading='{_data['reading']}',"
                          f"tv='{_data['tv']}',"
                          f"theater='{_data['theater']}',"
                          f"movies='{_data['movies']}',"
                          f"music='{_data['music']}',"
                          f"shopping='{_data['shopping']}',"
                          f"yoga='{_data['yoga']}', ")
            else:
                query += (f"sports=(SELECT sports FROM profiles WHERE ID ='{_id}'),"
                          f"tv_sports=(SELECT tv_sports FROM profiles WHERE ID ='{_id}'),"
                          f"exercise=(SELECT exercise FROM profiles WHERE ID ='{_id}'),"
                          f"dining=(SELECT dining FROM profiles WHERE ID ='{_id}'),"
                          f"art=(SELECT art FROM profiles WHERE ID ='{_id}'),"
                          f"hiking=(SELECT hiking FROM profiles WHERE ID ='{_id}'),"
                          f"gaming=(SELECT gaming FROM profiles WHERE ID ='{_id}'),"
                          f"clubbing=(SELECT clubbing FROM profiles WHERE ID ='{_id}'),"
                          f"reading=(SELECT reading FROM profiles WHERE ID ='{_id}'),"
                          f"tv=(SELECT tv FROM profiles WHERE ID ='{_id}'),"
                          f"theater=(SELECT theater FROM profiles WHERE ID ='{_id}'),"
                          f"movies=(SELECT movies FROM profiles WHERE ID ='{_id}'),"
                          f"music=(SELECT music FROM profiles WHERE ID ='{_id}'),"
                          f"shopping=(SELECT shopping FROM profiles WHERE ID ='{_id}'),"
                          f"yoga=(SELECT yoga FROM profiles WHERE ID ='{_id}'),")

            query += (f"same_interest='{boolean_text2num(_data['same_interest'])}' "
                      f"WHERE ID={_id} ")

            conn.execute(text(query))
            conn.commit()

            st.success("Your intos were correctly updated")

            log("INTOS UPDATE", 0)
        except exc as e:
            conn.rollback()
            st.error(f"An error occurred while updating your intos: {e}", icon="❌")

            log(f"INTOS UPDATE ERROR: {e}", 2)


# ========== PROFILE ==========

def load_profile(_id):
    with connect2db() as conn:
        try:
            df = pd.read_sql(f"SELECT * from full_profiles WHERE ID='{_id}'", conn)

            log("PROFILE RETRIEVAL", 0)

            return df.iloc[0]
        except exc as e:
            st.error(f"An error occurred while reading data from database: {e}", icon="❌")

            log(f"PROFILE RETRIEVAL ERROR: {e}", 2)


def update_profile(_id, _data):
    with connect2db() as conn:
        try:
            query = (f"UPDATE profiles SET "
                     f"name='{_data['name']}',"
                     f"bio='{_data['bio']}',"
                     f"gender='{pronoun_text2num(_data['gender'])}',"
                     f"age='{_data['age']}',"
                     f"longitude='{_data['longitude']}',"
                     f"latitude='{_data['latitude']}',"
                     f"attractiveness='{_data['attractiveness']}',"
                     f"sincerity='{_data['sincerity']}',"
                     f"intelligence='{_data['intelligence']}',"
                     f"funniness='{_data['funniness']}',"
                     f"ambition='{_data['ambition']}',"
                     f"sports='{_data['sports']}',"
                     f"tv_sports='{_data['tv_sports']}',"
                     f"exercise='{_data['exercise']}',"
                     f"dining='{_data['dining']}',"
                     f"art='{_data['art']}',"
                     f"hiking='{_data['hiking']}',"
                     f"gaming='{_data['gaming']}',"
                     f"clubbing='{_data['clubbing']}',"
                     f"reading='{_data['reading']}',"
                     f"tv='{_data['tv']}',"
                     f"theater='{_data['theater']}',"
                     f"movies='{_data['movies']}',"
                     f"music='{_data['music']}',"
                     f"shopping='{_data['shopping']}',"
                     f"yoga='{_data['yoga']}'"
                     f"WHERE ID='{_id}'")

            conn.execute(text(query))

            if _data['same_interests']:
                query = (f"UPDATE intos SET "
                         f"sports='{_data['sports']}',"
                         f"tv_sports='{_data['tv_sports']}',"
                         f"exercise='{_data['exercise']}',"
                         f"dining='{_data['dining']}',"
                         f"art='{_data['art']}',"
                         f"hiking='{_data['hiking']}',"
                         f"gaming='{_data['gaming']}',"
                         f"clubbing='{_data['clubbing']}',"
                         f"reading='{_data['reading']}',"
                         f"tv='{_data['tv']}',"
                         f"theater='{_data['theater']}',"
                         f"movies='{_data['movies']}',"
                         f"music='{_data['music']}',"
                         f"shopping='{_data['shopping']}',"
                         f"yoga='{_data['yoga']}'"
                         f"WHERE ID='{_id}'")

                conn.execute(text(query))

            conn.commit()

            st.success("Your profile was correctly updated")

            log("PROFILE UPDATE", 0)
        except exc as e:
            conn.rollback()
            st.error(f"An error occurred while updating your profile: {e}", icon="❌")

            log(f"PROFILE UPDATE ERROR: {e}", 2)


# ========== FULL PROFILE ==========

def load_full_profile(_id):
    with connect2db() as conn:
        try:
            df = pd.read_sql(f"SELECT * from full_profiles WHERE ID='{_id}'", conn)

            log("PERSONAL PROFILE LOADING", 0)

            return df
        except exc as e:
            st.error(f"An error occurred while reading personal profile: {e}", icon="❌")

            log(f"PERSONAL PROFILE LOADING ERROR: {e}", 2)


# ========== CANDIDATE PROFILES ==========

def load_candidates(_id, _user, _likes_dislikes):
    _user = _user.iloc[0]

    query = f"SELECT * FROM full_profiles WHERE ID <> {_id} "

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
        try:
            df = pd.read_sql(query, conn)

            log("CANDIDATE PROFILES LOADING", 0)
        except exc as e:
            st.error(f"An error occurred while reading candidate profiles: {e}", icon="❌")

            log(f"CANDIDATE PROFILES LOADING ERROR: {e}", 2)

    # Filters out already liked and disliked profiles
    dislikes = _likes_dislikes[_likes_dislikes['like_dislike'] == 0]['ID_other'].tolist()
    likes = _likes_dislikes[_likes_dislikes['like_dislike'] == 1]['ID_other'].tolist()

    df = df[~df['ID'].isin(dislikes)]
    df = df[~df['ID'].isin(likes)]

    return df


# ========== LIKES/DISLIKES ==========


def load_likes_dislikes(_id):
    with connect2db() as conn:
        df = pd.read_sql(f"SELECT ID_other, like_dislike, is_match from likes_bidirectional WHERE ID = '{_id}'",
                         conn)

    return df


def load_profiles_from_ids(_ids):
    ids_list = ', '.join(map(str, _ids))

    with connect2db() as conn:
        df = pd.read_sql(
            f"SELECT * from full_profiles WHERE ID IN ({ids_list}) ORDER BY CASE ID {' '.join([f'WHEN {_id} THEN {i}' for i, _id in enumerate(_ids)])} ELSE {len(_ids)} END",
            conn)

    return df


def set_like_dislike(_id, _id_other, _like_dislike):
    with connect2db() as conn:
        try:
            query = f"INSERT INTO likes SET ID='{_id}', ID_other='{_id_other}', like_dislike='{_like_dislike}'"

            conn.execute(text(query))
            conn.commit()

            log(f"LIKE DISLIKE INSERTING ({_like_dislike})", 0)

            if _like_dislike:
                st.balloons()
            else:
                st.snow()
        except exc as e:
            conn.rollback()
            st.error(f"An error occurred while updating your likes/dislikes in the database: {e}", icon="❌")

            log(f"LIKE DISLIKE INSERTING ({_like_dislike}) ERROR: {e}", 0)
