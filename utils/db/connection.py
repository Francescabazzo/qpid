import streamlit as st
from sqlalchemy.exc import SQLAlchemyError as exc
from sqlalchemy import create_engine
from utils.logger import log


def connect2db():
    try:
        engine = create_engine(st.secrets['database']['connection_url'])

        log("CONNECTION TO DB", 0)

        return engine.connect()
    except exc as e:
        st.error(f"An error was encountered while connecting to the database: {e}")

        log(f"CONNECTION TO DB ERROR: {e}", 2)

        return None
