from utils.db_connection import connect2db_NEW

import pandas as pd


def load_likes_dislikes(user_id):
    with connect2db_NEW() as conn:
        df = pd.read_sql(f"SELECT ID_other, like_dislike, is_match from likes_bidirectional WHERE ID = '{user_id}'", conn)

    return df

def load_profiles_from_ids(ids):
    ids_list = ', '.join(map(str, ids))

    with connect2db_NEW() as conn:
        df = pd.read_sql(
        f"SELECT * from full_profiles WHERE ID IN ({ids_list}) ORDER BY CASE ID {' '.join([f'WHEN {_id} THEN {i}' for i, _id in enumerate(ids)])} ELSE {len(ids)} END",
        conn)

    return df