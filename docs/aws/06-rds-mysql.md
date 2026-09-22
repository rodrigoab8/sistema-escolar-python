# Infraestrutura AWS — Amazon RDS e Camada Privada de Banco de Dados

## 1. Objetivo

Este documento descreve a evolução da infraestrutura AWS do projeto
**Sistema Escolar**, responsável pela separação entre a camada de aplicação
e a camada de banco de dados.

Na arquitetura inicial, a aplicação Flask e o banco MariaDB estavam
hospedados na mesma instância EC2.

A arquitetura inicial funcionava da seguinte maneira:

Internet
   |
   v
EC2
   |
   |-- Nginx
   |-- Gunicorn
   |-- Flask
   |
   `-- MariaDB local

Nesta etapa, o banco de dados foi migrado para o **Amazon RDS for MySQL**.

Também foram criadas sub-redes privadas, uma tabela de rotas privada,
um DB Subnet Group e um Security Group específico para o banco.

A arquitetura continua utilizando a região:

- **Região AWS:** US East (N. Virginia)
- **Código da região:** `us-east-1`

O principal objetivo desta evolução foi separar a camada de aplicação da
camada de dados, mantendo o banco de dados sem exposição direta à internet.

---

# 2. Evolução da arquitetura

## Arquitetura anterior

Inicialmente, a instância EC2 era responsável tanto pela aplicação quanto
pelo banco de dados.

EC2
   |
   |-- Nginx
   |-- Gunicorn
   |-- Flask
   |
   `-- MariaDB
       |
       `-- sistema_escolar

Essa arquitetura foi importante para validar o funcionamento inicial do
projeto.

Porém, aplicação e banco estavam executando no mesmo servidor.

## Arquitetura atual

Após esta evolução, as responsabilidades foram separadas.

EC2
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

Agora a EC2 permanece responsável pela camada de aplicação, enquanto o
Amazon RDS é responsável pela camada de banco de dados.

---

# 3. Sub-redes privadas

## O que são?

As subnets privadas são divisões da VPC destinadas a recursos que não
precisam possuir acesso direto pela internet.

Nesta etapa foram criadas duas novas subnets:

- **Subnet privada 1A:** `10.0.2.0/24`
- **Availability Zone:** `us-east-1a`

- **Subnet privada 1B:** `10.0.3.0/24`
- **Availability Zone:** `us-east-1b`

As duas pertencem à VPC:

`10.0.0.0/16`

A subnet pública existente continua sendo:

`10.0.1.0/24`

## Por que foram criadas?

O banco de dados não precisa receber conexões diretamente da internet.

Quem precisa acessar o banco é a aplicação executada na EC2.

Por isso, o RDS foi colocado na camada privada da arquitetura.

A divisão lógica passou a ser:

VPC — 10.0.0.0/16
   |
   |-- Subnet pública
   |   `-- 10.0.1.0/24
   |       `-- EC2
   |
   |-- Subnet privada
   |   `-- 10.0.2.0/24
   |
   `-- Subnet privada
       `-- 10.0.3.0/24

Essa separação permite manter recursos públicos e privados dentro da mesma
VPC, com funções diferentes.

---

# 4. Route Table privada

## O que é?

Assim como a subnet pública utiliza uma tabela de rotas, as subnets privadas
também precisam de uma Route Table para determinar como o tráfego será
encaminhado.

Foi criada uma tabela específica:

- **Nome:** `sistema-escolar-private-rt`

Ela foi associada às duas subnets privadas.

## Rota utilizada

A tabela possui a rota:

`10.0.0.0/16 → local`

Não foi adicionada a rota:

`0.0.0.0/0 → Internet Gateway`

## Por que?

A rota `local` permite a comunicação entre recursos pertencentes ao espaço
de endereçamento da própria VPC.

A EC2 e o RDS pertencem à mesma VPC.

Portanto, a comunicação entre eles não precisa passar pela internet.

O fluxo ocorre internamente:

EC2
   |
   | rede privada da VPC
   v
RDS

As subnets privadas também não foram associadas diretamente ao
Internet Gateway.

---

# 5. Por que não foi utilizado NAT Gateway?

Um NAT Gateway pode ser utilizado quando recursos em subnets privadas
precisam iniciar conexões com a internet sem receber conexões diretamente
dela.

Neste laboratório, o RDS não precisa acessar a internet para atender à
aplicação.

A comunicação necessária é:

EC2 → RDS

Como os dois recursos estão dentro da mesma VPC, a rota `local` é suficiente.

Por esse motivo, não foi criado um NAT Gateway.

Essa decisão também mantém a arquitetura mais simples e evita adicionar
um recurso desnecessário ao laboratório.

---

# 6. DB Subnet Group

## O que é?

O DB Subnet Group informa ao Amazon RDS quais subnets podem ser utilizadas
para posicionar o banco de dados dentro da VPC.

Foi criado:

- **Nome:** `sistema-escolar-db-subnet-group`

O grupo contém:

- `sistema-escolar-private-subnet-1a`
- `sistema-escolar-private-subnet-1b`

As subnets pertencem a Availability Zones diferentes:

- `us-east-1a`
- `us-east-1b`

## Por que duas subnets?

O DB Subnet Group foi construído utilizando subnets em Availability Zones
diferentes.

Nesta etapa, a instância RDS utiliza uma configuração **Single-AZ**.

Portanto, isso não significa que existem duas instâncias do banco.

O DB Subnet Group define as redes disponíveis para o serviço, enquanto a
instância criada nesta arquitetura continua sendo Single-AZ.

Essa organização também prepara a camada de rede para possíveis evoluções
futuras de disponibilidade.

---

# 7. Security Group do banco de dados

## O que é?

O Security Group funciona como um firewall virtual aplicado aos recursos
da AWS.

A EC2 já utiliza o Security Group:

`sistema-escolar-sg`

Para o banco foi criado um Security Group separado:

`sistema-escolar-db-sg`

## Regra de entrada

Foi configurada:

- **Tipo:** MySQL/Aurora
- **Protocolo:** TCP
- **Porta:** `3306`
- **Origem:** `sistema-escolar-sg`

## Por que utilizar o Security Group da EC2 como origem?

A porta `3306` não foi liberada para:

`0.0.0.0/0`

Também não foi necessário utilizar o IP público da EC2 como origem.

A regra estabelece a relação:

sistema-escolar-sg
        |
        | TCP 3306
        v
sistema-escolar-db-sg

Dessa forma, o Security Group do banco permite conexões provenientes dos
recursos autorizados pelo Security Group da aplicação.

Isso cria uma separação clara:

Internet
   |
   | HTTP / HTTPS
   v
EC2
   |
   | MySQL — TCP 3306
   v
RDS

A internet não possui uma regra direta para acessar a porta `3306` do banco.

---

# 8. Amazon RDS

## O que é?

O Amazon RDS — Relational Database Service — é um serviço gerenciado da AWS
para bancos de dados relacionais.

Nesta arquitetura ele passou a hospedar o banco utilizado pelo
Sistema Escolar.

## Configuração utilizada

- **Identificador:** `sistema-escolar-db`
- **Engine:** MySQL
- **Versão utilizada:** MySQL 8.4
- **Classe:** `db.t3.micro`
- **Armazenamento:** 20 GiB
- **Tipo de armazenamento:** General Purpose SSD
- **Disponibilidade:** Single-AZ
- **Porta:** `3306`
- **Public Access:** No
- **Database inicial:** `sistema_escolar`
- **DB Subnet Group:** `sistema-escolar-db-subnet-group`
- **Security Group:** `sistema-escolar-db-sg`

## Por que Public Access = No?

O banco não precisa ser acessado diretamente pela internet.

A aplicação está dentro da mesma VPC e pode acessar o RDS utilizando sua
conectividade privada.

Por isso, não existe necessidade de tornar o banco publicamente acessível.

Essa decisão reduz a superfície de exposição da camada de dados.

---

# 9. Comunicação EC2 → RDS

Após a criação do RDS, a comunicação foi testada diretamente a partir da EC2.

O endpoint do RDS foi utilizado como host do banco.

O teste foi realizado pela porta:

`3306`

A conexão foi estabelecida com sucesso.

Durante a autenticação, foi possível observar que a conexão chegava ao banco
a partir do endereço privado da EC2:

`10.0.1.102`

Isso demonstrou que a comunicação estava ocorrendo internamente pela VPC.

O fluxo validado foi:

EC2 — 10.0.1.102
   |
   | TCP 3306
   |
   | rota local da VPC
   v
RDS MySQL

Esse teste validou em conjunto:

- resolução DNS do endpoint;
- conectividade entre as subnets;
- rota local da VPC;
- Security Groups;
- porta TCP 3306;
- autenticação no MySQL.

---

# 10. Banco de dados de origem

Antes da migração, o banco estava hospedado localmente na EC2 utilizando:

- **SGBD:** MariaDB 10.11
- **Banco:** `sistema_escolar`

Foi realizado um inventário antes de qualquer alteração.

A tabela existente era:

`alunos`

Ela possuía inicialmente:

`61 registros`

Sua estrutura era:

- `id`
- `nome`
- `nota1`
- `nota2`
- `media`
- `status_aluno`
- `matricula`

Também existia a trigger:

`trg_atualizar_media_status`

Essa trigger é executada antes de atualizações na tabela `alunos` e possui
a responsabilidade de recalcular:

- média;
- status do aluno.

Realizar esse inventário antes da migração permitiu criar uma referência
para comparar a origem com o destino posteriormente.

---

# 11. Backup antes da migração

Antes de migrar os dados foi criado um dump do MariaDB local.

Arquivo:

`sistema_escolar_backup.sql`

Esse arquivo foi preservado sem modificações.

Em seguida foi criada uma cópia:

`sistema_escolar_rds.sql`

## Por que manter o arquivo original?

Durante uma migração entre SGBDs diferentes podem ser necessários ajustes
de compatibilidade.

Por isso, o backup original foi mantido intacto.

As alterações foram realizadas somente na cópia destinada ao RDS.

O processo ficou:

MariaDB
   |
   | dump
   v
sistema_escolar_backup.sql
   |
   | cópia
   v
sistema_escolar_rds.sql
   |
   | ajustes de compatibilidade
   v
RDS MySQL

Essa estratégia mantém uma opção de rollback e evita modificar diretamente
o backup original.

---

# 12. Compatibilidade MariaDB → MySQL

Durante a migração foram identificadas diferenças entre o dump gerado pelo
MariaDB 10.11 e o MySQL 8.4 utilizado no RDS.

## DEFINER da trigger

A trigger original possuía:

`DEFINER=sistema_app@localhost`

Esse contexto pertencia ao banco local.

Na cópia destinada ao RDS, o `DEFINER` foi removido antes da importação.

A trigger foi preservada.

Após a importação, ela passou a existir no RDS utilizando o contexto do
usuário responsável pela criação.

## NO_AUTO_CREATE_USER

Durante a primeira tentativa de importação ocorreu o erro:

`Variable 'sql_mode' can't be set to the value of 'NO_AUTO_CREATE_USER'`

O dump do MariaDB continha a opção:

`NO_AUTO_CREATE_USER`

Essa configuração não era aceita pelo MySQL 8.4 utilizado no RDS.

A opção foi removida somente do arquivo:

`sistema_escolar_rds.sql`

Após o ajuste, a importação foi executada novamente com sucesso.

## Por que documentar esses erros?

Os erros encontrados fazem parte do processo real de migração.

Registrar o troubleshooting permite entender que uma migração entre MariaDB
e MySQL pode exigir adaptações, mesmo quando os dois sistemas possuem grande
compatibilidade entre si.

---

# 13. Validação da migração

Após a importação foram realizadas verificações diretamente no RDS.

## Tabela

A tabela:

`alunos`

foi criada corretamente.

## Quantidade de registros

Antes da migração:

`61 registros`

Após a migração:

`61 registros`

## Trigger

A trigger:

`trg_atualizar_media_status`

também foi criada corretamente.

Com isso foram validados:

- estrutura da tabela;
- dados;
- quantidade de registros;
- trigger.

A migração do banco foi considerada concluída somente depois dessas
verificações.

---

# 14. Configuração da aplicação

A aplicação utiliza variáveis de ambiente armazenadas no servidor.

Arquivo:

`/etc/sistema-escolar.env`

As variáveis utilizadas são:

- `DB_HOST`
- `DB_USER`
- `DB_PASSWORD`
- `DB_NAME`

Antes da alteração foi criada uma cópia de segurança:

`/etc/sistema-escolar.env.backup`

O `DB_HOST`, que anteriormente apontava para o banco local, passou a utilizar
o endpoint do Amazon RDS.

Também foram configuradas as credenciais necessárias para conexão com o
novo banco.

## Por que utilizar variáveis de ambiente?

As credenciais do banco não devem ficar gravadas diretamente no
código-fonte.

Também não devem ser enviadas ao GitHub.

A aplicação lê as informações necessárias através das variáveis de ambiente
fornecidas pelo servidor.

Isso mantém a configuração do ambiente separada do código da aplicação.

---

# 15. Gunicorn e systemd

Após alterar as variáveis de ambiente, o serviço da aplicação foi reiniciado.

O serviço:

`sistema-escolar.service`

continuou com o estado:

`active (running)`

Inicialmente o arquivo possuía:

`After=network.target mariadb.service`

Essa configuração fazia sentido enquanto o banco MariaDB estava executando
localmente na EC2.

Depois da migração para o RDS, essa dependência deixou de ser necessária.

A configuração passou a utilizar:

`After=network.target`

Em seguida foram executados:

- reload das configurações do systemd;
- restart do serviço;
- validação do status do Gunicorn.

O serviço permaneceu ativo normalmente.

---

# 16. Validação ponta a ponta

Após a migração, não foi considerado suficiente apenas verificar se o
Gunicorn estava ativo.

Também foi realizado um teste funcional da aplicação.

O fluxo completo testado foi:

Navegador
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
   | TCP 3306
   v
Amazon RDS MySQL
   |
   v
sistema_escolar

A aplicação abriu normalmente no navegador e continuou aceitando operações.

Um aluno foi excluído através da interface web.

Em seguida, o banco no RDS foi consultado diretamente.

O registro excluído não estava mais presente no RDS.

A quantidade de registros também foi reduzida.

Isso comprovou que a operação realizada pelo navegador chegou até o banco
hospedado no Amazon RDS.

---

# 17. Desacoplamento do MariaDB local

Após validar o funcionamento da aplicação com o RDS, o serviço MariaDB
instalado na EC2 foi parado.

Mesmo com o MariaDB local parado, o Sistema Escolar continuou:

- carregando no navegador;
- listando os alunos;
- realizando consultas;
- aceitando alterações;
- realizando exclusões.

Isso confirmou que a aplicação não dependia mais do banco local.

O MariaDB não foi removido imediatamente.

## Por que não desinstalar imediatamente?

Manter temporariamente o banco antigo permite possuir uma opção adicional
de rollback durante a fase inicial após a migração.

Depois que o novo ambiente estiver suficientemente validado, o MariaDB
local poderá ser removido em uma etapa de limpeza.

---

# 18. Arquitetura final

A arquitetura após esta etapa pode ser representada da seguinte maneira:

Internet
   |
   v
Internet Gateway
   |
   v
VPC — 10.0.0.0/16
   |
   |-- Subnet pública — 10.0.1.0/24
   |       |
   |       v
   |      EC2
   |       |
   |       |-- Nginx
   |       |-- Gunicorn
   |       `-- Flask
   |              |
   |              | TCP 3306
   |              v
   |
   |-- Subnet privada — 10.0.2.0/24 — us-east-1a
   |       |
   |       |
   |       `-- DB Subnet Group
   |                    |
   |                    v
   |                 Amazon RDS
   |                 MySQL 8.4
   |                    |
   |                    `-- sistema_escolar
   |
   `-- Subnet privada — 10.0.3.0/24 — us-east-1b
           |
           `-- DB Subnet Group

O RDS não possui acesso público.

A comunicação da aplicação com o banco ocorre pela rede interna da VPC.

---

# 19. Decisões de arquitetura

Nesta evolução foram tomadas decisões visando segurança, organização,
aprendizado e controle de custos.

### Banco separado da aplicação

O banco deixou de executar dentro da mesma EC2 utilizada pela aplicação.

**Motivo:** separar as responsabilidades das camadas da arquitetura.

### RDS em subnets privadas

O banco foi posicionado na camada privada.

**Motivo:** o banco não precisa receber conexões diretamente da internet.

### Duas subnets privadas

Foram utilizadas subnets em duas Availability Zones.

**Motivo:** atender à organização necessária para o DB Subnet Group e
preparar a rede para futuras evoluções.

### RDS Single-AZ

Foi utilizada uma instância Single-AZ nesta etapa.

**Motivo:** manter a arquitetura adequada ao laboratório atual, sem adicionar
complexidade desnecessária.

### Security Group dedicado

Foi criado um Security Group exclusivo para o banco.

**Motivo:** separar as regras de segurança da aplicação das regras da camada
de dados.

### Security Group como origem

A porta `3306` aceita conexões provenientes do Security Group da EC2.

**Motivo:** evitar exposição pública do MySQL e criar uma relação direta
entre a camada de aplicação e a camada de banco.

### Sem acesso público ao RDS

Foi configurado:

`Public Access: No`

**Motivo:** todo o acesso necessário ocorre internamente pela VPC.

### Sem NAT Gateway

Não foi criado NAT Gateway.

**Motivo:** o RDS não precisa acessar a internet para atender à aplicação,
e EC2 e RDS conseguem se comunicar através da rota local da VPC.

### Credenciais fora do código

As credenciais são fornecidas através de variáveis de ambiente.

**Motivo:** evitar armazenar informações sensíveis no código ou no
repositório Git.

### Backup antes da migração

O banco original foi exportado antes de qualquer alteração.

**Motivo:** permitir recuperação e rollback caso a migração apresentasse
problemas.

---

# 20. Resultado da etapa

Ao final desta etapa, a infraestrutura do Sistema Escolar possui:

- VPC própria;
- subnet pública para a EC2;
- duas subnets privadas para a camada de banco;
- Route Table privada;
- rota local entre os recursos da VPC;
- DB Subnet Group;
- Security Group exclusivo para o RDS;
- acesso MySQL restrito à camada de aplicação;
- Amazon RDS utilizando MySQL;
- banco sem acesso público;
- banco `sistema_escolar` migrado;
- tabela `alunos` migrada;
- trigger migrada;
- aplicação utilizando o endpoint do RDS;
- credenciais fora do código;
- MariaDB local desacoplado da aplicação;
- validação funcional realizada ponta a ponta.

A arquitetura evoluiu de:

EC2
   |
   |-- Aplicação
   `-- Banco

para:

EC2
   |
   `-- Aplicação
          |
          | rede privada da VPC
          v
      Amazon RDS
          |
          `-- Banco

Essa evolução separa a camada de aplicação da camada de dados e cria uma
base mais organizada para as próximas etapas do projeto.

Possíveis evoluções futuras incluem:

- Infrastructure as Code com Terraform;
- maior automação de deploy;
- alta disponibilidade;
- monitoramento;
- gerenciamento de segredos;
- revisão da arquitetura de exposição da camada web;
- estratégias adicionais de backup e recuperação.