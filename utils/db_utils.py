from mysql.connector import Error
from utils.db_connection import connect2db
import pandas as pd


def load_likes_dislikes(user_id):
    df = pd.read_sql(f"SELECT ID_other, like_dislike from likes WHERE ID = '{user_id}'", connect2db())

    return df
