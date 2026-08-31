# Sistema Escolar — Arquitetura

## 1. Objetivo deste documento

Este documento descreve a arquitetura do **Sistema Escolar**, apresentando os principais componentes da aplicação, suas responsabilidades e a forma como eles se comunicam.

A arquitetura será documentada de forma incremental. Isso significa que este arquivo será atualizado conforme o projeto evoluir, principalmente durante a futura implantação em ambiente AWS.

O objetivo é registrar não apenas a arquitetura final, mas também as decisões técnicas tomadas durante a evolução do projeto.

---

## 2. Arquitetura atual

Atualmente, o Sistema Escolar é executado em ambiente local e possui três componentes principais:

1. Interface da aplicação;
2. Backend desenvolvido em Python;
3. Banco de dados MySQL.

De forma simplificada, o funcionamento pode ser representado como:

```text
Usuário
   |
   v
Interface da aplicação
   |
   v
Aplicação Python
   |
   v
Regras de negócio
   |
   v
Camada de acesso aos dados
   |
   v
Banco de Dados MySQL
```

Na aplicação web, o fluxo passa a ocorrer através do navegador:

```text
Navegador
    |
    | Requisição HTTP
    v
Aplicação Flask
    |
    v
Lógica da aplicação
    |
    v
Acesso aos dados
    |
    v
MySQL
    |
    | Resultado
    v
Aplicação Flask
    |
    | Resposta HTTP / HTML
    v
Navegador
```

---

## 3. Componentes da aplicação

### ### 3.1 Interface

O Sistema Escolar iniciou sua evolução como uma aplicação **CLI (Command-Line Interface)** desenvolvida em Python e executada localmente através do terminal.

Na primeira versão, o usuário interagia com o sistema por meio de um menu textual, utilizando o teclado para selecionar operações como cadastro, listagem, busca, edição e exclusão de alunos.

Essa abordagem permitiu desenvolver e validar inicialmente as regras de negócio e as operações CRUD antes da implementação de uma interface web.

Durante o desenvolvimento local, a aplicação foi executada principalmente em ambiente Windows, utilizando o **PowerShell** como terminal e o **PyCharm** como ambiente de desenvolvimento.

Posteriormente, o projeto evoluiu para uma aplicação web, permitindo que a interação com o Sistema Escolar passasse a ocorrer através de um navegador utilizando HTML, CSS e Flask.

```text
templates/
static/
```

O diretório `templates` contém os arquivos HTML utilizados para apresentar as páginas ao usuário.

Atualmente, entre os templates existentes estão:

```text
index.html
editar.html
```


O diretório `static` é utilizado para armazenar arquivos estáticos da aplicação, como CSS.

Essa separação evita misturar a apresentação visual diretamente com a lógica Python.

---

## 4. Backend

O backend é desenvolvido em **Python** e concentra a lógica responsável pelo funcionamento do Sistema Escolar.

Entre suas responsabilidades estão:

* receber dados informados pelo usuário;
* validar informações;
* executar regras de negócio;
* calcular a média dos alunos;
* determinar a situação acadêmica;
* solicitar operações no banco de dados;
* devolver os resultados para a interface.

Na versão web, o **Flask** é utilizado para permitir a comunicação entre o navegador e a aplicação Python.

O Flask será responsável por receber requisições HTTP, executar a lógica necessária e retornar páginas HTML ou redirecionamentos para o navegador.

---

## 5. Regras de negócio

As regras de negócio representam decisões que pertencem ao funcionamento do Sistema Escolar.

Um exemplo é a definição da situação acadêmica do aluno.

A média é calculada utilizando duas notas:

```text
media = (nota1 + nota2) / 2
```

A situação é determinada de acordo com as seguintes regras:

```text
Média >= 7               -> Aprovado
Média >= 5 e < 7         -> Recuperação
Média < 5                -> Reprovado
```

Também existem validações para impedir:

* notas inferiores a 0;
* notas superiores a 10;
* cadastro de aluno sem nome.

Manter essas regras separadas da interface facilita futuras alterações e reduz a duplicação de código.

---

## 6. Camada de acesso aos dados

A comunicação entre a aplicação Python e o banco de dados é realizada por uma camada responsável pelo acesso aos dados.

Essa camada concentra operações como:

```text
Cadastrar aluno
Consultar aluno
Listar alunos
Editar aluno
Excluir aluno
```

No banco de dados, essas operações correspondem principalmente aos comandos:

```text
CREATE / INSERT
READ   / SELECT
UPDATE / UPDATE
DELETE / DELETE
```

Esse conjunto de operações é conhecido como **CRUD**.

A separação da camada de acesso aos dados evita que comandos SQL fiquem espalhados por diferentes partes da aplicação.

---

## 7. Banco de dados

O Sistema Escolar utiliza atualmente o **MySQL** como banco de dados relacional.

O banco é responsável pela persistência das informações dos alunos.

Isso significa que os dados continuam armazenados mesmo depois que a aplicação Python é encerrada.

A aplicação utiliza o **MySQL Connector/Python** para realizar a comunicação entre Python e MySQL.

A estrutura detalhada do banco, incluindo banco de dados, tabela, campos e operações SQL, será documentada separadamente em:

```text
docs/database.md
```

---

## 8. Separação de responsabilidades

Uma das decisões adotadas durante a evolução do projeto foi evitar concentrar todas as funcionalidades em um único arquivo Python.

A aplicação passou a ser organizada de acordo com diferentes responsabilidades.

De forma conceitual:

```text
Interface
    |
    v
Rotas / Entrada
    |
    v
Regras de negócio
    |
    v
Repositório
    |
    v
Banco de dados
```

Cada camada possui uma responsabilidade.

### Interface

Apresenta informações e recebe ações do usuário.

### Rotas / Entrada

Recebe as solicitações realizadas através da aplicação.

### Regras de negócio

Decidem como o sistema deve se comportar.

### Repositório

Executa operações relacionadas ao armazenamento e recuperação dos dados.

### Banco de dados

Armazena as informações permanentemente.

Essa separação facilita manutenção, testes e futuras evoluções da aplicação.

---

## 9. Estrutura atual do projeto

A raiz do projeto está organizada para separar aplicação, documentação, infraestrutura, scripts e testes.

```text
Sistema Escolar/
|
|-- app/
|-- docs/
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

Contém a documentação técnica do projeto.

### `infra/`

Reservado para os arquivos relacionados à infraestrutura do projeto.

Essa pasta ganhará maior importância durante a implantação em nuvem e a futura utilização de Infrastructure as Code.

### `scripts/`

Reservado para scripts de automação e suporte ao projeto.

### `tests/`

Reservado para testes automatizados.

### `venv/`

Ambiente virtual utilizado localmente para isolar as dependências Python.

O diretório `venv` é um recurso do ambiente de desenvolvimento e não deve ser versionado no Git.

### `requirements.txt`

Registra as dependências Python necessárias para executar a aplicação.

---

## 10. Princípios utilizados na arquitetura

Durante a construção do Sistema Escolar, alguns princípios estão sendo adotados.

### Separação de responsabilidades

Cada parte do sistema deve possuir uma responsabilidade clara.

### Evolução incremental

Novas tecnologias são adicionadas somente quando existe uma necessidade técnica ou um objetivo de aprendizado relacionado ao projeto.

### Versionamento

As alterações relevantes são registradas utilizando Git e enviadas ao repositório GitHub.

### Documentação como parte do projeto

A documentação evolui junto com o código.

Uma implementação não é considerada completamente documentada apenas porque funciona: também é necessário registrar seu funcionamento, suas decisões e sua finalidade.

### Preparação para automação

A estrutura do projeto busca permitir que processos atualmente executados manualmente possam ser automatizados futuramente.

---

## 11. Arquitetura planejada para Cloud

O próximo grande estágio do projeto será retirar a aplicação de um ambiente exclusivamente local e disponibilizá-la em infraestrutura de nuvem.

Essa arquitetura **ainda não representa o ambiente atualmente implementado**.

Ela será construída e documentada progressivamente.

Uma visão inicial da evolução esperada é:

```text
                         INTERNET
                             |
                             v
                      Aplicação Web
                             |
                             v
                    Infraestrutura AWS
                             |
                 +-----------+-----------+
                 |                       |
                 v                       v
          Aplicação Python          Banco de Dados
              / Flask                   MySQL
```

Durante essa evolução serão avaliados serviços e tecnologias como:

* Amazon EC2;
* Amazon VPC;
* Security Groups;
* Amazon RDS;
* Linux;
* servidor de aplicação;
* proxy reverso;
* Docker;
* GitHub Actions;
* CI/CD;
* Terraform;
* monitoramento e logs.

Cada tecnologia será incorporada somente após entendermos sua responsabilidade dentro da arquitetura.

---

## 12. Evolução futura da arquitetura

A evolução planejada pode ser dividida conceitualmente nas seguintes etapas:

```text
Aplicação Local
      |
      v
Aplicação Web Local
      |
      v
Preparação para Deploy
      |
      v
Infraestrutura AWS
      |
      v
Banco de Dados Gerenciado
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
Monitoramento e Operação
```

Essa abordagem permite estudar cada camada individualmente e compreender qual problema cada tecnologia resolve.

---

## 13. Estado atual da arquitetura

No momento desta documentação:

**Implementado:**

* aplicação Python;
* operações CRUD;
* banco de dados MySQL;
* persistência dos dados;
* organização do código em diferentes responsabilidades;
* ambiente virtual Python;
* estrutura web;
* Flask;
* templates HTML;
* arquivos estáticos;
* Git e GitHub;
* estrutura inicial de documentação.

**Em validação e evolução:**

* integração completa entre Flask, templates HTML, regras de negócio e banco de dados;
* revisão da aplicação web antes do deploy.

**Planejado:**

* implantação na AWS;
* arquitetura de rede;
* banco de dados gerenciado;
* containerização;
* pipeline CI/CD;
* Infrastructure as Code;
* monitoramento.

---

## 14. Próximo passo arquitetural

Antes de iniciar a infraestrutura AWS, será realizada uma revisão da aplicação local.

O objetivo será validar o caminho completo:

```text
Usuário
   |
   v
HTML
   |
   v
Flask
   |
   v
Regras de negócio
   |
   v
Repositório
   |
   v
MySQL
   |
   v
Resposta apresentada ao usuário
```

Quando esse fluxo estiver validado localmente, a aplicação estará preparada para iniciar sua próxima fase: **implantação e operação em infraestrutura de nuvem**.
