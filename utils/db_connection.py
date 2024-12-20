from mysql.connector import connect, Error
import streamlit as st

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
        #conn = connect(host="sql7.freesqldatabase.com",user="sql7749843",database="sql7749843",password="fn9x4LYm1e")
        #conn = connect(host="sql.am-online.it",user="amonline13158",database="amonline13158",password="$Host2022!")

        if conn.is_connected():
            return conn
    except Error as e:
        st.error(f"An error was encountered while connecting to the database: {e}")
        return None