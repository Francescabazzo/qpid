import streamlit as st
from sqlalchemy.exc import SQLAlchemyError as exc
from sqlalchemy import create_engine


def connect2db():
    try:
        engine = create_engine(st.secrets['database']['connection_url'])

        return engine.connect()
    except exc as e:
        st.error(f"An error was encountered while connecting to the database: {e}")
        return None
