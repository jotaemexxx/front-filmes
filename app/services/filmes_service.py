
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
            

def cadastrar_filme(titulo, sinopse, data_lancamento,
                    duracao_minutos, class_indicativa, generos):
    conexao = conectar()

    if conexao is None:
        return False, "Não foi possível conectar ao banco."

    cursor = None

    try:
        cursor = conexao.cursor()

        # Insere o filme
        cursor.execute("""
            INSERT INTO filme (
                titulo,
                sinopse,
                data_lancamento,
                duracao_minutos,
                class_indicativa
            )
            VALUES (%s, %s, %s, %s, %s)
        """, (
            titulo,
            sinopse,
            data_lancamento,
            duracao_minutos,
            class_indicativa
        ))

        id_filme = cursor.lastrowid

        # Insere os gêneros associados ao filme
        for ordem, id_genero in enumerate(generos, start=1):
            cursor.execute("""
                INSERT INTO filme_genero (
                    id_filme,
                    id_genero,
                    ordem_exibicao
                )
                VALUES (%s, %s, %s)
            """, (id_filme, id_genero, ordem))

        conexao.commit()

        return True, "Filme cadastrado com sucesso!"

    except Exception as erro:
        conexao.rollback()
        return False, f"Erro ao cadastrar filme: {erro}"

    finally:
        if cursor is not None:
            cursor.close()

        conexao.close()


def listar_filmes_com_generos():
    conexao = conectar()

    if conexao is None:
        return []

    cursor = None

    try:
        cursor = conexao.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                f.id_filme,
                f.titulo,
                f.sinopse,
                f.data_lancamento,
                f.duracao_minutos,
                f.class_indicativa,
                GROUP_CONCAT(
                    g.nome
                    ORDER BY fg.ordem_exibicao
                    SEPARATOR ', '
                ) AS generos
            FROM filme f
            LEFT JOIN filme_genero fg
                ON f.id_filme = fg.id_filme
            LEFT JOIN genero g
                ON fg.id_genero = g.id_genero
            GROUP BY
                f.id_filme,
                f.titulo,
                f.sinopse,
                f.data_lancamento,
                f.duracao_minutos,
                f.class_indicativa
            ORDER BY f.titulo;
        """)

        return cursor.fetchall()

    except Exception as erro:
        print(f"Erro ao listar filmes: {erro}")
        return []

    finally:
        if cursor is not None:
            cursor.close()

        conexao.close()


def excluir_filme(id_filme):
    conexao = conectar()

    if conexao is None:
        return False, "Não foi possível conectar ao banco."

    cursor = None

    try:
        cursor = conexao.cursor()

        # Verifica se o filme possui registros no histórico
        cursor.execute("""
            SELECT COUNT(*)
            FROM historico
            WHERE id_filme = %s
        """, (id_filme,))

        quantidade = cursor.fetchone()[0]

        if quantidade > 0:
            return False, (
                "Não é possível excluir este filme, "
                "pois existem registros dele no histórico."
            )

        # Exclui os relacionamentos com os gêneros
        cursor.execute("""
            DELETE FROM filme_genero
            WHERE id_filme = %s
        """, (id_filme,))

        # Exclui o filme
        cursor.execute("""
            DELETE FROM filme
            WHERE id_filme = %s
        """, (id_filme,))

        if cursor.rowcount == 0:
            conexao.rollback()
            return False, "Filme não encontrado."

        conexao.commit()

        return True, "Filme excluído com sucesso!"

    except Exception as erro:
        conexao.rollback()
        return False, f"Erro ao excluir filme: {erro}"

    finally:
        if cursor is not None:
            cursor.close()

        conexao.close()

