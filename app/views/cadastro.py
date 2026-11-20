
import streamlit as st
from datetime import date

from app.services import filmes_service


def render():
    aba_cadastro, aba_listagem = st.tabs(
        ["Cadastrar filme", "Listar e excluir filmes"]
    )

    with aba_cadastro:
        cadastrar_filme()

    with aba_listagem:
        listar_filmes()


def cadastrar_filme():
    st.subheader("Cadastrar filme")

    generos_disponiveis = filmes_service.listar_generos()

    if not generos_disponiveis:
        st.warning("Nenhum gênero disponível.")
        return

    with st.form("form_cadastro_filme"):
        titulo = st.text_input("Título do filme")
        sinopse = st.text_area("Sinopse")

        data_lancamento = st.date_input(
            "Data de lançamento",
            value=date.today()
        )

        duracao = st.number_input(
            "Duração (minutos)",
            min_value=1,
            step=1
        )

        classificacao = st.selectbox(
            "Classificação indicativa",
            options=[0, 10, 12, 14, 16, 18]
        )

        generos_selecionados = st.multiselect(
            "Gêneros",
            options=generos_disponiveis,
            format_func=lambda genero: genero["nome"]
        )

        enviar = st.form_submit_button(
            "Cadastrar filme",
            use_container_width=True
        )

        if enviar:
            if not titulo.strip():
                st.error("Informe o título do filme.")

            elif not sinopse.strip():
                st.error("Informe a sinopse do filme.")

            elif not generos_selecionados:
                st.error("Selecione pelo menos um gênero.")

            else:
                sucesso, mensagem = filmes_service.cadastrar_filme(
                    titulo.strip(),
                    sinopse.strip(),
                    data_lancamento,
                    duracao,
                    classificacao,
                    [
                        genero["id_genero"]
                        for genero in generos_selecionados
                    ]
                )

                if sucesso:
                    st.success(mensagem)
                else:
                    st.error(mensagem)


def listar_filmes():
    st.subheader("Filmes cadastrados")

    filmes = filmes_service.listar_filmes_com_generos()

    if not filmes:
        st.info("Nenhum filme cadastrado.")
        return

    for filme in filmes:
        with st.container(border=True):
            st.markdown(f"**{filme['titulo']}**")

            st.write(f"ID: {filme['id_filme']}")
            st.write(f"Gêneros: {filme['generos'] or 'Não informado'}")
            st.write(
                f"Lançamento: {filme['data_lancamento']}"
            )
            st.write(
                f"Duração: {filme['duracao_minutos']} minutos"
            )
            st.write(
                f"Classificação: {filme['class_indicativa']} anos"
            )
            st.write(f"Sinopse: {filme['sinopse']}")

            if st.button(
                "Excluir filme",
                key=f"excluir_{filme['id_filme']}"
            ):
                sucesso, mensagem = filmes_service.excluir_filme(
                    filme["id_filme"]
                )

                if sucesso:
                    st.success(mensagem)
                    st.rerun()
                else:
                    st.error(mensagem)
