
import streamlit as st
from app.views import cadastro, relatorios

st.set_page_config(
    page_title="Streaming",
    page_icon="🎬",
    layout="wide"
)

st.title("Streaming")

aba_inicio, aba_cadastros, aba_relatorios = st.tabs([
    "Início",
    "Cadastros",
    "Relatórios"
])

with aba_inicio:
    st.write("Sistema de gerenciamento de filmes.")
    st.info("Bem-vindo ao Streaming!")

with aba_cadastros:
    cadastro.render()

with aba_relatorios:
    relatorios.render()
