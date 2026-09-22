# Sistema Escolar — Arquitetura

## 1. Objetivo deste documento

Este documento apresenta a arquitetura atual do projeto **Sistema Escolar**,
descrevendo os principais componentes da aplicação, suas responsabilidades
e a forma como eles se comunicam.

A arquitetura é documentada de forma incremental.

O projeto iniciou como uma aplicação Python executada localmente, evoluiu
para uma aplicação web utilizando Flask e posteriormente foi implantado
em infraestrutura AWS.

Atualmente, a aplicação está hospedada em uma instância Amazon EC2 e utiliza
Amazon RDS for MySQL como banco de dados.

O objetivo deste documento é registrar:

- arquitetura atual;
- separação das camadas;
- fluxo das requisições;
- componentes utilizados;
- decisões arquiteturais;
- evolução do projeto;
- próximos passos.

Os detalhes específicos da infraestrutura AWS estão documentados em:

```text
docs/aws/
```

---

# 2. Evolução da arquitetura

O projeto passou por diferentes estágios.

```text
Aplicação CLI Local
        |
        v
Aplicação Web Local
        |
        v
Deploy em EC2
        |
        v
Nginx + Gunicorn + Flask
        |
        v
MariaDB local na EC2
        |
        v
Amazon RDS MySQL
```

Cada etapa foi implementada somente após a validação da etapa anterior.

Essa abordagem permitiu compreender individualmente os componentes antes
de aumentar a complexidade da arquitetura.

---

# 3. Arquitetura atual

Atualmente, o Sistema Escolar está implantado na AWS.

A arquitetura possui duas camadas principais:

1. camada de aplicação;
2. camada de banco de dados.

A camada de aplicação está hospedada em uma instância Amazon EC2.

A camada de dados utiliza Amazon RDS for MySQL.

Uma visão simplificada é:

```text
Usuário
   |
   | HTTP / HTTPS
   v
Internet
   |
   v
Internet Gateway
   |
   v
Amazon EC2
   |
   |-- Nginx
   |-- Gunicorn
   `-- Flask
          |
          | TCP 3306
          v
      Amazon RDS
          |
          `-- MySQL
              |
              `-- sistema_escolar
```

Aplicação e banco não estão mais hospedados no mesmo servidor.

---

# 4. Arquitetura de rede AWS

A infraestrutura utiliza uma VPC própria:

```text
sistema-escolar-vpc
10.0.0.0/16
```

Dentro dessa VPC existem uma subnet pública e duas subnets privadas.

```text
VPC — 10.0.0.0/16
|
|-- Subnet pública — 10.0.1.0/24
|       |
|       `-- EC2
|
|-- Subnet privada — 10.0.2.0/24
|
`-- Subnet privada — 10.0.3.0/24
```

A EC2 está posicionada na subnet pública porque precisa receber as
requisições da aplicação web.

O RDS utiliza a camada de subnets privadas porque não precisa receber
conexões diretamente da internet.

A documentação detalhada da rede está disponível em:

```text
docs/aws/01-rede.md
docs/aws/06-rds-mysql.md
```

---

# 5. Camada de apresentação

A interação com o Sistema Escolar ocorre através do navegador.

A interface utiliza:

- HTML;
- CSS;
- templates Flask.

A aplicação possui diretórios como:

```text
templates/
static/
```

O diretório `templates` contém as páginas HTML utilizadas pelo Flask.

O diretório `static` contém arquivos estáticos utilizados pela interface.

Essa separação evita misturar a apresentação visual diretamente com a
lógica Python.

---

# 6. Nginx

O **Nginx** é utilizado como servidor web e proxy reverso.

Ele recebe as requisições HTTP destinadas à aplicação.

O fluxo é:

```text
Navegador
    |
    | HTTP
    v
Nginx
    |
    v
Gunicorn
```

O Gunicorn não precisa ficar diretamente exposto à internet.

O Nginx recebe a requisição e encaminha internamente para o servidor
de aplicação.

---

# 7. Gunicorn

O **Gunicorn** é utilizado como servidor WSGI para executar a aplicação Flask.

Atualmente ele escuta localmente em:

```text
127.0.0.1:8000
```

Isso significa que o Gunicorn não está diretamente exposto externamente.

O fluxo é:

```text
Internet
   |
   v
Nginx
   |
   | 127.0.0.1:8000
   v
Gunicorn
   |
   v
Flask
```

O serviço é gerenciado pelo `systemd` através de:

```text
sistema-escolar.service
```

Isso permite iniciar, parar, reiniciar e consultar o estado da aplicação
como um serviço Linux.

---

# 8. Backend

O backend é desenvolvido em **Python** utilizando **Flask**.

Entre suas responsabilidades estão:

- receber requisições;
- validar informações;
- executar regras de negócio;
- realizar operações CRUD;
- comunicar-se com o banco de dados;
- renderizar templates;
- devolver respostas ao navegador.

O Flask funciona como ponto de integração entre:

```text
Interface
    |
    v
Rotas Flask
    |
    v
Regras da aplicação
    |
    v
Acesso aos dados
    |
    v
Amazon RDS MySQL
```

---

# 9. Regras de negócio

O Sistema Escolar possui regras relacionadas ao desempenho acadêmico dos
alunos.

A média é calculada utilizando:

```text
media = (nota1 + nota2) / 2
```

A situação acadêmica segue:

```text
Média >= 7       -> Aprovado
Média >= 5 e < 7 -> Recuperação
Média < 5        -> Reprovado
```

Também existem validações para impedir valores inválidos, como notas fora
do intervalo permitido.

O banco possui ainda a trigger:

```text
trg_atualizar_media_status
```

Ela participa da atualização da média e do status dos alunos durante
operações de atualização.

---

# 10. Camada de acesso aos dados

A aplicação executa operações CRUD sobre os dados dos alunos.

```text
CREATE -> cadastrar
READ   -> consultar/listar
UPDATE -> editar
DELETE -> excluir
```

A aplicação utiliza o **MySQL Connector/Python** para estabelecer a
comunicação com o banco.

A configuração da conexão não fica diretamente gravada no código.

Ela é fornecida através de variáveis de ambiente.

---

# 11. Variáveis de ambiente

Na EC2, as informações necessárias para conexão com o banco são fornecidas
através do arquivo:

```text
/etc/sistema-escolar.env
```

A aplicação utiliza:

```text
DB_HOST
DB_USER
DB_PASSWORD
DB_NAME
```

O `DB_HOST` aponta para o endpoint do Amazon RDS.

As credenciais não devem ser armazenadas diretamente no código-fonte nem
enviadas para o GitHub.

Isso separa:

```text
Código da aplicação
        |
        X
Credenciais
```

das configurações específicas do ambiente onde a aplicação está sendo
executada.

---

# 12. Banco de dados

O banco de dados atual utiliza:

```text
Amazon RDS for MySQL
```

O banco da aplicação é:

```text
sistema_escolar
```

A principal tabela é:

```text
alunos
```

O banco anteriormente executava como MariaDB dentro da própria EC2.

Após a evolução da infraestrutura, os dados foram migrados para o RDS.

O MariaDB local foi desacoplado da aplicação e o Sistema Escolar foi
validado utilizando exclusivamente o banco remoto.

A documentação detalhada da migração está disponível em:

```text
docs/aws/06-rds-mysql.md
```

---

# 13. Isolamento do banco de dados

O RDS não possui acesso público.

A aplicação acessa o banco através da rede interna da VPC.

O Security Group do RDS permite:

```text
TCP 3306
```

tendo como origem o Security Group utilizado pela EC2.

O fluxo é:

```text
sistema-escolar-sg
        |
        | TCP 3306
        v
sistema-escolar-db-sg
        |
        v
Amazon RDS
```

A porta MySQL não está liberada diretamente para a internet.

Essa arquitetura separa a exposição da aplicação da exposição da camada
de dados.

---

# 14. Fluxo completo de uma requisição

Quando um usuário realiza uma operação no Sistema Escolar, o fluxo pode
ser representado como:

```text
Usuário
   |
   v
Navegador
   |
   | HTTP / HTTPS
   v
Internet
   |
   v
Internet Gateway
   |
   v
EC2
   |
   v
Nginx
   |
   v
Gunicorn
   |
   v
Flask
   |
   v
Regras da aplicação
   |
   v
MySQL Connector/Python
   |
   | TCP 3306
   v
Amazon RDS MySQL
   |
   v
Banco sistema_escolar
   |
   v
Resultado
   |
   v
Flask
   |
   v
Gunicorn
   |
   v
Nginx
   |
   v
Navegador
```

Esse fluxo representa a arquitetura atualmente implementada.

---

# 15. Validação ponta a ponta

Após a migração para o Amazon RDS, a arquitetura foi validada funcionalmente.

Primeiro, os dados do MariaDB local foram migrados para o MySQL do RDS.

Foram validados:

- tabela `alunos`;
- registros existentes;
- estrutura;
- trigger.

Depois, a aplicação passou a utilizar o endpoint do RDS através das
variáveis de ambiente.

O Gunicorn foi reiniciado e permaneceu:

```text
active (running)
```

O Nginx também respondeu corretamente.

Em seguida, operações foram realizadas através da interface web.

Alterações realizadas pelo navegador foram verificadas diretamente no
Amazon RDS.

Finalmente, o MariaDB local foi parado.

Mesmo assim, a aplicação continuou:

- carregando;
- listando alunos;
- consultando dados;
- realizando alterações;
- realizando exclusões.

Isso confirmou o funcionamento ponta a ponta da nova arquitetura.

---

# 16. Separação de responsabilidades

A arquitetura atual possui responsabilidades mais bem definidas.

```text
Navegador
    |
    v
Nginx
    |  Servidor web / Proxy reverso
    v
Gunicorn
    |  Servidor WSGI
    v
Flask
    |  Aplicação / Backend
    v
MySQL Connector
    |  Acesso aos dados
    v
Amazon RDS
       Persistência
```

### Nginx

Recebe as requisições web e encaminha para a aplicação.

### Gunicorn

Executa a aplicação Python em um servidor WSGI.

### Flask

Processa as requisições e executa a lógica da aplicação.

### Camada de acesso aos dados

Realiza a comunicação entre Python e MySQL.

### Amazon RDS

Mantém a persistência dos dados independentemente da instância EC2.

Essa separação reduz o acoplamento entre os componentes.

---

# 17. Estrutura do projeto

A raiz do projeto permanece organizada em:

```text
Sistema Escolar/
|
|-- app/
|-- docs/
|   `-- aws/
|-- infra/
|-- scripts/
|-- tests/
|-- venv/
|-- .gitignore
|-- README.md
`-- requirements.txt
```

### `app/`

Contém o código da aplicação.

### `docs/`

Contém a documentação geral do projeto.

### `docs/aws/`

Contém a documentação específica da infraestrutura AWS.

Atualmente inclui documentos relacionados a:

- rede;
- Security Groups;
- EC2;
- deploy;
- DNS/HTTPS/DDNS;
- Amazon RDS e camada privada.

### `infra/`

Reservado para componentes relacionados à infraestrutura e futuras
implementações de Infrastructure as Code.

### `scripts/`

Reservado para scripts de automação e suporte.

### `tests/`

Reservado para testes automatizados.

### `venv/`

Ambiente virtual Python utilizado no desenvolvimento.

O diretório não deve ser versionado no Git.

---

# 18. Princípios utilizados na arquitetura

## Separação de responsabilidades

Cada componente possui uma função específica.

Aplicação e banco de dados não estão mais concentrados no mesmo serviço.

## Segurança por camadas

A camada web pode receber tráfego externo, enquanto o banco permanece
na camada privada.

## Menor exposição necessária

O RDS não possui acesso público e sua porta `3306` é restrita à camada
de aplicação.

## Configuração fora do código

Informações específicas do ambiente e credenciais são fornecidas por
variáveis de ambiente.

## Evolução incremental

Cada nova tecnologia é incorporada depois da compreensão e validação da
etapa anterior.

## Documentação como parte da implementação

As mudanças arquiteturais são registradas junto com o projeto.

## Controle de custos

Recursos são adicionados somente quando possuem uma função necessária
para o laboratório.

Por exemplo, a arquitetura atual não utiliza NAT Gateway porque a
comunicação EC2 → RDS ocorre internamente pela VPC e não necessita dele.

## Preparação para automação

A infraestrutura foi inicialmente construída manualmente para aprendizado.

Uma evolução futura poderá reproduzir esses recursos utilizando
Infrastructure as Code.

---

# 19. Estado atual da arquitetura

## Implementado

- aplicação Python;
- Flask;
- interface web;
- templates HTML;
- operações CRUD;
- regras de negócio;
- Git e GitHub;
- VPC própria;
- subnet pública;
- Internet Gateway;
- Route Table pública;
- Security Group da aplicação;
- Amazon EC2;
- Linux;
- Nginx;
- Gunicorn;
- serviço systemd;
- variáveis de ambiente;
- duas subnets privadas;
- Route Table privada;
- DB Subnet Group;
- Security Group exclusivo do banco;
- Amazon RDS for MySQL;
- migração MariaDB → MySQL;
- comunicação EC2 → RDS pela VPC;
- banco sem acesso público;
- validação ponta a ponta da aplicação com o RDS.

## Em evolução

- DNS e HTTPS;
- estratégia de backup e recuperação;
- monitoramento e observabilidade;
- automação do deploy.

## Planejado

- Docker;
- CI/CD;
- Infrastructure as Code com Terraform;
- melhorias de disponibilidade;
- gerenciamento de segredos;
- monitoramento centralizado.

---

# 20. Arquitetura atual resumida

```text
                         INTERNET
                             |
                             v
                    Internet Gateway
                             |
                             v
                +-------------------------+
                |   VPC 10.0.0.0/16      |
                |                         |
                |   SUBNET PÚBLICA       |
                |   10.0.1.0/24          |
                |          |              |
                |          v              |
                |        EC2              |
                |          |              |
                |     +----+----+         |
                |     | Nginx   |         |
                |     | Gunicorn|         |
                |     | Flask   |         |
                |     +----+----+         |
                |          |              |
                |          | TCP 3306     |
                |          v              |
                |   SUBNETS PRIVADAS      |
                |                         |
                |   10.0.2.0/24           |
                |   10.0.3.0/24           |
                |          |              |
                |          v              |
                |    Amazon RDS           |
                |    MySQL 8.4            |
                |          |              |
                |          v              |
                |   sistema_escolar       |
                |                         |
                +-------------------------+
```

A principal evolução arquitetural até este ponto foi:

```text
ANTES

EC2
|-- Aplicação
`-- Banco MariaDB


AGORA

EC2
`-- Aplicação
       |
       | Rede privada da VPC
       v
   Amazon RDS
   `-- MySQL
```

A aplicação e o banco agora possuem responsabilidades separadas e se
comunicam internamente através da infraestrutura de rede da AWS.

---

# 21. Próximos passos arquiteturais

Com a separação entre aplicação e banco concluída, as próximas evoluções
podem ser realizadas sem alterar o princípio básico da arquitetura.

A evolução planejada é:

```text
Arquitetura AWS atual
        |
        v
Containerização
        |
        v
CI/CD
        |
        v
Infrastructure as Code
        |
        v
Monitoramento / Observabilidade
        |
        v
Evoluções de disponibilidade e segurança
```

O objetivo continuará sendo adicionar complexidade somente quando ela
resolver um problema real ou contribuir diretamente para o aprendizado
técnico do projeto.