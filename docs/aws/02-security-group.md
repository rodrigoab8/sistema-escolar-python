# Infraestrutura AWS — Security Group

## 1. Objetivo

Este documento descreve a configuração do **Security Group** utilizado
no projeto Sistema Escolar.

Após a criação da camada básica de rede da AWS, composta por VPC, subnet,
Internet Gateway e tabela de rotas, foi necessário definir quais tipos
de comunicação seriam permitidos para a instância EC2.

Para isso, foi criado um Security Group específico para o projeto.

---

# 2. O que é um Security Group?

O Security Group funciona como um firewall virtual associado aos recursos
da AWS, como uma instância EC2.

Ele controla o tráfego permitido por meio de dois tipos de regras:

- **Inbound Rules:** regras de entrada;
- **Outbound Rules:** regras de saída.

As regras podem considerar informações como:

- protocolo;
- porta;
- origem do tráfego;
- destino do tráfego.

No projeto Sistema Escolar, o Security Group foi configurado seguindo
o princípio de liberar somente os acessos necessários.

---

# 3. Security Group do projeto

## Configuração

- **Nome:** `sistema-escolar-sg`
- **VPC:** `sistema-escolar-vpc`

O Security Group foi criado especificamente para os recursos do
Sistema Escolar.

## Por que não utilizar o Security Group default?

A AWS cria um Security Group padrão para cada VPC.

Para este projeto foi criado um grupo específico.

Isso facilita:

- identificação das regras;
- manutenção;
- documentação;
- separação de responsabilidades;
- futuras alterações na arquitetura.

Dessa maneira, as regras de segurança do Sistema Escolar não ficam
misturadas com regras de outros recursos.

---

# 4. Regras de entrada — Inbound Rules

As regras de entrada determinam quais conexões externas podem chegar
até o recurso protegido pelo Security Group.

Foram configurados dois tipos de acesso:

| Tipo | Protocolo | Porta | Origem |
|---|---|---:|---|
| HTTP | TCP | 80 | `0.0.0.0/0` |
| SSH | TCP | 22 | Meu IP público |

---

# 5. HTTP — Porta 80

## O que é?

HTTP é um protocolo utilizado para comunicação entre clientes web
e servidores.

A porta padrão utilizada pelo HTTP é:

`80/TCP`

## Configuração

A regra foi configurada com origem:

`0.0.0.0/0`

Isso significa que conexões IPv4 provenientes de qualquer endereço
da internet podem chegar à porta 80 da instância.

## Por que permitimos acesso público?

O objetivo da aplicação é permitir que usuários acessem o Sistema Escolar
por meio de um navegador.

Portanto, o serviço web precisa estar disponível externamente.

Essa regra não significa que todas as portas do servidor estão abertas.

Somente a porta especificamente autorizada pelo Security Group pode
receber esse tipo de conexão.

---

# 6. SSH — Porta 22

## O que é?

SSH (Secure Shell) é um protocolo utilizado para administração remota
de servidores.

A porta padrão utilizada pelo SSH é:

`22/TCP`

No projeto, o SSH será utilizado inicialmente para acessar a EC2 e
realizar manualmente tarefas como:

- atualizar o sistema operacional;
- instalar dependências;
- instalar e configurar Python;
- configurar a aplicação;
- consultar arquivos e logs;
- executar comandos administrativos.

## Configuração

Diferentemente do HTTP, a porta SSH não foi aberta para toda a internet.

A origem foi configurada utilizando:

`My IP`

Dessa maneira, somente o endereço IP público autorizado pode iniciar
uma conexão SSH com a instância.

---

# 7. Por que não liberar SSH para 0.0.0.0/0?

Uma regra como:

`22/TCP → 0.0.0.0/0`

permitiria tentativas de conexão SSH provenientes de qualquer endereço
IPv4 da internet.

Embora a autenticação por chave ainda forneça proteção, essa exposição
é desnecessária para o laboratório.

Por isso, foi aplicado o princípio do menor privilégio:

> Permitir somente o acesso necessário, para quem precisa e pelo
> caminho necessário.

Como apenas o administrador do ambiente precisa utilizar SSH neste
momento, a origem foi limitada ao IP utilizado para administração.

---

# 8. Regras de saída — Outbound Rules

As regras de saída determinam para quais destinos a instância pode
iniciar comunicações.

Nesta primeira versão foi mantida a regra:

| Tipo | Protocolo | Destino |
|---|---|---|
| All Traffic | Todos | `0.0.0.0/0` |

## Por que permitimos todo o tráfego de saída?

Durante a preparação da EC2, o servidor precisará iniciar conexões
externas para atividades como:

- baixar atualizações do sistema operacional;
- instalar pacotes;
- acessar repositórios de software;
- instalar dependências da aplicação.

Por isso, nesta etapa inicial, a saída foi mantida liberada.

Em ambientes com requisitos de segurança mais rigorosos, regras de
saída também podem ser restringidas.

---

# 9. Entrada e saída

Uma maneira simples de entender a diferença é:

### Inbound

Pergunta:

> Quem pode iniciar uma comunicação com meu servidor?

Exemplos do projeto:

`Internet → HTTP 80 → EC2`

`Administrador → SSH 22 → EC2`

### Outbound

Pergunta:

> Com quem meu servidor pode iniciar uma comunicação?

Exemplo:

`EC2 → Internet → repositórios e serviços externos`

Portanto:

**Inbound controla quem entra.**

**Outbound controla para onde o servidor pode sair.**

---

# 10. Princípio do menor privilégio

Uma das decisões mais importantes desta etapa foi evitar a liberação
desnecessária de portas.

Não foi utilizada uma regra permitindo todas as conexões de entrada.

Foram autorizados somente os serviços necessários:

- porta `80` para acesso HTTP;
- porta `22` para administração via SSH.

Além disso, o SSH foi limitado ao IP do administrador.

Essa abordagem reduz a superfície de exposição do servidor.

---

# 11. Relação com a arquitetura de rede

O Security Group adiciona uma nova camada à infraestrutura construída
anteriormente.

O fluxo simplificado passa a ser:

Internet
   |
   v
Internet Gateway
   |
   v
Route Table
   |
   v
Subnet Pública
   |
   v
Security Group
   |
   |-- HTTP : 80  <- Internet
   |
   |-- SSH  : 22  <- IP autorizado
   |
   v
EC2
   |
   v
Sistema Escolar

É importante entender que cada componente possui uma responsabilidade.

O Internet Gateway fornece conectividade entre a VPC e a internet.

A Route Table determina o caminho do tráfego.

O Security Group determina qual tráfego é permitido para o recurso.

---

# 12. Decisões de segurança

## Security Group dedicado

Foi criado um Security Group exclusivo para o Sistema Escolar.

**Motivo:** facilitar organização, manutenção e controle das regras.

## HTTP público

A porta 80 foi disponibilizada para `0.0.0.0/0`.

**Motivo:** permitir que usuários acessem a aplicação web.

## SSH restrito

A porta 22 foi limitada ao IP utilizado para administração.

**Motivo:** não existe necessidade de disponibilizar o acesso
administrativo para toda a internet.

## Saída liberada

O tráfego de saída foi mantido liberado nesta primeira versão.

**Motivo:** permitir atualizações, instalação de pacotes e comunicação
externa necessária durante a configuração do servidor.

---

# 13. Observação sobre mudança de IP

A regra SSH foi criada utilizando o IP público do administrador no
momento da configuração.

Caso esse endereço IP público mude, a regra do Security Group poderá
precisar ser atualizada.

Isso não exige recriar o Security Group ou a instância EC2.

Basta alterar a origem autorizada na regra SSH.

---

# 14. Resultado da etapa

Ao final desta etapa, o projeto possui um Security Group específico
protegendo a instância EC2.

As regras implementadas permitem:

- acesso público à aplicação através de HTTP;
- administração remota através de SSH somente pelo IP autorizado;
- comunicação de saída da EC2 com a internet.

A configuração segue uma abordagem inicial baseada no
**princípio do menor privilégio**, evitando liberar portas de entrada
que não são necessárias para o funcionamento atual da aplicação.

Com a camada de rede e o Security Group configurados, a infraestrutura
está preparada para a criação e configuração da instância EC2.
