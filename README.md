🎓 Sistema Escolar — Cloud & DevOps Portfolio

Sistema de gestão escolar desenvolvido inicialmente em Python e MySQL, criado para aplicar conceitos de programação, banco de dados e regras de negócio em um projeto prático.

O projeto está sendo evoluído progressivamente para uma aplicação web implantada na AWS, incorporando conceitos de Cloud Computing, DevOps, segurança, automação, observabilidade, Infrastructure as Code (IaC), CI/CD e Inteligência Artificial.

Mais do que uma aplicação acadêmica, este repositório funciona como um projeto de portfólio em evolução, documentando não apenas a implementação, mas também as decisões de arquitetura, os problemas encontrados e as soluções adotadas durante o desenvolvimento.

🎯 Objetivos do Projeto
Desenvolver e evoluir uma aplicação completa utilizando Python e MySQL.
Aplicar conceitos de desenvolvimento backend e banco de dados.
Transformar o sistema atual em uma aplicação web.
Projetar uma arquitetura segura e escalável na AWS.
Aplicar conceitos de redes, segurança e gerenciamento de acessos.
Implementar práticas de DevOps e automação.
Utilizar Infrastructure as Code para provisionamento da infraestrutura.
Criar pipelines de CI/CD.
Implementar monitoramento e observabilidade.
Explorar a integração de agentes de Inteligência Artificial.
Documentar decisões técnicas e arquiteturais para consolidar o aprendizado.
🛠️ Tecnologias
Atualmente utilizadas
Python
MySQL
SQL
Git
GitHub
PyCharm
Planejadas durante a evolução
Flask
HTML / CSS
Docker
AWS
Linux
Nginx
GitHub Actions
Terraform
Amazon CloudWatch
Amazon RDS
Inteligência Artificial / Agentes de IA
📂 Estrutura do Projeto
sistema-escolar/
│
├── app/          # Código-fonte da aplicação
├── docs/         # Documentação técnica e decisões de arquitetura
├── infra/        # Infraestrutura, Docker e futuramente Terraform
├── scripts/      # Scripts de automação e administração
├── tests/        # Testes automatizados
│
├── .gitignore
└── README.md

A estrutura será refinada conforme novas tecnologias e componentes forem incorporados ao projeto.

🗺️ Roadmap
Fase 1 — Fundamentos da aplicação

Desenvolvimento inicial em Python

Integração com MySQL

Operações CRUD

Implementação de regras de negócio

Revisão e refatoração do código existente

Organização da estrutura do projeto

Documentação técnica

Fase 2 — Aplicação Web

Implementação com Flask

Criação das rotas da aplicação

Desenvolvimento das páginas HTML

Organização de templates e arquivos estáticos

Integração da aplicação web com MySQL

Tratamento de erros e validações

Fase 3 — Containerização

Criação do Dockerfile

Containerização da aplicação

Configuração das dependências

Execução da aplicação em containers

Fase 4 — Arquitetura AWS

Criação de uma VPC própria

Configuração de sub-redes públicas e privadas

Internet Gateway

Route Tables

Security Groups

IAM Roles e políticas de acesso

Deploy da aplicação em Amazon EC2

Configuração do Nginx

Migração do banco de dados para Amazon RDS

Monitoramento com Amazon CloudWatch

Fase 5 — DevOps e Automação

Pipeline de CI/CD

GitHub Actions

Automação de testes

Automação de build e deploy

Versionamento e estratégia de branches

Fase 6 — Infrastructure as Code

Introdução ao Terraform

Provisionamento da infraestrutura AWS com código

Versionamento da infraestrutura

Separação de ambientes

Documentação da arquitetura

Fase 7 — Inteligência Artificial

Estudo da arquitetura de agentes de IA

Integração segura entre IA e aplicação

Agente para consultas sobre dados escolares

Geração automatizada de relatórios

Uso de ferramentas e APIs pelos agentes

Observabilidade e segurança das integrações de IA

🏗️ Arquitetura

A arquitetura será desenvolvida de forma incremental.

O objetivo é partir de uma aplicação local simples e evoluí-la para uma solução distribuída em nuvem, utilizando serviços AWS e princípios de segurança, disponibilidade, escalabilidade e automação.

Os diagramas e registros das decisões arquiteturais serão armazenados em:

docs/
📚 Documentação e Aprendizado

Além do código-fonte, este repositório documentará conceitos utilizados durante o desenvolvimento, incluindo:

Git e controle de versão
SQL e MySQL
Linux
PowerShell
Redes e protocolos
AWS
Docker
CI/CD
Terraform
Segurança
Observabilidade
Arquitetura Cloud
Inteligência Artificial

A proposta é registrar não apenas como implementar, mas principalmente por que determinada solução foi escolhida.

🚀 Visão de Longo Prazo

A meta deste projeto é demonstrar a evolução de uma aplicação desde sua implementação inicial até uma arquitetura moderna em nuvem.

A evolução seguirá, de forma geral, o fluxo:

Python + MySQL → Flask → Docker → AWS → CI/CD → Terraform → Observabilidade → Agentes de IA

Cada etapa será implementada e documentada progressivamente, permitindo acompanhar a evolução técnica e arquitetural do sistema.

📌 Status

🚧 Em desenvolvimento

O projeto está atualmente passando por uma fase de reorganização e evolução arquitetural.

Novas funcionalidades, documentação e componentes de infraestrutura serão adicionados conforme o avanço dos estudos e da implementação.