# 05 - DNS, HTTPS e DDNS

## 1. Objetivo

Esta etapa teve como objetivo disponibilizar o Sistema Escolar por meio de um endereço DNS estável e HTTPS, mesmo utilizando uma instância EC2 com endereço IPv4 público dinâmico.

Ao final da configuração, a aplicação passou a ser acessada através de:

```text
https://sistema-escolar.servebeer.com
```

Além disso, foi configurada uma atualização automática de DNS para que uma alteração do endereço IPv4 público da EC2 após um ciclo de Stop/Start não exija atualização manual.

A solução final utiliza:

- Amazon EC2
- No-IP
- No-IP Dynamic Update Client (DUC)
- systemd
- Nginx
- Let's Encrypt
- Certbot
- Gunicorn
- Flask
- MariaDB

---

## 2. Problema: endereço IPv4 público dinâmico

A instância EC2 utilizada no projeto possui um endereço IPv4 público atribuído automaticamente pela AWS.

Esse endereço não é permanente.

Quando uma instância EC2 é interrompida e posteriormente iniciada novamente, um novo endereço IPv4 público pode ser atribuído.

Exemplo observado durante o laboratório:

```text
IP anterior:
98.86.164.187

Stop → Start

Novo IP:
100.58.168.128
```

Isso cria um problema para uma aplicação publicada na Internet.

Se os usuários acessassem diretamente:

```text
http://98.86.164.187
```

o endereço deixaria de funcionar após a mudança do IP.

Também não seria adequado alterar manualmente o DNS toda vez que a EC2 fosse reiniciada.

Era necessário criar uma camada de abstração:

```text
Usuário
   ↓
Nome DNS
   ↓
IP público atual da EC2
```

Assim, o usuário utiliza sempre o mesmo nome, independentemente do endereço IP atribuído à instância.

---

## 3. Por que não utilizar Elastic IP

Uma possível solução seria associar um Elastic IP à instância EC2.

O Elastic IP forneceria um endereço público estático.

A arquitetura seria:

```text
Internet
   ↓
Elastic IP
   ↓
EC2
```

Entretanto, para este projeto de laboratório foi escolhida uma solução que evitasse custos adicionais e permitisse estudar também o funcionamento de DNS dinâmico.

Por esse motivo foi adotado:

```text
No-IP + DDNS
```

Essa decisão também permitiu praticar conceitos importantes de:

- DNS;
- resolução de nomes;
- endereço IP público;
- automação;
- serviços Linux;
- systemd;
- troubleshooting;
- HTTPS;
- gerenciamento de certificados.

---

## 4. Escolha do No-IP

Foi utilizado o No-IP como provedor de Dynamic DNS (DDNS).

Foi criado o hostname:

```text
sistema-escolar.servebeer.com
```

Inicialmente, esse hostname foi configurado para apontar para o endereço IPv4 público da EC2.

A função do DNS é permitir:

```text
sistema-escolar.servebeer.com
        ↓
resolução DNS
        ↓
IP público da EC2
```

Dessa forma, o usuário não precisa conhecer o endereço IP da instância.

---

## 5. DNS não é o mesmo que DDNS

É importante separar os dois conceitos.

### DNS

O DNS realiza a resolução:

```text
nome
 ↓
IP
```

Exemplo:

```text
sistema-escolar.servebeer.com
        ↓
100.58.168.128
```

### DDNS

O Dynamic DNS adiciona automação a esse processo.

Quando o IP público muda:

```text
EC2 recebe novo IP
       ↓
DDNS detecta
       ↓
registro DNS é atualizado
```

Portanto:

```text
DNS  = resolve nome para IP
DDNS = mantém esse IP atualizado automaticamente
```

---

## 6. Configuração inicial do Nginx

A aplicação Flask não é exposta diretamente à Internet.

O Gunicorn executa a aplicação internamente:

```text
127.0.0.1:8000
```

O Nginx funciona como reverse proxy.

Fluxo:

```text
Internet
   ↓
Nginx
   ↓
Gunicorn
   ↓
Flask
```

O arquivo de configuração utilizado é:

```text
/etc/nginx/conf.d/sistema-escolar.conf
```

Inicialmente o bloco utilizava:

```nginx
server_name _;
```

Após a criação do hostname, foi necessário configurar:

```nginx
server_name sistema-escolar.servebeer.com;
```

Essa alteração foi importante para que o Nginx pudesse identificar corretamente qual hostname pertence à aplicação e para que o Certbot pudesse localizar o server block correspondente.

A configuração foi validada com:

```bash
sudo nginx -t
```

Após a validação:

```bash
sudo systemctl reload nginx
```

---

## 7. HTTPS com Let's Encrypt

Depois que o DNS passou a apontar para a EC2, foi configurado HTTPS.

Foi utilizado:

```text
Let's Encrypt
+
Certbot
```

O Let's Encrypt funciona como Autoridade Certificadora (CA) e emite certificados TLS.

O Certbot automatiza o processo de:

- solicitação;
- validação;
- instalação;
- renovação do certificado.

No Amazon Linux, foram instalados:

```bash
sudo dnf install certbot python3-certbot-nginx -y
```

A versão foi verificada com:

```bash
certbot --version
```

---

## 8. Validação antes da emissão do certificado

Antes da emissão definitiva foi utilizado o modo de teste:

```bash
sudo certbot certonly --nginx --dry-run -d sistema-escolar.servebeer.com
```

O dry-run permite validar o processo sem solicitar imediatamente um certificado de produção.

Após a validação bem-sucedida, foi executado:

```bash
sudo certbot --nginx -d sistema-escolar.servebeer.com
```

O certificado foi emitido com sucesso.

Os arquivos foram armazenados em:

```text
/etc/letsencrypt/live/sistema-escolar.servebeer.com/
```

Principais arquivos:

```text
fullchain.pem
privkey.pem
```

---

## 9. Instalação do certificado no Nginx

Inicialmente o Certbot não conseguiu instalar automaticamente o certificado porque o Nginx ainda utilizava:

```nginx
server_name _;
```

Após alterar para:

```nginx
server_name sistema-escolar.servebeer.com;
```

foi possível executar:

```bash
sudo certbot install --cert-name sistema-escolar.servebeer.com
```

O certificado foi então associado corretamente ao Nginx.

---

## 10. Redirecionamento HTTP para HTTPS

Após a configuração do certificado, foi validado que acessos HTTP eram redirecionados para HTTPS.

Teste:

```bash
curl -I http://sistema-escolar.servebeer.com
```

Resultado esperado:

```text
HTTP/1.1 301 Moved Permanently
Location: https://sistema-escolar.servebeer.com/
```

Teste HTTPS:

```bash
curl -I https://sistema-escolar.servebeer.com
```

Resultado:

```text
HTTP/1.1 200 OK
```

O fluxo passou a ser:

```text
HTTP :80
   ↓
301 Redirect
   ↓
HTTPS :443
   ↓
Nginx
   ↓
Gunicorn
   ↓
Flask
```

---

## 11. Security Group

Para permitir acesso à aplicação foram utilizadas regras para:

```text
TCP 80  - HTTP
TCP 443 - HTTPS
```

O SSH permanece restrito para administração.

A porta utilizada internamente pelo Gunicorn:

```text
8000
```

não foi exposta publicamente.

Da mesma forma, a porta do banco MariaDB/MySQL:

```text
3306
```

não foi aberta para a Internet.

Isso mantém o fluxo:

```text
Internet
   ↓
Security Group
   ↓
80 / 443
   ↓
Nginx
   ↓
127.0.0.1:8000
   ↓
Gunicorn
```

---

## 12. O problema após Stop/Start

Mesmo com DNS e HTTPS configurados, ainda existia um problema.

Após interromper e iniciar a EC2:

```text
Stop
 ↓
Start
 ↓
novo IP público
```

o registro DNS poderia continuar apontando para o endereço anterior.

Isso quebraria:

```text
sistema-escolar.servebeer.com
```

Foi então necessário implementar Dynamic DNS.

---

## 13. No-IP Dynamic Update Client

Foi utilizado o cliente oficial do No-IP:

```text
No-IP DUC
```

Versão utilizada:

```text
3.3.0
```

Como o pacote não estava disponível diretamente no repositório utilizado pelo Amazon Linux, o cliente foi obtido e instalado manualmente.

Download:

```bash
wget --content-disposition https://www.noip.com/download/linux/latest
```

Após extrair o pacote, foi utilizado o binário compatível com a arquitetura:

```text
x86_64
```

A arquitetura da EC2 foi verificada com:

```bash
uname -m
```

O executável foi instalado em:

```text
/usr/local/bin/noip-duc
```

Validação:

```bash
noip-duc --version
```

Resultado:

```text
noip-duc 3.3.0
```

---

## 14. Credenciais DDNS

Foi criada uma DDNS Key no painel do No-IP.

As credenciais da DDNS Key não foram armazenadas no código-fonte nem no GitHub.

Foi criado:

```text
/etc/noip-duc.env
```

Esse arquivo contém as variáveis necessárias para o cliente.

Exemplo sem credenciais reais:

```text
NOIP_USERNAME=<DDNS_KEY_USERNAME>
NOIP_PASSWORD=<DDNS_KEY_PASSWORD>
NOIP_HOSTNAMES=all.ddnskey.com
NOIP_IP_METHOD=dns,http,http-port-8245
NOIP_CHECK_INTERVAL=5m
```

O hostname:

```text
all.ddnskey.com
```

é utilizado pelo mecanismo de DDNS Key do No-IP.

Ele não é o endereço público da aplicação.

O endereço público continua sendo:

```text
sistema-escolar.servebeer.com
```

---

## 15. Proteção das credenciais

O arquivo foi configurado como propriedade do root:

```bash
sudo chown root:root /etc/noip-duc.env
```

E recebeu permissão:

```bash
sudo chmod 600 /etc/noip-duc.env
```

Validação:

```bash
sudo ls -l /etc/noip-duc.env
```

Resultado:

```text
-rw------- root root
```

A permissão `600` significa:

```text
root → leitura e escrita
outros usuários → nenhum acesso
```

Essa decisão evita armazenar credenciais diretamente:

- no código;
- no repositório Git;
- no GitHub;
- no arquivo do serviço.

---

## 16. Automação com systemd

Para que o No-IP DUC fosse iniciado automaticamente junto com a EC2, foi criado um serviço systemd.

Arquivo:

```text
/etc/systemd/system/noip-duc.service
```

Conteúdo:

```ini
[Unit]
Description=No-IP Dynamic Update Client
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
EnvironmentFile=/etc/noip-duc.env
ExecStart=/usr/local/bin/noip-duc
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Após criar o serviço:

```bash
sudo systemctl daemon-reload
```

Habilitação no boot:

```bash
sudo systemctl enable noip-duc
```

Inicialização:

```bash
sudo systemctl start noip-duc
```

Validação:

```bash
sudo systemctl status noip-duc
```

---

## 17. Por que utilizar systemd

Sem o systemd, seria necessário entrar por SSH após cada inicialização da EC2 e executar manualmente o DUC.

Com:

```text
systemctl enable noip-duc
```

o fluxo passa a ser automático:

```text
EC2 inicia
   ↓
Linux inicia
   ↓
systemd
   ↓
noip-duc.service
   ↓
DUC verifica IP
   ↓
No-IP é atualizado
```

Isso elimina uma etapa operacional manual.

---

## 18. Troubleshooting - AWS Metadata

Inicialmente foi utilizado:

```text
NOIP_IP_METHOD=aws-metadata
```

O DUC tentou consultar:

```text
http://169.254.169.254/latest/meta-data/public-ipv4
```

Entretanto, a consulta não retornou o IP esperado.

O log apresentou:

```text
Failed to parse IP from
http://169.254.169.254/latest/meta-data/public-ipv4
```

Em vez de alterar as configurações de segurança do serviço de metadata da EC2 apenas para atender ao DUC, foi utilizado outro método suportado pelo cliente:

```text
NOIP_IP_METHOD=dns,http,http-port-8245
```

Após a alteração, o cliente detectou corretamente:

```text
got new ip
```

---

## 19. Troubleshooting - credenciais

Durante os testes também ocorreu:

```text
update failed; Incorrect credentials
```

As credenciais da DDNS Key foram revisadas no arquivo:

```text
/etc/noip-duc.env
```

Após a correção, o log apresentou:

```text
update successful
```

Isso confirmou que:

```text
DUC
 ↓
No-IP
```

estava autenticando corretamente.

---

## 20. Troubleshooting - update successful, mas DNS antigo

Mesmo após o DUC informar:

```text
update successful
```

o domínio continuava resolvendo para o IP anterior.

Foram utilizados:

```bash
dig +short sistema-escolar.servebeer.com A
```

Google DNS:

```bash
dig @8.8.8.8 +short sistema-escolar.servebeer.com A
```

Cloudflare DNS:

```bash
dig @1.1.1.1 +short sistema-escolar.servebeer.com A
```

Também foi utilizado:

```bash
dig +trace sistema-escolar.servebeer.com A
```

O trace mostrou que os servidores autoritativos do domínio pertenciam ao No-IP:

```text
nf1.no-ip.com
nf2.no-ip.com
nf3.no-ip.com
nf4.no-ip.com
```

A consulta direta ao servidor autoritativo:

```bash
dig @nf1.no-ip.com +short sistema-escolar.servebeer.com A
```

também retornava o IP antigo.

Isso provou que o problema não era simplesmente cache DNS.

---

## 21. Associação da DDNS Key

Durante o troubleshooting foi identificado que o hostname:

```text
sistema-escolar.servebeer.com
```

não estava marcado como target da DDNS Key criada no painel do No-IP.

Após associar o hostname à chave e atualizar a configuração, o DUC foi reiniciado:

```bash
sudo systemctl restart noip-duc
```

O log mostrou:

```text
got new ip
update successful
checking ip again in 5m
```

A consulta ao servidor autoritativo passou a retornar o novo endereço:

```bash
dig @nf1.no-ip.com +short sistema-escolar.servebeer.com A
```

Resultado observado:

```text
100.58.168.128
```

O DDNS estava finalmente validado de ponta a ponta.

---

## 22. Teste real de Stop/Start

Foi realizado um teste completo.

Antes da interrupção:

```text
IP público:
98.86.164.187
```

A instância foi interrompida:

```text
Stop
```

e iniciada novamente:

```text
Start
```

A AWS atribuiu:

```text
100.58.168.128
```

O serviço No-IP DUC iniciou automaticamente durante o boot.

Logs:

```text
got new ip; current=100.58.168.128
update successful; current=100.58.168.128
checking ip again in 5m
```

Finalmente:

```bash
dig @nf1.no-ip.com +short sistema-escolar.servebeer.com A
```

retornou:

```text
100.58.168.128
```

Isso comprovou que a automação funcionou.

---

## 23. Comportamento atual após iniciar a EC2

Atualmente não é necessário realizar conexão SSH para atualizar o endereço IP.

Após um Start:

```text
EC2 inicia
   ↓
novo IPv4 público é atribuído
   ↓
systemd inicia noip-duc
   ↓
DUC descobre o novo IP
   ↓
No-IP atualiza o registro DNS
   ↓
sistema-escolar.servebeer.com
passa a apontar para o novo IP
```

Da mesma forma, os demais serviços configurados para inicialização automática são carregados pelo sistema.

A conexão SSH fica necessária apenas para:

- manutenção;
- administração;
- troubleshooting;
- deploy;
- consulta de logs.

---

## 24. HTTPS após mudança do IP

O certificado TLS não foi emitido para o endereço IP.

Ele foi emitido para:

```text
sistema-escolar.servebeer.com
```

Portanto, uma mudança de:

```text
98.86.164.187
```

para:

```text
100.58.168.128
```

não exige um novo certificado.

Desde que:

```text
sistema-escolar.servebeer.com
```

continue resolvendo para a EC2 correta, o Nginx pode continuar utilizando o mesmo certificado.

Isso demonstra uma vantagem importante do uso de nomes DNS em vez de depender diretamente de endereços IP.

---

## 25. Renovação do certificado

O Certbot configurou a renovação automática do certificado Let's Encrypt.

O objetivo é evitar a renovação manual sempre que o certificado se aproximar da expiração.

A existência dos mecanismos de renovação pode ser verificada com os recursos disponibilizados pelo Certbot/systemd no servidor.

A renovação do certificado é independente da atualização DDNS:

```text
Certbot
→ gerencia certificado TLS

No-IP DUC
→ gerencia atualização do IP no DNS
```

São duas automações diferentes.

---

## 26. Limitação do No-IP gratuito

O hostname utilizado pertence ao serviço gratuito do No-IP.

Uma limitação importante é a necessidade de confirmação periódica do hostname, conforme as regras do plano gratuito.

Portanto:

```text
Atualização do IP
→ automática pelo DUC

Confirmação periódica do hostname
→ ação administrativa no No-IP
```

O DUC não deve ser confundido com a renovação/confirmação do hostname gratuito.

---

## 27. Arquitetura final

```text
Usuário / Navegador
        │
        │ HTTPS
        ▼
sistema-escolar.servebeer.com
        │
        │ DNS
        ▼
No-IP
        │
        │ A Record atualizado pelo DDNS
        ▼
IPv4 público dinâmico da EC2
        │
        ▼
Security Group
        │
        ├── 80  HTTP
        ├── 443 HTTPS
        └── 22  SSH restrito
        │
        ▼
Nginx
        │
        │ TLS - Let's Encrypt
        │ Reverse Proxy
        ▼
Gunicorn
127.0.0.1:8000
        │
        ▼
Flask
        │
        ▼
MariaDB
```

Paralelamente:

```text
EC2
 │
 ▼
systemd
 │
 ▼
noip-duc.service
 │
 ▼
detecta IPv4 público
 │
 ▼
No-IP
 │
 ▼
atualiza DNS
```

---

## 28. Fluxo após Stop/Start

```text
EC2 STOP
   ↓
instância fica indisponível
   ↓
EC2 START
   ↓
AWS atribui IPv4 público
   ↓
Linux inicializa
   ↓
systemd inicializa serviços
   ↓
No-IP DUC detecta IP
   ↓
No-IP atualiza DNS
   ↓
hostname aponta para a EC2
   ↓
Nginx recebe HTTPS
   ↓
Gunicorn
   ↓
Flask
   ↓
MariaDB
   ↓
Aplicação disponível novamente
```

---

## 29. Comandos úteis

### Status do DUC

```bash
sudo systemctl status noip-duc
```

### Reiniciar DUC

```bash
sudo systemctl restart noip-duc
```

### Logs

```bash
sudo journalctl -u noip-duc -n 30 --no-pager
```

Logs recentes:

```bash
sudo journalctl -u noip-duc --since "10 minutes ago" --no-pager
```

### Verificar se inicia no boot

```bash
sudo systemctl is-enabled noip-duc
```

### Resolver hostname

```bash
dig +short sistema-escolar.servebeer.com A
```

### Google DNS

```bash
dig @8.8.8.8 +short sistema-escolar.servebeer.com A
```

### Cloudflare DNS

```bash
dig @1.1.1.1 +short sistema-escolar.servebeer.com A
```

### Consultar diretamente o DNS autoritativo do No-IP

```bash
dig @nf1.no-ip.com +short sistema-escolar.servebeer.com A
```

### Validar Nginx

```bash
sudo nginx -t
```

### Status do Nginx

```bash
sudo systemctl status nginx
```

### Status da aplicação

```bash
sudo systemctl status sistema-escolar
```

### Status do banco

```bash
sudo systemctl status mariadb
```

---

## 30. Checklist após Start da EC2

Em condições normais nenhuma intervenção manual é necessária.

Caso a aplicação não volte, verificar:

```text
[ ] EC2 está Running
[ ] EC2 possui IPv4 público
[ ] noip-duc.service está ativo
[ ] DNS aponta para o IPv4 atual
[ ] nginx está ativo
[ ] sistema-escolar.service está ativo
[ ] mariadb está ativo
[ ] Security Group mantém 80/443 liberadas
[ ] HTTPS responde corretamente
```

A ordem de troubleshooting recomendada é:

```text
EC2
 ↓
IP público
 ↓
DDNS
 ↓
DNS
 ↓
Security Group
 ↓
Nginx
 ↓
Gunicorn
 ↓
Flask
 ↓
MariaDB
```

Essa ordem ajuda a investigar a infraestrutura de fora para dentro.

---

## 31. Resultado final

A aplicação passou a possuir um endereço estável:

```text
https://sistema-escolar.servebeer.com
```

mesmo utilizando uma EC2 com IPv4 público dinâmico.

O laboratório demonstrou na prática:

- DNS;
- DDNS;
- resolução de nomes;
- servidores DNS autoritativos;
- `dig`;
- reverse proxy;
- Nginx;
- HTTPS;
- TLS;
- Let's Encrypt;
- Certbot;
- systemd;
- gerenciamento seguro de credenciais;
- automação no boot;
- troubleshooting de infraestrutura;
- recuperação da aplicação após Stop/Start.

O resultado final elimina a necessidade de atualizar manualmente o endereço IP no No-IP após cada inicialização da EC2.

A infraestrutura consegue recuperar automaticamente o acesso pelo hostname após uma mudança de endereço IPv4 público.