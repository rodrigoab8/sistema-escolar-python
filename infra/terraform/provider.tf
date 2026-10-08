# ============================================================
# PROJETO: SISTEMA ESCOLAR
# ARQUIVO: provider.tf
# OBJETIVO: CONFIGURAR O TERRAFORM PARA UTILIZAR A AWS
# ============================================================

# Define os provedores necessários para o projeto.
# O Terraform utiliza provedores para interagir com
# serviços externos, como AWS, Azure e Google Cloud.

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

# Configura o provedor AWS.
#
# A região us-east-1 foi escolhida porque utilizamos
# essa região na infraestrutura original do Sistema Escolar.
#
# As credenciais serão obtidas pelo mecanismo de
# autenticação da AWS, sem armazenar senhas no código.

provider "aws" {
  region = "us-east-1"
}