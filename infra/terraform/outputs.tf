
# ============================================================
# PROJETO: SISTEMA ESCOLAR
# ARQUIVO: outputs.tf
# OBJETIVO: EXIBIR INFORMACOES DA INFRAESTRUTURA
# ============================================================

# O QUE E UM OUTPUT?
# E uma informacao de saida disponibilizada pelo Terraform.
#
# POR QUE UTILIZAMOS?
# Para consultar dados importantes dos recursos
# gerenciados, como identificadores e enderecos de rede.

# ------------------------------------------------------------
# OUTPUT: vpc_id
# ------------------------------------------------------------

# Exibe o identificador da VPC atribuido pela AWS.
#
# aws_vpc: tipo do recurso.
# sistema_escolar: nome local definido no main.tf.
# id: identificador atribuido pela AWS.

output "vpc_id" {
  description = "Identificador da VPC do Sistema Escolar"
  value       = aws_vpc.sistema_escolar.id
}

# ------------------------------------------------------------
# OUTPUT: vpc_cidr
# ------------------------------------------------------------

# Exibe o bloco de enderecos IPv4 configurado na VPC.

output "vpc_cidr" {
  description = "Bloco CIDR da VPC do Sistema Escolar"
  value       = aws_vpc.sistema_escolar.cidr_block
}
