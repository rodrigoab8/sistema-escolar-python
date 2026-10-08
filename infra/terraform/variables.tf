
# ============================================================
# PROJETO: SISTEMA ESCOLAR
# ARQUIVO: variables.tf
# OBJETIVO: DEFINIR PARAMETROS REUTILIZAVEIS
# ============================================================

# O QUE E UMA VARIAVEL?
# Uma variavel permite configurar valores utilizados
# pelos recursos sem alterar diretamente sua estrutura.
#
# POR QUE UTILIZAMOS?
# Para facilitar a reutilizacao da infraestrutura
# em diferentes ambientes, como desenvolvimento e testes.

# ------------------------------------------------------------
# VARIAVEL: vpc_cidr
# ------------------------------------------------------------

# Define o intervalo de enderecos IPv4 da nossa VPC.
#
# type = string:
# O valor deve ser uma sequencia de caracteres.
#
# default:
# Valor utilizado quando nenhum outro for informado.

variable "vpc_cidr" {
  description = "Bloco CIDR IPv4 da VPC do Sistema Escolar"
  type        = string
  default     = "10.0.0.0/16"
}

