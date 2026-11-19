
from app.database.conexao import conectar


def listar_filmes():
    conexao = conectar()

    if conexao is None:
        return []

    try:
        cursor = conexao.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id_filme,
                titulo,
                sinopse,
                data_lancamento,
                duracao_minutos,
                class_indicativa
            FROM filme
            ORDER BY titulo
        """)

        filmes = cursor.fetchall()
        return filmes

    except Exception as erro:
        print(f"Erro ao listar filmes: {erro}")
        return []

    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()


def listar_generos():
    conexao = conectar()

    if conexao is None:
        return []

    try:
        cursor = conexao.cursor(dictionary=True)

        cursor.execute("""
            SELECT id_genero, nome
            FROM genero
            ORDER BY nome
        """)

        return cursor.fetchall()

    except Exception as erro:
        print(f"Erro ao listar gêneros: {erro}")
        return []

    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()
