import streamlit as st
import mysql.connector

def get_connection():
    config = st.secrets["mysql"]

    return mysql.connector.connect(
        host=config["host"],
        user=config["user"],
        password=config["password"],
        database=config["database"],
        port=config.get("port", 24643),
    )
