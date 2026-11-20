
from app.database.conexao import conectar


def relatorio_historico():
    conexao = conectar()

    if conexao is None:
        return []

    cursor = None

    try:
        cursor = conexao.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                usuario.nome,
                filme.titulo,
                historico.data_visualizacao,
                historico.progresso_min
            FROM historico
            INNER JOIN usuario
                ON historico.id_usuario = usuario.id_usuario
            INNER JOIN filme
                ON historico.id_filme = filme.id_filme
        """)

        return cursor.fetchall()

    except Exception as erro:
        print(f"Erro no relatório de histórico: {erro}")
        return []

    finally:
        if cursor is not None:
            cursor.close()
        conexao.close()


def relatorio_filmes_generos():
    conexao = conectar()

    if conexao is None:
        return []

    cursor = None

    try:
        cursor = conexao.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                filme.titulo,
                genero.nome AS genero,
                filme_genero.ordem_exibicao
            FROM filme
            INNER JOIN filme_genero
                ON filme.id_filme = filme_genero.id_filme
            INNER JOIN genero
                ON filme_genero.id_genero = genero.id_genero
        """)

        return cursor.fetchall()

    except Exception as erro:
        print(f"Erro no relatório de filmes e gêneros: {erro}")
        return []

    finally:
        if cursor is not None:
            cursor.close()
        conexao.close()


def relatorio_assinaturas():
    conexao = conectar()

    if conexao is None:
        return []

    cursor = None

    try:
        cursor = conexao.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                plano,
                SUM(valor_mensal) AS total_mensal
            FROM assinatura
            WHERE status_assinatura = 'Ativa'
            GROUP BY plano
        """)

        return cursor.fetchall()

    except Exception as erro:
        print(f"Erro no relatório de assinaturas: {erro}")
        return []

    finally:
        if cursor is not None:
            cursor.close()
        conexao.close()
