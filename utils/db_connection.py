from mysql.connector import connect, Error
import streamlit as st
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine

#@st.cache_resource
def connect2db():
    try:
        # Database: Clever Cloud
        conn = connect(
            host="bxdahcfis71ncmcthutg-mysql.services.clever-cloud.com",
            user="uwywwwp2ws2f97ds",
            database="bxdahcfis71ncmcthutg",
            password="VqDZ4xcAw4Bu7LialwMm",
            auth_plugin="mysql_native_password"
        )

        if conn.is_connected():
            return conn
    except Error as e:
        st.error(f"An error was encountered while connecting to the database: {e}")
        return None

def connect2db_NEW():
    try:
        engine = create_engine("mysql://uwywwwp2ws2f97ds:VqDZ4xcAw4Bu7LialwMm@bxdahcfis71ncmcthutg-mysql.services.clever-cloud.com:3306/bxdahcfis71ncmcthutg")

        return engine.connect()
    except SQLAlchemyError as e:
        st.error(f"An error was encountered while connecting to the database: {e}")
        return None