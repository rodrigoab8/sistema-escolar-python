import mysql.connector


# =========================================
# CONEXÃO COM BANCO
# =========================================

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="roo123",
        database="sistema_escolar"
    )


# =========================================
# LIMPAR TELA
# =========================================

def limpar_tela():
    print("\033[H\033[J", end="")


# =========================================
# INTERFACE
# =========================================

def linha():
    print("=" * 50)


def cabecalho(titulo):
    linha()
    print(titulo.center(50))
    linha()


# =========================================
# REGRA DE NEGÓCIO
# =========================================

def calcular_status(nota1, nota2):

    media = (nota1 + nota2) / 2

    if media >= 7:
        return "Aprovado"

    elif media >= 5:
        return "Recuperação"

    else:
        return "Reprovado"


# =========================================
# CADASTRAR ALUNO
# =========================================

def cadastrar_aluno():

    limpar_tela()

    cabecalho("CADASTRAR ALUNO")

    nome = input("Nome do aluno: ")

    nota1 = float(input("Primeira nota: "))
    nota2 = float(input("Segunda nota: "))

    status = calcular_status(nota1, nota2)

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    INSERT INTO alunos
    (nome, nota1, nota2, status_aluno)
    VALUES (%s, %s, %s, %s)
    """

    valores = (nome, nota1, nota2, status)

    cursor.execute(sql, valores)

    conexao.commit()

    print("\nAluno cadastrado com sucesso!")

    linha()
    print(f"Aluno : {nome}")
    print(f"Nota 1: {nota1}")
    print(f"Nota 2: {nota2}")
    print(f"Status: {status}")
    linha()

    cursor.close()
    conexao.close()

    input("\nPressione ENTER para continuar...")

    limpar_tela()


# =========================================
# LISTAR ALUNOS
# =========================================

def listar_alunos():

    limpar_tela()

    cabecalho("LISTA DE ALUNOS")

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT id, nome, nota1, nota2, status_aluno
    FROM alunos
    """)

    alunos = cursor.fetchall()

    if len(alunos) == 0:

        print("Nenhum aluno cadastrado.")

    else:

        for aluno in alunos:

            print(f"ID      : {aluno[0]}")
            print(f"Nome    : {aluno[1]}")
            print(f"Nota 1  : {aluno[2]}")
            print(f"Nota 2  : {aluno[3]}")
            print(f"Status  : {aluno[4]}")

            linha()

    cursor.close()
    conexao.close()

    input("\nPressione ENTER para continuar...")

    limpar_tela()


# =========================================
# MENU PRINCIPAL
# =========================================

def menu_principal():

    while True:

        limpar_tela()

        cabecalho("SISTEMA ESCOLAR v1.0")

        print("[1] Cadastrar aluno")
        print("[2] Listar alunos")
        print("[3] Sair")

        linha()

        opcao = input("Escolha uma opção: ")

        if opcao == "1":

            cadastrar_aluno()

        elif opcao == "2":

            listar_alunos()

        elif opcao == "3":

            limpar_tela()

            print("Encerrando sistema...")

            break

        else:

            print("\nOpção inválida.")

            input("\nPressione ENTER para continuar...")

            limpar_tela()


# =========================================
# INICIANDO SISTEMA
# =========================================

menu_principal()