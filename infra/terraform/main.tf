
# ============================================================
# PROJETO: SISTEMA ESCOLAR
# ARQUIVO: main.tf
# CAMADA: REDE - AMAZON VPC
# ============================================================

# OBJETIVO:
# Criar a rede virtual privada do Sistema Escolar.
#
# POR QUE UTILIZAMOS?
# A VPC permite organizar os recursos AWS dentro
# de uma rede logicamente isolada.
#
# DECISAO DE ARQUITETURA:
# Utilizamos o CIDR 10.0.0.0/16 para manter
# o enderecamento da nossa infraestrutura original.
#
# IMPORTANTE:
# Criar uma VPC nao fornece acesso automatico
# a internet. Isso sera configurado posteriormente.

resource "aws_vpc" "sistema_escolar" {

  # Utiliza o bloco CIDR definido no arquivo variables.tf.
  cidr_block = var.vpc_cidr

  # Habilita a resolucao de nomes DNS.
  enable_dns_support = true

  # Permite a atribuicao de nomes DNS compativeis.
  enable_dns_hostnames = true

  # Identifica o recurso no console AWS.
  tags = {
    Name    = "sistema-escolar-vpc"
    Project = "Sistema-Escolar"
    Managed = "Terraform"
  }
}

