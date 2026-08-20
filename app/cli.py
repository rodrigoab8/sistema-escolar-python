from services import calcular_status

from aluno_repository import (
    inserir_aluno,
    buscar_todos_alunos,
    buscar_aluno_por_nome,
    buscar_aluno_por_matricula,
    excluir_aluno,
    atualizar_aluno,
    contar_alunos
)


# =========================================
# LIMPAR TELA
# =========================================

def limpar_tela():
    # Código ANSI utilizado para limpar o terminal.
    print("\033[H\033[J", end="")


# =========================================
# INTERFACE
# =========================================

def linha():
    # Cria uma linha visual para organizar a CLI.
    print("=" * 50)


def cabecalho(titulo):
    # Exibe um título centralizado entre duas linhas.
    linha()
    print(titulo.center(50))
    linha()


# =========================================
# CADASTRAR ALUNO
# =========================================

def cadastrar_aluno():

    limpar_tela()
    cabecalho("CADASTRAR ALUNO")

    nome = input("Nome do aluno: ").strip()

    # Impede cadastro com nome vazio.
    if not nome:
        print("\nErro: o nome do aluno não pode ficar vazio.")
        input("\nPressione ENTER para continuar...")
        return

    try:
        entrada_nota1 = input("Primeira nota: ").strip()
        entrada_nota2 = input("Segunda nota: ").strip()

        # Impede notas vazias.
        if not entrada_nota1 or not entrada_nota2:
            print("\nErro: as notas não podem ficar vazias.")
            input("\nPressione ENTER para continuar...")
            return

        # Converte os valores digitados para números decimais.
        nota1 = float(entrada_nota1)
        nota2 = float(entrada_nota2)

    except ValueError:
        # Executado caso o usuário digite algo que não seja número.
        print("\nErro: digite apenas números nas notas.")
        input("\nPressione ENTER para continuar...")
        return

    # Validação do intervalo permitido para as notas.
    if not (0 <= nota1 <= 10 and 0 <= nota2 <= 10):
        print("\nErro: as notas devem estar entre 0 e 10.")
        input("\nPressione ENTER para continuar...")
        return

    # A regra de negócio fica no services.py.
    status = calcular_status(nota1, nota2)

    # O repository grava o aluno no MySQL e devolve a matrícula.
    matricula = inserir_aluno(nome, nota1, nota2, status)

    print("\nAluno cadastrado com sucesso!")

    linha()
    print("Matrícula: {}".format(matricula))
    print("Aluno    : {}".format(nome))
    print("Nota 1   : {}".format(nota1))
    print("Nota 2   : {}".format(nota2))
    print("Status   : {}".format(status))
    linha()

    input("\nPressione ENTER para continuar...")

    limpar_tela()


# =========================================
# LISTAR ALUNOS
# =========================================

def listar_alunos():

    limpar_tela()
    cabecalho("LISTA DE ALUNOS")

    # Busca todos os registros existentes no banco.
    alunos = buscar_todos_alunos()

    if len(alunos) == 0:
        print("Nenhum aluno cadastrado.")

    else:
        for aluno in alunos:

            print("ID        : {}".format(aluno[0]))
            print("Matrícula : {}".format(aluno[1]))
            print("Nome      : {}".format(aluno[2]))
            print("Nota 1    : {}".format(aluno[3]))
            print("Nota 2    : {}".format(aluno[4]))
            print("Status    : {}".format(aluno[5]))
            linha()

    input("\nPressione ENTER para continuar...")

    limpar_tela()


# =========================================
# BUSCAR ALUNO POR NOME
# =========================================

def buscar_aluno():

    limpar_tela()
    cabecalho("BUSCAR ALUNO POR NOME")

    nome = input("Digite o nome do aluno: ").strip()

    if not nome:
        print("\nErro: o nome não pode ficar vazio.")
        input("\nPressione ENTER para continuar...")
        return

    # A consulta é realizada pelo aluno_repository.py.
    alunos = buscar_aluno_por_nome(nome)

    if len(alunos) == 0:
        print("\nNenhum aluno encontrado.")

    else:
        for aluno in alunos:

            print()
            print("ID        : {}".format(aluno[0]))
            print("Matrícula : {}".format(aluno[1]))
            print("Nome      : {}".format(aluno[2]))
            print("Nota 1    : {}".format(aluno[3]))
            print("Nota 2    : {}".format(aluno[4]))
            print("Status    : {}".format(aluno[5]))
            linha()

    input("\nPressione ENTER para continuar...")

    limpar_tela()


# =========================================
# BUSCAR ALUNO POR MATRÍCULA
# =========================================

def buscar_por_matricula():

    limpar_tela()
    cabecalho("BUSCAR ALUNO POR MATRÍCULA")

    matricula = input("Digite a matrícula do aluno: ").strip()

    if not matricula:
        print("\nErro: a matrícula não pode ficar vazia.")
        input("\nPressione ENTER para continuar...")
        return

    # Busca um único aluno utilizando a matrícula.
    aluno = buscar_aluno_por_matricula(matricula)

    if aluno is None:
        print("\nNenhum aluno encontrado.")

    else:
        print()
        print("ID        : {}".format(aluno[0]))
        print("Matrícula : {}".format(aluno[1]))
        print("Nome      : {}".format(aluno[2]))
        print("Nota 1    : {}".format(aluno[3]))
        print("Nota 2    : {}".format(aluno[4]))
        print("Status    : {}".format(aluno[5]))
        linha()

    input("\nPressione ENTER para continuar...")

    limpar_tela()


# =========================================
# EDITAR ALUNO
# =========================================

def editar_aluno():

    limpar_tela()
    cabecalho("EDITAR ALUNO")

    print("Para editar um aluno, será necessário informar a matrícula.")
    print("Caso não saiba a matrícula, utilize primeiro a busca por nome.")

    linha()

    matricula = input("Digite a matrícula do aluno: ").strip()

    if not matricula:
        print("\nErro: a matrícula não pode ficar vazia.")
        input("\nPressione ENTER para continuar...")
        return

    # Primeiro buscamos o aluno para verificar se ele existe.
    aluno = buscar_aluno_por_matricula(matricula)

    if aluno is None:
        print("\nNenhum aluno encontrado com essa matrícula.")
        input("\nPressione ENTER para continuar...")
        return

    print("\nAluno encontrado:")
    linha()
    print("Matrícula : {}".format(aluno[1]))
    print("Nome      : {}".format(aluno[2]))
    print("Nota 1    : {}".format(aluno[3]))
    print("Nota 2    : {}".format(aluno[4]))
    print("Status    : {}".format(aluno[5]))
    linha()

    print("\nDigite os novos dados.")
    print("Pressione ENTER para manter o valor atual.")

    novo_nome = input(
        "\nNome [{}]: ".format(aluno[2])
    ).strip()

    # Se nada for digitado, mantém o nome atual.
    if not novo_nome:
        novo_nome = aluno[2]

    entrada_nota1 = input(
        "Nota 1 [{}]: ".format(aluno[3])
    ).strip()

    entrada_nota2 = input(
        "Nota 2 [{}]: ".format(aluno[4])
    ).strip()

    try:

        # ENTER mantém a nota que já estava cadastrada.
        if entrada_nota1:
            nova_nota1 = float(entrada_nota1)
        else:
            nova_nota1 = float(aluno[3])

        if entrada_nota2:
            nova_nota2 = float(entrada_nota2)
        else:
            nova_nota2 = float(aluno[4])

    except ValueError:
        print("\nErro: digite apenas números nas notas.")
        input("\nPressione ENTER para continuar...")
        return

    if not (0 <= nova_nota1 <= 10 and 0 <= nova_nota2 <= 10):
        print("\nErro: as notas devem estar entre 0 e 10.")
        input("\nPressione ENTER para continuar...")
        return

    # Recalcula o status porque as notas podem ter mudado.
    novo_status = calcular_status(
        nova_nota1,
        nova_nota2
    )

    linha()
    print("\nNOVOS DADOS")
    linha()

    print("Matrícula : {}".format(matricula))
    print("Nome      : {}".format(novo_nome))
    print("Nota 1    : {}".format(nova_nota1))
    print("Nota 2    : {}".format(nova_nota2))
    print("Status    : {}".format(novo_status))

    linha()

    confirmacao = input(
        "\nConfirmar alteração? [S/N]: "
    ).strip().upper()

    if confirmacao == "S":

        # Envia os novos dados para o repository atualizar no MySQL.
        aluno_atualizado = atualizar_aluno(
            matricula,
            novo_nome,
            nova_nota1,
            nova_nota2,
            novo_status
        )

        if aluno_atualizado:
            print("\nAluno atualizado com sucesso.")
        else:
            print("\nNenhuma alteração foi realizada.")

    elif confirmacao == "N":
        print("\nAlteração cancelada.")

    else:
        print("\nOpção inválida. Alteração cancelada.")

    input("\nPressione ENTER para continuar...")

    limpar_tela()


# =========================================
# EXCLUIR ALUNO
# =========================================

def excluir_aluno_cli():

    limpar_tela()
    cabecalho("EXCLUIR ALUNO")

    print("Para excluir um aluno, será necessário informar a matrícula.")
    print("Caso não saiba a matrícula, utilize primeiro a busca por nome.")

    linha()

    matricula = input("Digite a matrícula do aluno: ").strip()

    if not matricula:
        print("\nErro: a matrícula não pode ficar vazia.")
        input("\nPressione ENTER para continuar...")
        return

    # Busca antes de excluir para confirmar qual aluno será removido.
    aluno = buscar_aluno_por_matricula(matricula)

    if aluno is None:
        print("\nNenhum aluno encontrado com essa matrícula.")
        input("\nPressione ENTER para continuar...")
        return

    print("\nAluno encontrado:")
    linha()
    print("Matrícula : {}".format(aluno[1]))
    print("Nome      : {}".format(aluno[2]))
    print("Nota 1    : {}".format(aluno[3]))
    print("Nota 2    : {}".format(aluno[4]))
    print("Status    : {}".format(aluno[5]))
    linha()

    # Proteção para evitar exclusões acidentais.
    confirmacao = input(
        "\nTem certeza que deseja excluir este aluno? [S/N]: "
    ).strip().upper()

    if confirmacao == "S":

        aluno_excluido = excluir_aluno(matricula)

        if aluno_excluido:
            print("\nAluno excluído com sucesso.")
        else:
            print("\nErro: não foi possível excluir o aluno.")

    elif confirmacao == "N":
        print("\nExclusão cancelada.")

    else:
        print("\nOpção inválida. Exclusão cancelada.")

    input("\nPressione ENTER para continuar...")

    limpar_tela()


# =========================================
# MENU PRINCIPAL
# =========================================

def menu_principal():

    # O while mantém o programa rodando até
    # o usuário selecionar a opção de sair.
    while True:

        limpar_tela()

        cabecalho("SISTEMA ESCOLAR v1.0")


        # =========================================
        # CONTADOR DE ALUNOS
        # =========================================

        # Consulta o MySQL através do repository.
        #
        # O repository executa:
        # SELECT COUNT(*) FROM alunos
        #
        # Por isso o número sempre representa a
        # quantidade REAL de alunos cadastrados.
        total_alunos = contar_alunos()

        print(
            "Alunos cadastrados: {}".format(total_alunos)
        )

        linha()


        # =========================================
        # OPÇÕES DISPONÍVEIS
        # =========================================

        print("[1] Cadastrar aluno")
        print("[2] Listar alunos")
        print("[3] Buscar aluno por Nome")
        print("[4] Buscar aluno por Matrícula")
        print("[5] Editar aluno")
        print("[6] Excluir aluno")
        print("[0] Sair")

        linha()

        opcao = input(
            "Escolha uma opção: "
        ).strip()


        # =========================================
        # CONTROLE DO MENU
        # =========================================

        if opcao == "1":
            cadastrar_aluno()

        elif opcao == "2":
            listar_alunos()

        elif opcao == "3":
            buscar_aluno()

        elif opcao == "4":
            buscar_por_matricula()

        elif opcao == "5":
            editar_aluno()

        elif opcao == "6":
            excluir_aluno_cli()

        elif opcao == "0":

            limpar_tela()

            print("Encerrando sistema...")

            # break encerra o while True e,
            # consequentemente, termina o menu.
            break

        else:

            print("\nOpção inválida.")

            input(
                "\nPressione ENTER para continuar..."
            )

            limpar_tela()


# =========================================
# INICIANDO SISTEMA
# =========================================

# Este é o ponto onde iniciamos a CLI.
# Ao executar este arquivo, o menu principal
# começa a funcionar.
menu_principal()