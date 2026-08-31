# Sistema Escolar — Banco de Dados

## 1. Objetivo deste documento

Este documento descreve a camada de banco de dados do **Sistema Escolar**, apresentando sua finalidade, a tecnologia utilizada, a estrutura dos dados, as operações realizadas e a comunicação entre o backend Python e o MySQL.

O banco de dados representa uma parte fundamental da aplicação, pois é responsável pela **persistência das informações dos alunos**.

Isso permite que os dados permaneçam armazenados mesmo após o encerramento da aplicação.

Assim como os demais componentes do projeto, a camada de banco de dados será documentada e evoluída progressivamente.

---

## 2. Tecnologia utilizada

Atualmente, o Sistema Escolar utiliza:

**MySQL**

O MySQL é um sistema de gerenciamento de banco de dados relacional.

No projeto, ele é responsável pelo armazenamento das informações utilizadas pela aplicação.

A comunicação entre Python e MySQL é realizada utilizando:

**MySQL Connector/Python**

O fluxo básico pode ser representado como:

```text
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
Dados dos alunos
```

---

## 3. Por que utilizar um banco de dados

Nas primeiras etapas de desenvolvimento de uma aplicação, informações podem existir apenas durante a execução do programa.

Entretanto, um sistema real precisa manter seus dados disponíveis mesmo depois que a aplicação é encerrada ou reiniciada.

Essa característica é chamada de **persistência de dados**.

No Sistema Escolar:

```text
Usuário cadastra aluno
        |
        v
Backend processa os dados
        |
        v
MySQL armazena os dados
        |
        v
Aplicação é encerrada
        |
        v
Dados continuam armazenados
```

Quando a aplicação for iniciada novamente, os registros poderão ser consultados no banco.

---

## 4. Banco de dados do projeto

O banco utilizado pelo Sistema Escolar é:

```text
sistema_escolar
```

Ele é responsável por armazenar os dados necessários para o funcionamento da aplicação.

Atualmente, o principal conjunto de informações armazenado é relacionado aos alunos cadastrados no sistema.

---

## 5. Estrutura dos dados dos alunos

Os registros dos alunos possuem informações utilizadas pelas regras de negócio da aplicação.

Entre os dados utilizados estão:

```text
id
matricula
nome
nota1
nota2
status_aluno
```

Cada registro representa um aluno cadastrado no Sistema Escolar.

Conceitualmente:

```text
Aluno
 |
 +-- ID
 |
 +-- Matrícula
 |
 +-- Nome
 |
 +-- Nota 1
 |
 +-- Nota 2
 |
 `-- Status acadêmico
```

### ID

Identificador interno utilizado pelo banco de dados para diferenciar os registros.

### Matrícula

Identificação utilizada pelo Sistema Escolar para localizar determinado aluno.

A matrícula também é utilizada em operações como busca, edição e exclusão.

### Nome

Armazena o nome do aluno.

### Nota 1

Armazena a primeira nota utilizada no cálculo da média.

### Nota 2

Armazena a segunda nota utilizada no cálculo da média.

### Status do aluno

Armazena a situação acadêmica determinada pelas regras de negócio da aplicação.

Os estados utilizados atualmente são:

```text
Aprovado
Recuperação
Reprovado
```

---

## 6. Regras relacionadas às notas

Antes de determinados dados serem armazenados, a aplicação realiza validações.

As notas devem permanecer dentro do intervalo:

```text
0 <= nota <= 10
```

A média é calculada utilizando:

```text
media = (nota1 + nota2) / 2
```

A situação acadêmica é definida de acordo com as seguintes regras:

```text
Média >= 7        -> Aprovado
Média >= 5 e < 7  -> Recuperação
Média < 5         -> Reprovado
```

Essas decisões pertencem às regras de negócio da aplicação.

O banco de dados possui como principal responsabilidade armazenar as informações resultantes dessas operações.

---

## 7. Operações CRUD

O Sistema Escolar implementa operações CRUD sobre os registros dos alunos.

CRUD representa:

```text
Create
Read
Update
Delete
```

No banco de dados, essas operações correspondem principalmente a:

| CRUD | SQL | Sistema Escolar |
|---|---|---|
| Create | INSERT | Cadastrar aluno |
| Read | SELECT | Consultar alunos |
| Update | UPDATE | Editar aluno |
| Delete | DELETE | Excluir aluno |

---

## 8. CREATE — Cadastro

Quando um novo aluno é cadastrado, a aplicação recebe os dados através da interface.

O backend valida as informações e solicita ao banco a criação do registro.

O fluxo pode ser representado como:

```text
Usuário
   |
   v
Dados do aluno
   |
   v
Backend
   |
   v
Validação
   |
   v
INSERT
   |
   v
MySQL
```

Após a operação ser concluída, os dados passam a permanecer armazenados no banco.

---

## 9. READ — Consulta

As operações de leitura utilizam consultas ao banco para recuperar informações existentes.

No Sistema Escolar existem funcionalidades como:

```text
Listar alunos
Buscar por nome
Buscar por matrícula
```

Essas operações são realizadas principalmente através do comando SQL:

```sql
SELECT
```

O fluxo conceitual é:

```text
Usuário solicita informação
          |
          v
        Backend
          |
          v
        SELECT
          |
          v
         MySQL
          |
          v
       Resultado
          |
          v
        Backend
          |
          v
       Interface
```

---

## 10. UPDATE — Atualização

O sistema também permite modificar informações de alunos existentes.

A aplicação primeiro identifica o aluno e posteriormente realiza a alteração necessária.

No banco de dados, essa operação corresponde ao comando:

```sql
UPDATE
```

Fluxo:

```text
Localizar aluno
      |
      v
Exibir informações
      |
      v
Alterar dados
      |
      v
Validar novos dados
      |
      v
UPDATE
      |
      v
MySQL
```

Essa funcionalidade permite manter os registros atualizados sem a necessidade de excluir e cadastrar novamente o aluno.

---

## 11. DELETE — Exclusão

A aplicação também permite remover registros existentes.

Antes da exclusão, o sistema identifica o aluno através da matrícula.

Após a confirmação da operação, o backend solicita a exclusão ao banco.

No SQL, essa operação utiliza:

```sql
DELETE
```

Fluxo conceitual:

```text
Matrícula
    |
    v
Buscar aluno
    |
    v
Aluno encontrado
    |
    v
Confirmar exclusão
    |
    v
DELETE
    |
    v
MySQL
```

Após a conclusão da operação, o registro deixa de existir no banco de dados.

---

## 12. Camada de acesso aos dados

Uma decisão importante na organização do projeto foi separar as operações relacionadas ao banco de dados das demais responsabilidades da aplicação.

Conceitualmente:

```text
Interface
    |
    v
Flask
    |
    v
Regras de negócio
    |
    v
Repository
    |
    v
MySQL
```

A camada de repositório concentra operações relacionadas ao armazenamento e recuperação das informações.

Entre essas operações estão:

```text
Cadastrar aluno
Listar alunos
Buscar aluno
Atualizar aluno
Excluir aluno
```

Essa separação evita espalhar comandos SQL por diferentes partes da aplicação.

---

## 13. Comunicação Python e MySQL

A aplicação Python precisa de um mecanismo para estabelecer comunicação com o servidor MySQL.

Para isso, o projeto utiliza:

```text
mysql-connector-python
```

Essa dependência também é registrada no arquivo:

```text
requirements.txt
```

A comunicação ocorre conceitualmente da seguinte maneira:

```text
Python
   |
   v
MySQL Connector/Python
   |
   v
Conexão
   |
   v
MySQL
   |
   v
Executa SQL
   |
   v
Retorna resultado
   |
   v
Python
```

Essa integração permite que o backend manipule os dados sem que o usuário precise executar comandos SQL manualmente.

---

## 14. Transações e persistência

Operações que modificam dados precisam ser efetivamente registradas no banco.

Após determinadas operações, como:

```text
INSERT
UPDATE
DELETE
```

a aplicação confirma a alteração para que ela seja persistida no banco.

Esse processo é realizado através do conceito de:

```text
COMMIT
```

De forma simplificada:

```text
Python
   |
   v
Executa alteração
   |
   v
MySQL
   |
   v
COMMIT
   |
   v
Alteração persistida
```

Isso garante que a operação concluída seja efetivamente registrada.

---

## 15. Separação entre banco e regras de negócio

Uma característica importante da arquitetura é que o banco de dados não deve concentrar toda a lógica da aplicação.

Por exemplo, a regra:

```text
Média >= 7 -> Aprovado
```

é uma regra do **Sistema Escolar**.

Ela pertence à lógica da aplicação.

O banco possui principalmente a responsabilidade de armazenar o resultado necessário.

Essa separação pode ser entendida como:

```text
Backend
 |
 +-- valida
 |
 +-- calcula
 |
 +-- decide
 |
 v
Repository
 |
 v
Banco
 |
 `-- armazena
```

Essa organização reduz o acoplamento entre a aplicação e o banco de dados.

---

## 16. Banco local

Atualmente, o banco MySQL é utilizado no ambiente local de desenvolvimento.

Isso significa que a arquitetura atual pode ser representada como:

```text
Computador local
      |
      +----------------------+
      |                      |
      v                      v
Aplicação Flask          MySQL
      |                      ^
      |                      |
      +----------------------+
```

Essa estrutura é adequada para o desenvolvimento e validação inicial do projeto.

Entretanto, ela ainda não representa a arquitetura final planejada.

---

## 17. Segurança das credenciais

Para estabelecer uma conexão com o banco de dados, a aplicação precisa utilizar informações como:

```text
host
usuário
senha
nome do banco
```

Essas informações são consideradas configurações sensíveis da aplicação.

Como evolução do projeto, essas configurações não deverão permanecer diretamente escritas no código-fonte.

A aplicação deverá utilizar mecanismos adequados para separar:

```text
Código
```

de:

```text
Configurações e credenciais
```

Esse ponto será tratado durante a preparação do projeto para implantação.

---

## 18. Evolução para Cloud

Atualmente:

```text
Aplicação local
      |
      v
MySQL local
```

Durante a evolução do projeto para AWS, será avaliada a utilização de um banco de dados gerenciado.

Uma possível evolução arquitetural será:

```text
Internet
    |
    v
Aplicação
    |
    v
AWS
    |
    +---------------------+
    |                     |
    v                     v
Aplicação Python     Banco Gerenciado
    / Flask               MySQL
```

Entre os serviços que serão estudados está o:

```text
Amazon RDS
```

O Amazon RDS permite executar bancos de dados relacionais utilizando um serviço gerenciado pela AWS.

A adoção desse serviço ainda faz parte do **roadmap do projeto** e será realizada somente após a aplicação local estar completamente validada.

---

## 19. Banco de dados e infraestrutura

Durante a futura implantação em nuvem, outros conceitos também passarão a fazer parte da arquitetura do banco.

Entre eles:

- rede privada;
- VPC;
- sub-redes;
- Security Groups;
- controle de acesso;
- variáveis de ambiente;
- backup;
- disponibilidade;
- monitoramento;
- logs.

Esses componentes serão adicionados e documentados progressivamente durante a etapa de infraestrutura.

---

## 20. Estado atual do banco de dados

No momento desta documentação:

### Implementado

- MySQL;
- banco de dados `sistema_escolar`;
- armazenamento persistente;
- dados dos alunos;
- matrícula;
- nome;
- notas;
- situação acadêmica;
- integração entre Python e MySQL;
- MySQL Connector/Python;
- operações INSERT;
- operações SELECT;
- operações UPDATE;
- operações DELETE;
- cadastro de alunos;
- listagem de alunos;
- busca por nome;
- busca por matrícula;
- edição;
- exclusão;
- uso de COMMIT para persistência das alterações.

### Em evolução

- revisão da integração completa com a aplicação Flask;
- revisão do tratamento de erros;
- preparação das configurações para ambientes diferentes;
- separação adequada das credenciais do código.

### Planejado

- banco de dados em ambiente AWS;
- avaliação e implementação do Amazon RDS;
- configuração de rede;
- Security Groups;
- gerenciamento seguro de credenciais;
- backups;
- monitoramento;
- logs;
- automação da infraestrutura.

---

## 21. Evolução planejada

A evolução da camada de dados seguirá aproximadamente o seguinte caminho:

```text
MySQL Local
     |
     v
Integração completa com Flask
     |
     v
Configuração por ambiente
     |
     v
Deploy da aplicação
     |
     v
MySQL na AWS
     |
     v
Amazon RDS
     |
     v
Segurança e rede
     |
     v
Backup e monitoramento
     |
     v
Automação com Infrastructure as Code
```

Essa evolução permitirá utilizar a camada de banco de dados como parte prática dos estudos de desenvolvimento, infraestrutura, Cloud e DevOps.

---

## 22. Próxima etapa

Com a documentação da arquitetura, backend e banco de dados, o projeto passa a possuir uma descrição técnica das principais camadas que compõem a aplicação.

A sequência documentada até este ponto é:

```text
01 - Visão Geral
       |
       v
02 - Arquitetura
       |
       v
03 - Backend
       |
       v
04 - Database
```

O próximo passo será continuar documentando os demais componentes do projeto e, paralelamente, validar a aplicação local antes de iniciar sua implantação na AWS.

A partir dessa base, será possível avançar progressivamente para:

```text
Aplicação
   |
   v
Infraestrutura
   |
   v
Cloud
   |
   v
Automação
   |
   v
CI/CD
   |
   v
Monitoramento
```

O objetivo final é transformar o Sistema Escolar em um projeto completo de portfólio, demonstrando não apenas desenvolvimento de software, mas também **banco de dados, infraestrutura, Cloud, automação e práticas de DevOps**.
