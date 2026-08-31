# Sistema Escolar — Backend

## 1. Objetivo deste documento

Este documento descreve o funcionamento do **backend do Sistema Escolar**, apresentando as tecnologias utilizadas, suas responsabilidades, as regras de negócio implementadas e a comunicação entre a aplicação, a interface e o banco de dados.

O objetivo é documentar como a lógica interna do sistema foi construída e como o backend evoluiu desde a primeira versão executada pelo terminal até a atual aplicação web utilizando Flask.

Assim como os demais documentos do projeto, este arquivo será atualizado conforme novas funcionalidades e tecnologias forem incorporadas.

---

## 2. O que é o backend

O backend representa a parte da aplicação responsável pelo processamento das informações e pela execução das regras do sistema.

Enquanto a interface permite que o usuário visualize informações e realize ações, o backend recebe essas solicitações, processa os dados, aplica as regras de negócio e realiza a comunicação com o banco de dados.

De forma simplificada:

Usuário
   |
   v
Interface
   |
   v
Backend Python
   |
   +--> Validações
   |
   +--> Regras de negócio
   |
   +--> Operações CRUD
   |
   v
Banco de Dados MySQL

Na versão web, o Flask permite que essa comunicação seja realizada através de requisições HTTP.

---

## 3. Tecnologias utilizadas

O backend do Sistema Escolar utiliza atualmente as seguintes tecnologias:

| Tecnologia | Responsabilidade |
|---|---|
| Python | Linguagem principal utilizada para desenvolver a lógica da aplicação |
| Flask | Framework web responsável pelas rotas e comunicação entre navegador e aplicação Python |
| MySQL | Banco de dados relacional utilizado para persistência das informações |
| MySQL Connector/Python | Biblioteca responsável pela comunicação entre Python e MySQL |
| HTML | Estrutura das páginas apresentadas ao usuário |
| CSS | Estilização da interface web |
| Jinja2 | Mecanismo de templates utilizado pelo Flask para gerar páginas HTML dinamicamente |
| Git | Controle de versão do código-fonte |
| GitHub | Repositório remoto utilizado para armazenar e acompanhar a evolução do projeto |
| pip | Gerenciador utilizado para instalar as dependências Python |
| venv | Ambiente virtual utilizado para isolar as dependências do projeto |

As dependências necessárias para execução da aplicação são registradas no arquivo:

requirements.txt

Isso permite que o ambiente Python necessário para executar o projeto possa ser reconstruído posteriormente.

---

## 4. Evolução do backend

O backend foi desenvolvido de forma incremental.

A primeira versão do Sistema Escolar utilizava uma interface CLI executada diretamente pelo terminal.

Nesse estágio, o Python já era responsável pelas principais funcionalidades do sistema:

- cadastro de alunos;
- listagem de alunos;
- busca por nome;
- busca por matrícula;
- edição de alunos;
- exclusão de alunos;
- validação das notas;
- cálculo da média;
- definição da situação acadêmica;
- comunicação com o banco de dados MySQL.

Essa etapa foi importante para validar a lógica da aplicação antes da implementação da interface web.

Posteriormente, o projeto passou a utilizar Flask, permitindo que as funcionalidades fossem disponibilizadas através de um navegador.

Essa evolução pode ser representada como:

CLI
 |
 v
Python
 |
 v
MySQL

        ↓ evolução

Navegador
 |
 v
HTML / CSS
 |
 v
Flask
 |
 v
Python
 |
 v
MySQL

A lógica principal do sistema continua sendo executada no backend. O que mudou foi principalmente a forma como o usuário interage com a aplicação.

---

## 5. Responsabilidades do backend

O backend concentra as operações necessárias para o funcionamento do Sistema Escolar.

Entre suas principais responsabilidades estão:

### 5.1 Receber dados

O sistema recebe informações fornecidas pelo usuário, como:

- nome do aluno;
- matrícula;
- primeira nota;
- segunda nota.

Essas informações podem ser recebidas pela interface da aplicação e posteriormente processadas pelo backend.

---

### 5.2 Validar informações

Antes de armazenar ou processar determinadas informações, o backend realiza validações.

Entre as validações existentes estão:

- impedir cadastro de aluno sem nome;
- impedir notas inferiores a 0;
- impedir notas superiores a 10;
- validar os dados necessários antes da execução das operações.

Essas validações evitam que informações inválidas sejam processadas ou armazenadas no banco de dados.

---

## 6. Regras de negócio

As regras de negócio determinam como o Sistema Escolar deve se comportar.

Uma das principais regras implementadas é o cálculo da média do aluno.

A média é calculada utilizando duas notas:

media = (nota1 + nota2) / 2

Após o cálculo, o sistema determina automaticamente a situação acadêmica.

As regras utilizadas são:

Média >= 7        -> Aprovado
Média >= 5 e < 7  -> Recuperação
Média < 5         -> Reprovado

Dessa forma, a situação do aluno não precisa ser definida manualmente pelo usuário.

O próprio backend realiza essa decisão de acordo com as regras estabelecidas.

---

## 7. Operações CRUD

O backend implementa operações CRUD para gerenciamento dos alunos.

CRUD representa quatro operações fundamentais realizadas sobre os dados:

| Operação | SQL | Função |
|---|---|---|
| Create | INSERT | Cadastrar um aluno |
| Read | SELECT | Consultar ou listar alunos |
| Update | UPDATE | Alterar informações de um aluno |
| Delete | DELETE | Excluir um aluno |

No Sistema Escolar, essas operações permitem realizar o ciclo completo de gerenciamento dos registros.

### Create

Permite cadastrar um novo aluno no sistema.

### Read

Permite consultar os alunos cadastrados.

O sistema possui operações como:

- listar alunos;
- buscar aluno por nome;
- buscar aluno por matrícula.

### Update

Permite editar informações de um aluno existente.

### Delete

Permite excluir um aluno do banco de dados.

---

## 8. Camada de acesso aos dados

O acesso ao banco de dados é separado da interface da aplicação.

A responsabilidade dessa camada é executar operações relacionadas ao armazenamento e recuperação das informações.

Conceitualmente:

Interface
   |
   v
Backend
   |
   v
Regras de negócio
   |
   v
Repository
   |
   v
MySQL

Essa separação evita que comandos SQL sejam espalhados por diferentes partes da aplicação.

O repositório concentra operações relacionadas aos alunos, como:

- cadastrar;
- consultar;
- listar;
- atualizar;
- excluir.

Essa organização também facilita futuras alterações no sistema.

---

## 9. Comunicação com o MySQL

O Sistema Escolar utiliza o **MySQL Connector/Python** para estabelecer a comunicação entre a aplicação Python e o banco de dados MySQL.

O fluxo básico ocorre da seguinte maneira:

Aplicação Python
      |
      v
MySQL Connector/Python
      |
      v
Servidor MySQL
      |
      v
Banco sistema_escolar
      |
      v
Tabela de alunos

A aplicação envia comandos SQL através da conexão com o banco.

O MySQL executa a operação e retorna o resultado para o backend.

Dependendo da operação, o backend pode então apresentar esse resultado ao usuário.

A estrutura completa do banco de dados será documentada separadamente no documento dedicado ao banco.

---

## 10. Flask e aplicação web

O Flask foi incorporado ao projeto para transformar o Sistema Escolar em uma aplicação web.

Ele funciona como uma camada de comunicação entre o navegador e a lógica Python.

De maneira simplificada:

Navegador
    |
    | Requisição HTTP
    v
Rota Flask
    |
    v
Lógica Python
    |
    v
Repository
    |
    v
MySQL
    |
    v
Resultado
    |
    v
Flask
    |
    | Resposta HTTP
    v
Navegador

As rotas determinam qual ação será executada quando o usuário acessar determinada página ou enviar informações através da interface.

---

## 11. Templates HTML

O Flask utiliza templates HTML para gerar as páginas apresentadas ao usuário.

Esses arquivos ficam armazenados no diretório:

templates/

Entre os templates utilizados no projeto estão:

index.html
editar.html

Os templates permitem separar a estrutura visual da aplicação da lógica Python.

Além disso, o Flask utiliza o mecanismo de templates **Jinja2**, permitindo inserir informações processadas pelo backend dentro das páginas HTML.

---

## 12. Arquivos estáticos

Arquivos responsáveis pela apresentação visual ficam separados da lógica Python.

Eles são armazenados no diretório:

static/

Nesse diretório podem existir arquivos como:

styles.css

Essa organização permite manter responsabilidades separadas:

HTML     -> estrutura da página
CSS      -> apresentação visual
Flask    -> comunicação web
Python   -> lógica da aplicação
MySQL    -> persistência dos dados

---

## 13. Fluxo de uma operação

Uma operação realizada através da aplicação web pode ser representada da seguinte maneira:

1. O usuário acessa a aplicação pelo navegador.
2. O navegador envia uma requisição HTTP para o Flask.
3. Uma rota Flask recebe a solicitação.
4. Os dados são enviados para a lógica Python.
5. O backend realiza as validações necessárias.
6. As regras de negócio são executadas.
7. Caso necessário, o repositório realiza uma operação no MySQL.
8. O banco de dados retorna o resultado.
9. O Flask processa a resposta.
10. O resultado é apresentado novamente ao usuário através do navegador.

Visualmente:

Usuário
   |
   v
HTML
   |
   v
Flask
   |
   v
Validação
   |
   v
Regra de negócio
   |
   v
Repository
   |
   v
MySQL
   |
   v
Resultado
   |
   v
Flask
   |
   v
HTML
   |
   v
Usuário

---

## 14. Organização e separação de responsabilidades

Uma das decisões tomadas durante a evolução do projeto foi evitar concentrar todas as funcionalidades em um único arquivo.

A aplicação passou a separar responsabilidades relacionadas a:

- interface;
- entrada de dados;
- regras de negócio;
- acesso ao banco de dados;
- aplicação web.

Essa organização possui vantagens importantes:

- facilita a leitura do código;
- reduz duplicação;
- facilita manutenção;
- permite testar componentes individualmente;
- facilita futuras alterações;
- prepara o projeto para crescer de maneira organizada.

Esse princípio será mantido durante as próximas etapas do projeto.

---

## 15. Tratamento e validação de dados

O backend também possui a responsabilidade de impedir que determinados dados inválidos avancem pelo sistema.

Por exemplo, uma nota escolar deve permanecer dentro do intervalo definido:

0 <= nota <= 10

Da mesma forma, campos obrigatórios não devem ser processados sem conteúdo válido.

Esse tipo de validação é importante porque a interface não deve ser considerada a única responsável pela integridade das informações.

As regras importantes pertencem ao backend.

---

## 16. Dependências do backend

As bibliotecas Python utilizadas pelo projeto são registradas no arquivo:

requirements.txt

Esse arquivo permite instalar as dependências necessárias utilizando o gerenciador de pacotes Python.

O projeto também utiliza um ambiente virtual:

venv/

O ambiente virtual mantém as dependências do Sistema Escolar isoladas das demais instalações Python existentes na máquina.

O diretório `venv` não deve ser enviado para o GitHub.

Somente a lista das dependências necessárias deve ser versionada através do `requirements.txt`.

---

## 17. Versionamento

O backend é versionado utilizando Git.

As alterações realizadas no código podem seguir o fluxo:

Desenvolvimento
     |
     v
git add
     |
     v
git commit
     |
     v
git push
     |
     v
GitHub

Isso cria um histórico da evolução do projeto e permite acompanhar as alterações realizadas ao longo do desenvolvimento.

O versionamento também será fundamental futuramente para implementação do pipeline de CI/CD.

---

## 18. Estado atual do backend

No momento desta documentação, o backend possui:

**Implementado:**

- aplicação desenvolvida em Python;
- operações CRUD;
- cadastro de alunos;
- listagem de alunos;
- busca por nome;
- busca por matrícula;
- edição de alunos;
- exclusão de alunos;
- validação das notas;
- cálculo automático da média;
- definição da situação acadêmica;
- persistência em MySQL;
- comunicação Python/MySQL;
- estrutura web utilizando Flask;
- templates HTML;
- arquivos estáticos;
- gerenciamento das dependências através do requirements.txt;
- versionamento utilizando Git e GitHub.

**Em evolução:**

- revisão da integração completa da aplicação web;
- validação do fluxo entre interface, Flask, regras de negócio e banco de dados;
- preparação da aplicação para implantação.

**Planejado:**

- testes automatizados;
- melhorias no tratamento de erros;
- autenticação e controle de acesso;
- preparação para execução em ambiente Linux;
- containerização com Docker;
- implantação na AWS;
- pipeline CI/CD;
- monitoramento e logs.

---

## 19. Preparação para Cloud e DevOps

A organização atual do backend também possui um objetivo importante: preparar a aplicação para as próximas etapas do projeto.

Antes da implantação em nuvem, será necessário garantir que a aplicação possa ser executada de forma previsível fora do ambiente de desenvolvimento.

O fluxo de evolução planejado é:

Backend local
     |
     v
Aplicação web validada
     |
     v
Execução em Linux
     |
     v
Deploy AWS
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
Monitoramento

Essa evolução permitirá utilizar o Sistema Escolar não apenas como projeto de desenvolvimento Python, mas também como laboratório prático para estudos de **Cloud e DevOps**.

---

## 20. Próxima etapa

Após a documentação do backend, o próximo componente será o banco de dados.

O documento seguinte detalhará:

- função do banco de dados no projeto;
- MySQL;
- estrutura utilizada;
- tabela de alunos;
- campos armazenados;
- persistência;
- operações SQL;
- integração entre Python e MySQL;
- evolução futura para banco de dados em nuvem.

A próxima documentação será:

docs/04-database.md
