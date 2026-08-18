from database import conectar


def inserir_aluno(nome, nota1, nota2, status):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    INSERT INTO alunos
    (nome, nota1, nota2, status_aluno)
    VALUES (%s, %s, %s, %s)
    """

    valores = (nome, nota1, nota2, status)

    cursor.execute(sql, valores)

    # Pega o ID criado automaticamente pelo MySQL
    id_aluno = cursor.lastrowid

    # Gera a matrícula a partir do ID
    matricula = f"ALU{id_aluno:06d}"

    # Atualiza o aluno com a matrícula gerada
    sql_matricula = """
    UPDATE alunos
    SET matricula = %s
    WHERE id = %s
    """

    cursor.execute(sql_matricula, (matricula, id_aluno))

    conexao.commit()

    cursor.close()
    conexao.close()

    return matricula


def buscar_todos_alunos():
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT id, matricula, nome, nota1, nota2, status_aluno
    FROM alunos
    """

    cursor.execute(sql)

    alunos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return alunos

def buscar_aluno_por_nome(nome):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT id, matricula, nome, nota1, nota2, status_aluno
    FROM alunos
    WHERE LOWER(nome) LIKE LOWER(%s)
    """

    termo_busca = f"%{nome}%"

    cursor.execute(sql, (termo_busca,))

    alunos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return alunos

def buscar_aluno_por_matricula(matricula):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT id, matricula, nome, nota1, nota2, status_aluno
    FROM alunos
    WHERE matricula = %s
    """

    cursor.execute(sql, (matricula,))

    aluno = cursor.fetchone()

    cursor.close()
    conexao.close()

    return aluno