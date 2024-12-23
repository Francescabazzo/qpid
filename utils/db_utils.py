from mysql.connector import Error
from utils.db_connection import connect2db
import pandas as pd


def load_likes_dislikes(user_id):
    df = pd.read_sql(f"SELECT ID_other, like_dislike, is_match from likes_bidirectional WHERE ID = '{user_id}'", connect2db())

    return df

def load_profiles_from_ids(ids):
    ids_list = ', '.join(map(str, ids))

    df = pd.read_sql(
        f"SELECT * from full_profiles WHERE ID IN ({ids_list}) ORDER BY CASE ID {' '.join([f'WHEN {_id} THEN {i}' for i, _id in enumerate(ids)])} ELSE {len(ids)} END",
        connect2db())

    return df