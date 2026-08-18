
# REGRA DE NEGÓCIO

def calcular_status(nota1, nota2):
    media = (nota1 + nota2) / 2

    if media >= 7:
        return "Aprovado"
    elif media >= 5:
        return "Recuperação"
    else:
        return "Reprovado"