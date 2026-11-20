
import streamlit as st
from app.services import relatorios_service


def render():
    st.title("Relatórios")

    aba_historico, aba_generos, aba_assinaturas = st.tabs([
        "Histórico de visualizações",
        "Filmes por gênero",
        "Assinaturas"
    ])

    with aba_historico:
        exibir_historico()

    with aba_generos:
        exibir_filmes_generos()

    with aba_assinaturas:
        exibir_assinaturas()


def exibir_historico():
    st.subheader("Histórico de visualizações")

    dados = relatorios_service.relatorio_historico()

    if not dados:
        st.info("Nenhum registro de visualização encontrado.")
        return

    st.dataframe(
        dados,
        use_container_width=True,
        hide_index=True
    )


def exibir_filmes_generos():
    st.subheader("Filmes e seus gêneros")

    dados = relatorios_service.relatorio_filmes_generos()

    if not dados:
        st.info("Nenhum filme com gênero encontrado.")
        return

    st.dataframe(
        dados,
        use_container_width=True,
        hide_index=True
    )


def exibir_assinaturas():
    st.subheader("Valores mensais por plano")

    dados = relatorios_service.relatorio_assinaturas()

    if not dados:
        st.info("Nenhuma assinatura ativa encontrada.")
        return

    st.dataframe(
        dados,
        use_container_width=True,
        hide_index=True
    )
