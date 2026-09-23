# Rotina Diária de Operação — Sistema Escolar

## 1. Objetivo

Este documento descreve a rotina operacional do projeto **Sistema Escolar** hospedado na AWS.

O objetivo é validar diariamente o funcionamento das principais camadas da aplicação, desde o servidor EC2 até o banco de dados RDS.

A rotina também tem como objetivo desenvolver uma metodologia de troubleshooting baseada em camadas:

```text
EC2 / Linux
    ↓
systemd
    ↓
Nginx
    ↓
HTTP / HTTPS
    ↓
Gunicorn
    ↓
Flask
    ↓
Rede AWS
    ↓
RDS
    ↓
MySQL
    ↓
Aplicação / CRUD
```

A ideia não é apenas verificar se a aplicação está funcionando, mas entender **qual componente está sendo validado por cada comando**.

---

# 2. Acesso à EC2

Antes de realizar o acesso, verificar no console da AWS o endereço **Public IPv4** atual da instância.

O IP público pode mudar após um processo de `stop/start` da EC2.

No PowerShell do Windows:

```powershell
ssh -i "C:\Users\admin\.ssh\sistema-escolar-key.pem" ec2-user@IP_PUBLICO_EC2
```

Exemplo atual:

```powershell
ssh -i "C:\Users\admin\.ssh\sistema-escolar-key.pem" ec2-user@34.200.245.60
```

Após a conexão:

```text
[ec2-user@ip-10-0-1-102 ~]$
```

Isso indica que o terminal está operando dentro da instância EC2.

### Por que verificar?

O SSH é a principal forma utilizada atualmente para administração da instância.

Fluxo:

```text
Windows
   │
   │ SSH / TCP 22
   ▼
Internet
   │
   ▼
EC2
```

---

# 3. Check-up básico da EC2

Após entrar na instância, verificar o estado básico do sistema operacional.

```bash
whoami
hostname
uptime
df -h
free -h
```

## `whoami`

```bash
whoami
```

Mostra qual usuário está executando os comandos.

Resultado esperado:

```text
ec2-user
```

---

## `hostname`

```bash
hostname
```

Identifica o servidor atual.

Exemplo:

```text
ip-10-0-1-102.ec2.internal
```

O hostname também permite identificar o IP privado utilizado pela EC2 dentro da VPC:

```text
10.0.1.102
```

---

## `uptime`

```bash
uptime
```

Mostra:

- tempo desde a inicialização;
- quantidade de usuários conectados;
- carga média do sistema.

Os três valores de `load average` representam aproximadamente:

```text
1 minuto
5 minutos
15 minutos
```

---

## `df -h`

```bash
df -h
```

Mostra a utilização dos sistemas de arquivos.

No ambiente atual, o volume principal possui aproximadamente:

```text
8 GB
```

O objetivo é observar principalmente a porcentagem de utilização da partição `/`.

---

## `free -h`

```bash
free -h
```

Mostra o consumo de memória RAM.

Observar principalmente:

```text
total
used
available
```

Atualmente a EC2 não possui Swap configurado.

---

# 4. Verificar os serviços

A aplicação depende principalmente de dois serviços:

```text
Nginx
Sistema Escolar / Gunicorn
```

## Nginx

```bash
sudo systemctl status nginx
```

Resultado esperado:

```text
Active: active (running)
```

---

## Sistema Escolar

```bash
sudo systemctl status sistema-escolar
```

Resultado esperado:

```text
Active: active (running)
```

O serviço `sistema-escolar` executa o Gunicorn, responsável por servir a aplicação Flask.

Fluxo:

```text
systemd
   │
   └── sistema-escolar.service
              │
              ▼
           Gunicorn
              │
              ▼
            Flask
```

### Diferença entre `enabled` e `active`

```text
enabled
```

Significa que o serviço está configurado para iniciar automaticamente durante o boot.

```text
active (running)
```

Significa que o serviço está executando naquele momento.

---

# 5. Testar Gunicorn e Flask diretamente

Executar:

```bash
curl -I http://127.0.0.1:8000
```

Resultado esperado:

```text
HTTP/1.1 200 OK
Server: gunicorn
```

Esse teste acessa diretamente o Gunicorn sem passar pelo Nginx.

Fluxo:

```text
EC2
 │
 ▼
127.0.0.1:8000
 │
 ▼
Gunicorn
 │
 ▼
Flask
```

### Por que testar dessa forma?

Esse teste ajuda a separar problemas da aplicação de problemas relacionados ao Nginx.

Se o Gunicorn responder `200 OK`, sabemos que a aplicação Flask está sendo servida internamente.

---

# 6. Testar HTTP, HTTPS e Nginx

O teste completo pode ser realizado com:

```bash
curl -I -L http://sistema-escolar.servebeer.com
```

A opção:

```text
-I
```

solicita apenas os headers HTTP.

A opção:

```text
-L
```

faz o `curl` seguir redirecionamentos.

Resultado esperado:

```text
HTTP/1.1 301 Moved Permanently
Location: https://sistema-escolar.servebeer.com/

HTTP/1.1 200 OK
```

Isso comprova o fluxo:

```text
HTTP :80
   │
   ▼
Nginx
   │
   │ 301 Redirect
   ▼
HTTPS :443
   │
   ▼
Nginx
   │
   │ proxy_pass
   ▼
Gunicorn :8000
   │
   ▼
Flask
   │
   ▼
200 OK
```

---

# 7. Testar HTTPS diretamente

Também é possível testar diretamente o endpoint HTTPS:

```bash
curl -I https://sistema-escolar.servebeer.com
```

Resultado esperado:

```text
HTTP/1.1 200 OK
Server: nginx
```

Isso confirma que o Nginx está recebendo a requisição HTTPS e encaminhando a requisição para a aplicação.

---

# 8. Verificar portas

Executar:

```bash
sudo ss -tulpn
```

Esse comando permite verificar quais portas possuem processos em escuta.

Na arquitetura atual:

```text
80      → HTTP / Nginx
443     → HTTPS / Nginx
8000    → Gunicorn / Flask
3306    → MySQL / RDS
```

O Gunicorn utiliza:

```text
127.0.0.1:8000
```

Isso significa que ele está acessível localmente pela EC2.

O acesso externo deve acontecer através do Nginx.

Arquitetura:

```text
Internet
   │
   │ 80 / 443
   ▼
Nginx
   │
   │ 127.0.0.1:8000
   ▼
Gunicorn
   │
   ▼
Flask
```

---

# 9. Verificar logs da aplicação

Para visualizar as últimas 50 linhas:

```bash
sudo journalctl -u sistema-escolar -n 50
```

Para visualizar eventos registrados no dia:

```bash
sudo journalctl -u sistema-escolar --since today
```

Para acompanhar os logs em tempo real:

```bash
sudo journalctl -u sistema-escolar -f
```

Para interromper:

```text
Ctrl + C
```

### Por que verificar logs?

Os logs fornecem evidências sobre o comportamento da aplicação.

Antes de reiniciar serviços ou alterar configurações, é importante procurar evidências do problema.

---

# 10. Verificar logs do Nginx

## Access Log

```bash
sudo tail -50 /var/log/nginx/access.log
```

Mostra as requisições recebidas pelo Nginx.

---

## Error Log

```bash
sudo tail -50 /var/log/nginx/error.log
```

Mostra erros relacionados ao Nginx e ao encaminhamento das requisições.

---

# 11. Verificar configuração do RDS

As configurações utilizadas pela aplicação estão armazenadas em:

```text
/etc/sistema-escolar.env
```

Por segurança, não exibir o arquivo inteiro, pois ele contém a senha do banco.

Executar:

```bash
sudo grep -E 'DB_HOST|DB_USER|DB_NAME' /etc/sistema-escolar.env
```

Configuração atual:

```text
DB_HOST=sistema-escolar-db.cchc2oaekmxz.us-east-1.rds.amazonaws.com
DB_USER=admin
DB_NAME=sistema_escolar
```

O `DB_HOST` aponta para o endpoint do RDS.

Isso significa que a aplicação não utiliza mais:

```text
localhost
```

ou:

```text
127.0.0.1
```

como servidor de banco de dados.

---

# 12. Testar conectividade EC2 → RDS

Executar:

```bash
nc -zv sistema-escolar-db.cchc2oaekmxz.us-east-1.rds.amazonaws.com 3306
```

Resultado validado:

```text
Ncat: Connected to 10.0.3.45:3306.
```

O endpoint DNS do RDS foi resolvido para um endereço privado:

```text
sistema-escolar-db.cchc2oaekmxz.us-east-1.rds.amazonaws.com
                         │
                         │ DNS
                         ▼
                     10.0.3.45
```

Depois a EC2 conseguiu estabelecer uma conexão TCP com a porta `3306`.

```text
EC2
10.0.1.102
     │
     │ TCP 3306
     ▼
RDS
10.0.3.45
```

### O que esse teste comprova?

```text
Resolução DNS          OK
Conectividade de rede  OK
Porta TCP 3306         OK
EC2 → RDS              OK
```

Esse teste não valida usuário, senha ou consultas SQL.

Ele valida somente a conectividade de rede até a porta do banco.

---

# 13. Acessar o RDS

Para acessar o banco:

```bash
mysql -h sistema-escolar-db.cchc2oaekmxz.us-east-1.rds.amazonaws.com -u admin -p
```

O cliente solicitará:

```text
Enter password:
```

A senha não será exibida enquanto estiver sendo digitada.

Após autenticação bem-sucedida:

```text
mysql>
```

Nesse momento o fluxo é:

```text
Windows
   │
   │ SSH
   ▼
EC2
10.0.1.102
   │
   │ TCP 3306
   ▼
RDS
10.0.3.45
   │
   └── MySQL
```

---

# 14. Validar banco de dados

Listar os bancos:

```sql
SHOW DATABASES;
```

Selecionar o banco do projeto:

```sql
USE sistema_escolar;
```

Listar tabelas:

```sql
SHOW TABLES;
```

Verificar quantidade de alunos:

```sql
SELECT COUNT(*) FROM alunos;
```

Visualizar uma amostra:

```sql
SELECT * FROM alunos LIMIT 10;
```

Esses testes validam diferentes camadas:

```text
nc -zv
   │
   └── Rede / TCP
          ↓
mysql -h
   │
   └── Autenticação
          ↓
USE sistema_escolar
   │
   └── Banco
          ↓
SELECT
   │
   └── Dados
```

---

# 15. Teste funcional da aplicação

Abrir no navegador:

```text
https://sistema-escolar.servebeer.com
```

Realizar uma operação CRUD para validar a integração completa.

```text
CREATE  → cadastrar aluno
READ    → consultar/listar aluno
UPDATE  → editar aluno
DELETE  → excluir aluno
```

Não é necessário realizar todas as operações diariamente.

Uma operação pode ser utilizada como teste funcional.

Fluxo completo:

```text
Navegador
    │
    │ HTTPS :443
    ▼
Nginx
    │
    │ proxy_pass
    ▼
Gunicorn
    │
    ▼
Flask
    │
    │ TCP 3306
    ▼
RDS
    │
    ▼
MySQL
```

---

# 16. Conferir logs após o teste

Após realizar uma operação pela aplicação:

```bash
sudo journalctl -u sistema-escolar -n 50
```

Também podem ser verificados:

```bash
sudo tail -50 /var/log/nginx/access.log
```

e:

```bash
sudo tail -50 /var/log/nginx/error.log
```

Isso permite correlacionar uma ação realizada no navegador com os eventos registrados pelo servidor.

---

# 17. Encerramento

Para sair do MySQL:

```sql
exit;
```

Para sair da EC2:

```bash
exit
```

Após finalizar os testes, verificar se os recursos AWS precisam continuar executando.

Caso não sejam necessários, os recursos podem ser interrompidos conforme a estratégia de custos definida para o laboratório.

---

# 18. Checklist rápido

```text
[ ] Conferir estado da EC2 e RDS
[ ] Conferir Public IPv4 da EC2
[ ] Acessar EC2 via SSH

[ ] whoami
[ ] hostname
[ ] uptime
[ ] df -h
[ ] free -h

[ ] sudo systemctl status nginx
[ ] sudo systemctl status sistema-escolar

[ ] curl -I http://127.0.0.1:8000

[ ] curl -I -L http://sistema-escolar.servebeer.com

[ ] sudo ss -tulpn

[ ] sudo journalctl -u sistema-escolar -n 50

[ ] sudo tail -50 /var/log/nginx/access.log
[ ] sudo tail -50 /var/log/nginx/error.log

[ ] sudo grep -E 'DB_HOST|DB_USER|DB_NAME' /etc/sistema-escolar.env

[ ] nc -zv sistema-escolar-db.cchc2oaekmxz.us-east-1.rds.amazonaws.com 3306

[ ] mysql -h sistema-escolar-db.cchc2oaekmxz.us-east-1.rds.amazonaws.com -u admin -p

[ ] SHOW DATABASES;
[ ] USE sistema_escolar;
[ ] SHOW TABLES;
[ ] SELECT COUNT(*) FROM alunos;
[ ] SELECT * FROM alunos LIMIT 10;

[ ] Abrir aplicação no navegador
[ ] Realizar operação CRUD
[ ] Conferir logs após o teste

[ ] exit;  → sair do MySQL
[ ] exit   → sair da EC2
```

---

# 19. Resumo da arquitetura validada

```text
                         INTERNET
                             │
                    HTTP 80 / HTTPS 443
                             │
                             ▼
┌─────────────────────────────────────────────────┐
│                  VPC 10.0.0.0/16                │
│                                                 │
│   Subnet Pública                                │
│                                                 │
│   ┌───────────────────────────────┐             │
│   │ EC2                           │             │
│   │ 10.0.1.102                    │             │
│   │                               │             │
│   │ Nginx :80/:443                │             │
│   │       ↓                       │             │
│   │ Gunicorn 127.0.0.1:8000      │             │
│   │       ↓                       │             │
│   │ Flask                         │             │
│   └──────────────┬────────────────┘             │
│                  │                              │
│                  │ TCP 3306                     │
│                  ▼                              │
│   Camada privada                                │
│                                                 │
│   ┌───────────────────────────────┐             │
│   │ RDS                           │             │
│   │ 10.0.3.45                     │             │
│   │ MySQL :3306                   │             │
│   │                               │             │
│   │ Database: sistema_escolar     │             │
│   └───────────────────────────────┘             │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

# 20. Princípio de troubleshooting

A rotina deve ser executada por camadas.

Em caso de problema, evitar alterar várias configurações ao mesmo tempo.

Seguir a sequência:

```text
Servidor está saudável?
        ↓
Serviços estão ativos?
        ↓
Gunicorn responde?
        ↓
Nginx responde?
        ↓
HTTPS funciona?
        ↓
EC2 alcança o RDS?
        ↓
Banco aceita autenticação?
        ↓
SQL funciona?
        ↓
CRUD funciona?
        ↓
O que dizem os logs?
```

Dessa forma, cada teste elimina possíveis causas e ajuda a localizar exatamente em qual camada está o problema.