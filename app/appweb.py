from flask import Flask, render_template, request, redirect

from aluno_repository import (
    buscar_todos_alunos,
    inserir_aluno,
    buscar_aluno_por_nome,
    buscar_aluno_por_matricula,
    atualizar_aluno,
    excluir_aluno,
    contar_alunos
)

from services import calcular_status


app = Flask(__name__)


# =========================================
# PÁGINA INICIAL
# =========================================

@app.route("/")
def inicio():

    alunos = buscar_todos_alunos()
    total_alunos = contar_alunos()

    return render_template(
        "index.html",
        alunos=alunos,
        total_alunos=total_alunos
    )


# =========================================
# CADASTRAR ALUNO
# =========================================

@app.route("/cadastrar", methods=["POST"])
def cadastrar():

    nome = request.form["nome"].strip()

    nota1 = float(request.form["nota1"])
    nota2 = float(request.form["nota2"])

    status = calcular_status(
        nota1,
        nota2
    )

    inserir_aluno(
        nome,
        nota1,
        nota2,
        status
    )

    return redirect("/")


# =========================================
# BUSCAR ALUNO POR NOME
# =========================================

@app.route("/buscar")
def buscar():

    nome = request.args.get("nome", "").strip()

    if nome:
        alunos = buscar_aluno_por_nome(nome)
    else:
        alunos = buscar_todos_alunos()

    total_alunos = contar_alunos()

    return render_template(
        "index.html",
        alunos=alunos,
        total_alunos=total_alunos
    )


# =========================================
# BUSCAR ALUNO POR MATRÍCULA
# =========================================

@app.route("/buscar-matricula")
def buscar_matricula():

    matricula = request.args.get("matricula", "").strip()

    if matricula:
        aluno = buscar_aluno_por_matricula(matricula)

        if aluno:
            alunos = [aluno]
        else:
            alunos = []

    else:
        alunos = buscar_todos_alunos()

    total_alunos = contar_alunos()

    return render_template(
        "index.html",
        alunos=alunos,
        total_alunos=total_alunos
    )


# =========================================
# EDITAR ALUNO
# =========================================

@app.route("/editar/<matricula>", methods=["GET", "POST"])
def editar(matricula):

    aluno = buscar_aluno_por_matricula(matricula)

    if aluno is None:
        return redirect("/")

    if request.method == "POST":

        nome = request.form["nome"].strip()

        nota1 = float(request.form["nota1"])
        nota2 = float(request.form["nota2"])

        status = calcular_status(
            nota1,
            nota2
        )

        atualizar_aluno(
            matricula,
            nome,
            nota1,
            nota2,
            status
        )

        return redirect("/")

    return render_template(
        "editar.html",
        aluno=aluno
    )


# =========================================
# EXCLUIR ALUNO
# =========================================

@app.route("/excluir/<matricula>", methods=["POST"])
def excluir(matricula):

    excluir_aluno(matricula)

    return redirect("/")


# =========================================
# INICIAR APLICAÇÃO
# =========================================

if __name__ == "__main__":
    app.run(debug=True)