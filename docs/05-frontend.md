# Sistema Escolar — Frontend

## 1. Objetivo deste documento

Este documento descreve o **frontend do Sistema Escolar**, apresentando sua função dentro da aplicação, as tecnologias utilizadas, a organização dos arquivos visuais e a forma como a interface se comunica com o backend.

O frontend representa a camada responsável pela interação entre o usuário e o sistema.

É através dessa camada que o usuário visualiza informações, preenche formulários, realiza ações e recebe os resultados processados pela aplicação.

Assim como os demais componentes do projeto, o frontend foi desenvolvido de forma incremental e continuará evoluindo conforme novas funcionalidades forem adicionadas.

---

## 2. Evolução da interface

O Sistema Escolar não começou como uma aplicação web.

A primeira versão utilizava uma interface **CLI — Command-Line Interface**, executada diretamente pelo terminal.

Nesse estágio, a interação ocorria através de menus textuais.

Exemplo conceitual:

```text
1 - Cadastrar aluno
2 - Listar alunos
3 - Buscar aluno
4 - Editar aluno
5 - Excluir aluno
```

Essa abordagem permitiu desenvolver e validar inicialmente:

* regras de negócio;
* operações CRUD;
* integração com MySQL;
* validações;
* fluxo da aplicação.

Após a estabilização dessas funcionalidades, o projeto evoluiu para uma interface web.

A evolução pode ser representada como:

```text
CLI
 |
 v
Terminal
 |
 v
Python
```

Posteriormente:

```text
Navegador
   |
   v
HTML / CSS
   |
   v
Flask
   |
   v
Backend Python
```

Essa evolução permitiu separar melhor a apresentação da lógica interna da aplicação.

---

## 3. O que é o frontend

O frontend representa a parte da aplicação com a qual o usuário interage diretamente.

No Sistema Escolar, ele é responsável por:

* apresentar informações;
* exibir formulários;
* receber dados digitados;
* permitir navegação entre funcionalidades;
* apresentar resultados;
* exibir mensagens retornadas pela aplicação.

De forma simplificada:

```text
Usuário
   |
   v
Frontend
   |
   v
Backend
   |
   v
Banco de Dados
```

O frontend não deve ser responsável pelas principais regras de negócio.

Sua função principal é realizar a interação com o usuário e encaminhar as ações para o backend.

---

## 4. Tecnologias utilizadas

Atualmente, o frontend do Sistema Escolar utiliza as seguintes tecnologias:

| Tecnologia    | Responsabilidade                                        |
| ------------- | ------------------------------------------------------- |
| HTML          | Estrutura das páginas                                   |
| CSS           | Estilização da interface                                |
| Jinja2        | Inserção dinâmica de informações nas páginas HTML       |
| Flask         | Comunicação entre as páginas e o backend Python         |
| Navegador Web | Interface utilizada pelo usuário para acessar o sistema |

Essas tecnologias trabalham em conjunto para apresentar a aplicação ao usuário.

---

## 5. HTML

O **HTML — HyperText Markup Language** é utilizado para construir a estrutura das páginas.

No projeto, os arquivos HTML são responsáveis por elementos como:

* títulos;
* textos;
* formulários;
* campos de entrada;
* botões;
* tabelas;
* links;
* mensagens.

De forma conceitual:

```text
Página
 |
 +-- Cabeçalho
 |
 +-- Formulário
 |
 +-- Botões
 |
 +-- Tabela
 |
 `-- Mensagens
```

O HTML define **o que existe na página**.

---

## 6. CSS

O **CSS — Cascading Style Sheets** é responsável pela apresentação visual da aplicação.

Enquanto o HTML define a estrutura, o CSS controla aspectos como:

* espaçamento;
* tamanho dos elementos;
* organização visual;
* fontes;
* bordas;
* posicionamento;
* aparência dos formulários;
* aparência dos botões.

A separação pode ser entendida como:

```text
HTML -> Estrutura
CSS  -> Aparência
```

Essa divisão facilita alterações futuras no layout sem modificar diretamente a lógica Python.

---

## 7. Organização dos templates

Os arquivos HTML da aplicação ficam armazenados no diretório:

```text
templates/
```

Entre os templates atualmente utilizados estão:

```text
index.html
editar.html
```

O diretório de templates existe para manter os arquivos de apresentação separados do código Python.

Conceitualmente:

```text
app/
 |
 +-- Código Python
 |
 +-- templates/
 |      |
 |      +-- index.html
 |      |
 |      `-- editar.html
 |
 `-- static/
```

Essa organização segue o padrão utilizado por aplicações Flask.

---

## 8. Template principal

O arquivo:

```text
index.html
```

representa uma das principais páginas da aplicação.

Ele pode ser utilizado para apresentar funcionalidades e informações do Sistema Escolar.

Através dessa página, o usuário interage com o sistema utilizando o navegador.

O fluxo básico é:

```text
Usuário
   |
   v
index.html
   |
   v
Flask
   |
   v
Backend
```

Dependendo da ação executada, o backend poderá consultar ou modificar informações no banco de dados e posteriormente retornar uma nova resposta para a interface.

---

## 9. Tela de edição

O projeto também possui o template:

```text
editar.html
```

Esse arquivo é utilizado no fluxo relacionado à alteração dos dados de um aluno existente.

Conceitualmente:

```text
Usuário seleciona edição
         |
         v
Backend localiza aluno
         |
         v
editar.html
         |
         v
Usuário altera dados
         |
         v
Flask recebe formulário
         |
         v
Backend valida
         |
         v
MySQL atualiza registro
```

Essa separação permite utilizar uma página específica para a operação de edição.

---

## 10. Arquivos estáticos

Os arquivos que não precisam ser processados dinamicamente pelo backend ficam armazenados no diretório:

```text
static/
```

Nesse diretório podem existir arquivos como:

```text
styles.css
```

O CSS utilizado pela aplicação pode ser carregado pelas páginas HTML a partir dessa pasta.

A estrutura conceitual fica:

```text
templates/
   |
   +-- index.html
   `-- editar.html

static/
   |
   `-- styles.css
```

Assim:

```text
templates -> conteúdo das páginas
static    -> recursos visuais
```

---

## 11. Jinja2

O Flask utiliza o mecanismo de templates **Jinja2**.

O Jinja2 permite que informações processadas pelo backend sejam inseridas dinamicamente dentro das páginas HTML.

O fluxo conceitual é:

```text
MySQL
  |
  v
Python
  |
  v
Flask
  |
  v
Jinja2
  |
  v
HTML
  |
  v
Navegador
```

Por exemplo, o backend pode buscar uma lista de alunos no banco de dados e enviar essa informação para o template.

O template então apresenta os registros ao usuário.

Isso permite gerar páginas dinamicamente sem precisar criar manualmente um novo arquivo HTML para cada informação existente no sistema.

---

## 12. Flask e frontend

Embora o Flask faça parte do backend da aplicação, ele possui uma função importante na integração com o frontend.

O Flask é responsável por:

* receber requisições do navegador;
* identificar a rota solicitada;
* processar informações;
* executar funções Python;
* renderizar templates;
* realizar redirecionamentos;
* devolver respostas HTTP.

O fluxo pode ser representado como:

```text
Navegador
    |
    | Requisição HTTP
    v
Flask
    |
    v
Backend Python
    |
    v
Flask
    |
    | Resposta HTTP
    v
Template HTML
    |
    v
Navegador
```

---

## 13. Formulários

Os formulários HTML permitem que o usuário envie dados para a aplicação.

No contexto do Sistema Escolar, podem ser utilizados para operações como:

* cadastro;
* busca;
* edição.

O fluxo geral de um formulário pode ser representado como:

```text
Usuário
   |
   v
Preenche formulário
   |
   v
HTML
   |
   | HTTP
   v
Flask
   |
   v
Backend
   |
   v
Validação
   |
   v
Banco de Dados
```

Depois do processamento, o backend retorna uma resposta ao usuário.

---

## 14. Separação entre frontend e regras de negócio

Uma decisão importante no projeto é evitar concentrar as regras de negócio diretamente nas páginas HTML.

Por exemplo:

```text
Média >= 7 -> Aprovado
```

Essa regra não pertence ao HTML.

Ela pertence ao backend.

O frontend possui principalmente a responsabilidade de:

```text
Receber
Apresentar
Enviar
Exibir
```

Enquanto o backend possui responsabilidades como:

```text
Validar
Calcular
Decidir
Processar
Persistir
```

Conceitualmente:

```text
Frontend
   |
   | dados
   v
Backend
   |
   | processamento
   v
Banco
```

Essa separação torna a aplicação mais organizada e facilita futuras alterações.

---

## 15. Fluxo completo de uma ação

Uma ação realizada pelo usuário através da interface web pode seguir o seguinte caminho:

```text
Usuário
   |
   v
Navegador
   |
   v
HTML
   |
   | Requisição HTTP
   v
Flask
   |
   v
Backend Python
   |
   v
Validação
   |
   v
Regras de negócio
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
Jinja2
   |
   v
HTML
   |
   v
Usuário
```

Esse fluxo demonstra que o frontend representa apenas uma parte da arquitetura completa.

---

## 16. Responsabilidades da interface

No projeto atual, a interface possui responsabilidades como:

### Apresentação

Mostrar as informações de maneira compreensível ao usuário.

### Entrada de dados

Disponibilizar campos para que informações possam ser inseridas.

### Navegação

Permitir que o usuário acesse as funcionalidades existentes.

### Feedback

Exibir resultados das ações realizadas.

### Integração

Enviar as solicitações ao backend através das rotas Flask.

---

## 17. Experiência do usuário

A migração da CLI para uma interface web também representa uma evolução na experiência do usuário.

Na interface CLI, era necessário utilizar diretamente o terminal.

Na interface web, o acesso ocorre através de um navegador.

Antes:

```text
Usuário
   |
   v
Terminal
   |
   v
Menu textual
```

Depois:

```text
Usuário
   |
   v
Navegador
   |
   v
Interface Web
```

Essa mudança torna a aplicação mais acessível para usuários que não possuem conhecimento técnico sobre terminal ou linha de comando.

---

## 18. Responsividade e evolução visual

A interface atual representa uma etapa inicial da aplicação web.

Conforme o projeto evoluir, poderão ser avaliadas melhorias relacionadas a:

* organização visual;
* responsividade;
* navegação;
* padronização de formulários;
* mensagens de sucesso;
* mensagens de erro;
* experiência do usuário.

Essas melhorias deverão ser realizadas sem alterar as responsabilidades principais do backend.

---

## 19. Estado atual do frontend

No momento desta documentação:

### Implementado

* interface web;
* HTML;
* CSS;
* Flask integrado à camada web;
* templates;
* diretório `templates`;
* diretório `static`;
* `index.html`;
* `editar.html`;
* arquivo de estilos;
* formulários;
* integração entre navegador e aplicação Python;
* renderização de páginas através do Flask.

### Em evolução

* revisão completa da experiência do usuário;
* melhorias visuais;
* revisão dos formulários;
* validação do fluxo das páginas;
* padronização das mensagens;
* integração completa com todas as operações do backend.

### Planejado

* melhorias de responsividade;
* melhorias na usabilidade;
* autenticação;
* controle de acesso;
* preparação da interface para ambiente de produção;
* publicação da aplicação na AWS.

---

## 20. Frontend e arquitetura em nuvem

Atualmente, a aplicação web é executada localmente.

O fluxo atual pode ser representado como:

```text
Navegador local
      |
      v
Aplicação Flask
      |
      v
Backend Python
      |
      v
MySQL local
```

Após a implantação na AWS, o objetivo será permitir que o usuário acesse a aplicação através da rede.

Conceitualmente:

```text
Usuário
   |
   v
Internet
   |
   v
Aplicação na AWS
   |
   v
Flask
   |
   v
Backend
   |
   v
Banco de Dados
```

Essa evolução será documentada durante a etapa de deploy.

---

## 21. Evolução planejada

A evolução da camada de frontend seguirá de forma incremental.

```text
CLI
 |
 v
HTML / CSS
 |
 v
Flask + Templates
 |
 v
Integração completa
 |
 v
Melhoria da experiência
 |
 v
Deploy
 |
 v
Aplicação acessível pela rede
```

O foco não será adicionar tecnologias apenas por adicionar.

Cada mudança deverá solucionar uma necessidade real do projeto ou contribuir diretamente para o aprendizado relacionado ao desenvolvimento e à operação da aplicação.

---

## 22. Relação com as demais camadas

O frontend faz parte de uma arquitetura maior.

```text
Frontend
   |
   v
Backend
   |
   v
Database
```

A documentação do projeto passa a possuir a seguinte sequência:

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
       |
       v
05 - Frontend
```

Cada documento possui uma responsabilidade específica.

### Visão Geral

Apresenta o objetivo e o contexto do projeto.

### Arquitetura

Apresenta a visão geral dos componentes.

### Backend

Detalha a lógica e o processamento da aplicação.

### Database

Detalha a persistência e manipulação dos dados.

### Frontend

Detalha a interação entre o usuário e o sistema.

---

## 23. Próxima etapa

Após a documentação do frontend, a próxima etapa será:

```text
06 - Deploy
```

Esse documento será responsável por registrar como a aplicação será preparada para deixar o ambiente exclusivamente local e passar a ser executada em outro ambiente.

A evolução esperada será:

```text
Aplicação local
      |
      v
Preparação para deploy
      |
      v
Servidor Linux
      |
      v
AWS
      |
      v
Automação
      |
      v
CI/CD
```

Essa etapa será especialmente importante para transformar o Sistema Escolar em um projeto de portfólio direcionado também para **Cloud e DevOps**.
