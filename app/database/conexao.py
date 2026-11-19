
import streamlit as st
import mysql.connector
from mysql.connector import Error


def conectar():
    try:
        conexao = mysql.connector.connect(
    host=st.secrets["mysql"]["host"],
    port=st.secrets["mysql"]["port"],
    user=st.secrets["mysql"]["user"],
    password=st.secrets["mysql"]["password"],
    database=st.secrets["mysql"]["database"],
    charset="utf8mb4"
)

        return conexao

    except Error as erro:
        print(f"Erro ao conectar ao MySQL: {erro}")
        return None
