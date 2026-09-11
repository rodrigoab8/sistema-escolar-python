# 04 - Deploy da Aplicação na AWS EC2

## 1. Objetivo

Este documento descreve o processo de preparação da instância EC2 para executar o projeto **Sistema Escolar**, desenvolvido em Python com Flask e banco de dados relacional.

O objetivo não é apenas registrar os comandos utilizados, mas também documentar **por que cada configuração foi necessária**.

A arquitetura utilizada nesta etapa é:

```text
Usuário / Navegador
        |
        | HTTP
        v
Security Group
        |
        v
      EC2
   Amazon Linux
        |
        +--------------------+
        |                    |
        v                    v
  Aplicação Flask        MariaDB
      Python          sistema_escolar
```

Nesta fase, aplicação e banco de dados estão hospedados na mesma instância EC2.

---

# 2. Ajuste das Inbound Rules

## O que são Inbound Rules?

As **Inbound Rules** são regras de entrada configuradas no Security Group associado à instância EC2.

Elas determinam:

> Qual tráfego pode entrar na instância, através de qual protocolo, porta e origem.

O Security Group funciona como um firewall virtual da instância.

---

## Porta 22 - SSH

Para administrar a EC2 remotamente, foi necessário permitir tráfego SSH.

Configuração utilizada:

```text
Tipo: SSH
Protocolo: TCP
Porta: 22
Origem: Meu IP
```

### Por que utilizar "Meu IP"?

Restringir o SSH ao endereço IP utilizado para administração reduz a superfície de ataque.

Evita-se utilizar:

```text
0.0.0.0/0
```

para SSH sempre que possível, pois isso permitiria tentativas de conexão vindas de qualquer endereço IPv4 da internet.

### Conceito aprendido

Liberar uma porta no Security Group **não significa que existe automaticamente um serviço naquela porta**.

O Security Group apenas permite que o tráfego chegue à instância.

Também é necessário existir um serviço escutando naquela porta.

Exemplo:

```text
Internet
   |
   v
Security Group
   |
   | TCP/22 permitido
   v
EC2
   |
   v
Servidor SSH
```

---

# 3. Acesso à EC2 via SSH

A administração da instância foi realizada através de SSH utilizando a chave privada `.pem` criada durante o provisionamento da EC2.

Exemplo:

```bash
ssh -i minha-chave.pem ec2-user@IP_PUBLICO_DA_EC2
```

Após a autenticação:

```text
Windows
   |
   | SSH + chave privada
   v
Internet
   |
   v
Security Group
   |
   v
EC2 Amazon Linux
```

## Por que utilizar uma chave `.pem`?

A chave privada é utilizada para comprovar que o usuário possui autorização para acessar a instância.

Ela não deve:

- ser enviada ao GitHub;
- ser compartilhada publicamente;
- ficar armazenada dentro do repositório do projeto.

---

# 4. Banco de dados no ambiente local

Durante o desenvolvimento inicial, o Sistema Escolar utilizava:

```text
Windows
   |
   v
Aplicação Python / Flask
   |
   v
MySQL
   |
   v
sistema_escolar
```

O banco possuía as estruturas e dados utilizados durante o desenvolvimento e os testes da aplicação.

Ao realizar o deploy para a AWS, surgiu um novo ambiente:

```text
EC2
Amazon Linux
```

O objetivo passou a ser permitir que a aplicação também funcionasse nesse ambiente sem manter dependência do computador Windows.

---

# 5. MariaDB na EC2

No ambiente Linux da EC2 foi utilizado o **MariaDB** como servidor de banco de dados.

A arquitetura passou a ser:

```text
EC2
 |
 +-- Aplicação Flask
 |
 +-- MariaDB
      |
      +-- sistema_escolar
```

## Por que utilizar MariaDB?

MariaDB possui alta compatibilidade com MySQL e permite utilizar a mesma abordagem SQL empregada pelo projeto.

O código Python continua utilizando:

```python
import mysql.connector
```

A biblioteca atua como cliente responsável pela comunicação entre a aplicação Python e o servidor de banco de dados.

---

# 6. Migração do banco

O banco existente no ambiente Windows precisava ser disponibilizado no novo ambiente.

O processo conceitual foi:

```text
MySQL - Windows
      |
      | exportação
      v
 arquivo .sql
      |
      | transferência/importação
      v
MariaDB - EC2
      |
      v
sistema_escolar
```

Isso permitiu preservar a estrutura e os dados existentes em vez de reconstruir manualmente o banco na EC2.

## Importante

Existem dois conceitos diferentes neste projeto:

### Importação do banco

A migração utiliza um arquivo SQL contendo a estrutura e/ou os dados do banco.

```text
MySQL
  ↓
arquivo .sql
  ↓
MariaDB
```

### `import os` no Python

O comando:

```python
import os
```

não importa o banco de dados.

Ele permite que o Python acesse recursos fornecidos pelo sistema operacional, incluindo **variáveis de ambiente**.

---

# 7. Adaptação da conexão com o banco

Inicialmente, uma aplicação pode possuir configurações diretamente no código, por exemplo:

```python
mysql.connector.connect(
    host="localhost",
    user="usuario",
    password="senha",
    database="sistema_escolar"
)
```

Essa estratégia gera problemas quando o mesmo projeto precisa funcionar em ambientes diferentes.

Por isso, a conexão foi modificada para utilizar variáveis de ambiente.

Código utilizado:

```python
# CONEXÃO COM BANCO #

import os
import mysql.connector


def conectar():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "sistema_escolar")
    )
```

---

# 8. Por que utilizar `os.getenv()`?

`os.getenv()` permite que a aplicação leia configurações fornecidas pelo ambiente onde está sendo executada.

Por exemplo:

```python
os.getenv("DB_USER")
```

significa:

> Obtenha do sistema operacional o valor armazenado na variável `DB_USER`.

Com isso, não é necessário alterar o código para cada ambiente.

---

# 9. Valores padrão

Algumas variáveis possuem um segundo parâmetro:

```python
os.getenv("DB_HOST", "localhost")
```

Nesse caso:

```text
Existe DB_HOST?
      |
   +--+--+
   |     |
  SIM   NÃO
   |     |
   v     v
valor  localhost
```

O mesmo acontece com:

```python
os.getenv("DB_NAME", "sistema_escolar")
```

Se `DB_NAME` não estiver configurada, será utilizado:

```text
sistema_escolar
```

Já:

```python
os.getenv("DB_USER")
os.getenv("DB_PASSWORD")
```

não possuem valores padrão.

As credenciais precisam ser fornecidas pelo ambiente.

---

# 10. Mesmo código em Windows e Linux

Uma das principais melhorias realizadas foi separar:

```text
CÓDIGO
```

de:

```text
CONFIGURAÇÃO DO AMBIENTE
```

O código da aplicação permanece igual.

## Windows

```text
Aplicação Flask
      |
      | mysql.connector
      v
MySQL
      |
      v
sistema_escolar
```

As variáveis de ambiente do Windows fornecem as configurações necessárias.

## AWS EC2

```text
Aplicação Flask
      |
      | mysql.connector
      v
MariaDB
      |
      v
sistema_escolar
```

As variáveis configuradas no Linux fornecem as credenciais correspondentes ao ambiente EC2.

Portanto:

```text
             MESMO CÓDIGO
                  |
          +-------+-------+
          |               |
          v               v
       Windows           Linux
          |               |
        MySQL          MariaDB
```

Essa abordagem melhora a **portabilidade da aplicação**.

---

# 11. Segurança das credenciais

Uma vantagem importante das variáveis de ambiente é evitar armazenar informações sensíveis diretamente no código-fonte.

Evitar:

```python
password="minha_senha"
```

Principalmente quando o projeto está versionado com Git e hospedado em um repositório remoto.

A estratégia adotada é:

```text
GitHub
  |
  | código
  v
Aplicação
  |
  | lê configuração
  v
Variáveis de ambiente
```

Assim, as credenciais não precisam fazer parte do repositório.

---

# 12. Código-fonte na EC2

O projeto foi armazenado no GitHub e posteriormente clonado para a EC2.

Fluxo:

```text
Desenvolvimento local
       |
       | git push
       v
     GitHub
       |
       | git clone
       v
      EC2
```

Na EC2 foi possível verificar a estrutura do projeto utilizando:

```bash
ls -la
```

O repositório passou a existir diretamente no servidor Linux.

---

# 13. Ambiente virtual Python

Após clonar o projeto, foi criado um ambiente virtual Python:

```text
venv
```

A função do ambiente virtual é isolar as dependências utilizadas pelo projeto.

Conceitualmente:

```text
EC2
 |
 +-- Python do sistema
 |
 +-- sistema-escolar-python
      |
      +-- venv
           |
           +-- Flask
           +-- mysql-connector-python
           +-- outras dependências
```

Isso evita instalar todas as bibliotecas diretamente no Python utilizado pelo sistema operacional.

Após ativado, o terminal apresenta:

```text
(venv)
```

Exemplo:

```text
(venv) [ec2-user@ip-10-0-1-102 sistema-escolar-python]$
```

Isso indica que os comandos Python e `pip` executados naquele terminal estão utilizando o ambiente virtual.

---

# 14. requirements.txt

O projeto possui um arquivo:

```text
requirements.txt
```

Ele registra as dependências Python necessárias para executar a aplicação.

Entre elas estão:

```text
Flask
mysql-connector-python
Jinja2
Werkzeug
```

## Por que isso é importante?

Não é necessário lembrar manualmente quais bibliotecas devem ser instaladas em cada servidor.

O fluxo passa a ser:

```text
Código no GitHub
       |
       v
git clone
       |
       v
criar venv
       |
       v
requirements.txt
       |
       v
instalar dependências
       |
       v
executar aplicação
```

A instalação normalmente é realizada com:

```bash
pip install -r requirements.txt
```

---

# 15. Problema de codificação identificado

Ao verificar o arquivo na EC2 com:

```bash
cat requirements.txt
```

foi observado um caractere estranho antes da primeira dependência:

```text
��blinker==1.9.0
```

Isso indica um possível problema de **codificação do arquivo** criado originalmente no Windows.

Antes da instalação das dependências, esse ponto deve ser corrigido para garantir que o `pip` interprete corretamente o conteúdo do arquivo.

Esse tipo de situação também demonstra uma diferença prática entre ambientes Windows e Linux que deve ser considerada durante processos de deploy.

---

# 16. Persistência dos dados

O uso de:

```python
os.getenv()
```

não é responsável pela persistência dos dados.

Ele é responsável apenas pela **configuração da conexão**.

Quem persiste os dados é o servidor de banco de dados.

Na EC2:

```text
Flask
   |
   | INSERT / UPDATE / DELETE
   v
MariaDB
   |
   v
Arquivos do banco
   |
   v
Armazenamento da EC2
```

Portanto, encerrar a aplicação Flask não apaga os registros existentes no MariaDB.

---

# 17. Situação atual do deploy

Até este ponto, a infraestrutura possui:

```text
AWS
 |
 +-- VPC
 |
 +-- Subnet
 |
 +-- Internet Gateway
 |
 +-- Route Table
 |
 +-- Security Group
 |
 +-- EC2 - Amazon Linux
      |
      +-- SSH
      |
      +-- MariaDB
      |    |
      |    +-- sistema_escolar
      |
      +-- Git
      |
      +-- Projeto clonado
      |
      +-- Python
           |
           +-- venv
           |
           +-- requirements.txt
```

---

# 18. Próximos passos

A próxima etapa será continuar a preparação do ambiente de execução da aplicação.

Fluxo planejado:

```text
Corrigir requirements.txt
        ↓
Instalar dependências
        ↓
Configurar variáveis de ambiente
        ↓
Testar conexão com MariaDB
        ↓
Executar Flask
        ↓
Liberar somente a porta necessária
        ↓
Acessar aplicação pelo navegador
        ↓
Validar CRUD na EC2
```

Posteriormente, a arquitetura poderá evoluir para uma estrutura mais próxima de produção, separando responsabilidades.

Exemplo:

```text
Internet
   |
   v
Load Balancer / Reverse Proxy
   |
   v
Aplicação
   |
   v
Banco de dados gerenciado
```

Uma evolução possível na AWS seria retirar o banco da EC2 e utilizar um serviço gerenciado como Amazon RDS.

---

# 19. Principais conceitos aprendidos

Durante esta etapa foram aplicados conceitos importantes de desenvolvimento, infraestrutura e DevOps:

- Security Groups e controle de tráfego;
- portas TCP;
- SSH;
- autenticação por chave;
- EC2;
- Linux;
- MySQL e MariaDB;
- migração de banco de dados;
- Git e GitHub;
- ambientes virtuais Python;
- gerenciamento de dependências;
- variáveis de ambiente;
- proteção de credenciais;
- separação entre código e configuração;
- portabilidade entre Windows e Linux;
- persistência de dados;
- preparação de ambiente para deploy.

---

# 20. Resumo da decisão arquitetural

O principal objetivo desta etapa foi transformar uma aplicação que funcionava apenas no ambiente local em uma aplicação preparada para diferentes ambientes.

Antes:

```text
Código
  |
  +-- configuração do ambiente
  |
  +-- lógica da aplicação
```

Depois:

```text
                Aplicação
                    |
             Código reutilizável
                    |
          +---------+---------+
          |                   |
     configuração         configuração
       Windows               EC2
          |                   |
          v                   v
        MySQL               MariaDB
```

Essa separação permite que o mesmo projeto seja implantado em ambientes diferentes sem necessidade de alterar o código-fonte para cada servidor.