# Infraestrutura AWS — Camada de Rede

## 1. Objetivo

Este documento descreve a primeira etapa da infraestrutura AWS do projeto
**Sistema Escolar**, responsável pela criação e configuração da camada de rede.

O objetivo desta etapa foi construir manualmente a infraestrutura de rede,
entendendo a função de cada componente antes da criação e configuração
do servidor EC2.

A arquitetura foi criada na região:

- **Região AWS:** US East (N. Virginia)
- **Código da região:** `us-east-1`

Nesta primeira versão do ambiente foi utilizada uma arquitetura simples,
adequada para estudos, desenvolvimento e validação da aplicação.

---

# 2. VPC — Virtual Private Cloud

## O que é?

A VPC é uma rede virtual privada criada dentro da AWS.

Ela funciona como o limite principal da nossa infraestrutura de rede.
Recursos como EC2, sub-redes, tabelas de rotas e outros componentes podem
ser organizados dentro dessa rede.

## Configuração utilizada

- **Nome:** `sistema-escolar-vpc`
- **CIDR IPv4:** `10.0.0.0/16`
- **IPv6:** não utilizado
- **Tenancy:** Default

## Por que foi criada?

A VPC foi criada para que o Sistema Escolar tenha sua própria rede lógica,
em vez de utilizar diretamente a VPC padrão fornecida pela AWS.

Isso permite controlar:

- endereçamento IP;
- criação das sub-redes;
- roteamento;
- acesso à internet;
- isolamento dos recursos;
- regras de segurança.

O bloco:

`10.0.0.0/16`

representa o espaço de endereçamento reservado para a nossa VPC.

Uma maneira simples de visualizar é considerar a VPC como um grande terreno.
As sub-redes serão divisões menores desse terreno.

---

# 3. Sub-rede pública

## O que é?

Uma subnet (sub-rede) é uma divisão da rede principal da VPC.

Ela permite separar e organizar os recursos da infraestrutura.

## Configuração utilizada

- **Nome:** `sistema-escolar-public-subnet-1a`
- **CIDR IPv4:** `10.0.1.0/24`
- **Tipo planejado:** Pública
- **VPC:** `sistema-escolar-vpc`

A subnet pertence a uma única Availability Zone da região `us-east-1`.

> A Availability Zone utilizada deve ser conferida no console AWS e
> registrada aqui de acordo com a configuração real da subnet.

## Por que usamos `/24`?

A VPC possui o bloco:

`10.0.0.0/16`

Em vez de utilizar todo esse espaço em uma única subnet, foi reservado:

`10.0.1.0/24`

para a primeira subnet.

Isso mantém a rede organizada e permite criar outras sub-redes futuramente,
por exemplo, sub-redes privadas ou sub-redes em outras Availability Zones.

## Por que uma subnet pública?

Nesta primeira arquitetura, a instância EC2 que hospedará a aplicação
precisa ser acessível pela internet.

Por isso, ela será posicionada nesta subnet.

É importante observar que **o nome "public" não torna uma subnet pública**.

Para que ela tenha conectividade com a internet, também é necessário
configurar corretamente:

1. Internet Gateway;
2. tabela de rotas;
3. rota para a internet;
4. associação da tabela de rotas à subnet;
5. endereço IP público no recurso que necessita de acesso externo.

---

# 4. Availability Zone — AZ

## O que é?

Uma Availability Zone é uma localização isolada dentro de uma região AWS.

A região `us-east-1`, por exemplo, possui múltiplas Availability Zones.

Enquanto a VPC pertence à região, cada subnet pertence especificamente
a uma Availability Zone.

A relação pode ser visualizada assim:

Região → VPC → Availability Zone → Subnet

## Por que estamos utilizando apenas uma AZ?

Nesta primeira etapa, o objetivo é aprender e validar a arquitetura básica
da aplicação sem adicionar complexidade desnecessária.

Uma única Availability Zone é suficiente para o laboratório atual.

Em uma arquitetura de produção com requisito de alta disponibilidade,
seria recomendável distribuir os recursos entre duas ou mais
Availability Zones.

Isso reduz a dependência de uma única zona.

---

# 5. Internet Gateway — IGW

## O que é?

O Internet Gateway é o componente que permite comunicação entre uma VPC
e a internet.

Ele é anexado à VPC.

## Configuração utilizada

- **Nome:** `sistema-escolar-igw`
- **VPC associada:** `sistema-escolar-vpc`
- **Estado:** Attached

## Por que foi criado?

Sem um Internet Gateway, nossa VPC não teria um caminho de comunicação
direta com a internet.

Uma analogia utilizada durante a construção foi:

- **VPC:** condomínio;
- **Internet Gateway:** portão do condomínio;
- **Internet:** rua externa.

Porém, possuir um portão não é suficiente.

Também precisamos de uma regra indicando que o tráfego destinado à
internet deve utilizar esse portão.

Essa função pertence à tabela de rotas.

---

# 6. Route Table — Tabela de Rotas

## O que é?

A Route Table determina para onde o tráfego da rede deve ser encaminhado.

Ela funciona como uma tabela de decisões de roteamento.

Podemos pensar nela como as placas de trânsito da nossa rede.

## Rota interna

A VPC possui uma rota local:

`10.0.0.0/16 → local`

Essa rota permite a comunicação interna entre recursos pertencentes ao
espaço de endereçamento da VPC, respeitando também os demais controles
de rede e segurança.

Essa rota é criada automaticamente pela AWS.

## Rota para a internet

Foi adicionada a seguinte rota:

`0.0.0.0/0 → Internet Gateway`

O destino:

`0.0.0.0/0`

representa qualquer endereço IPv4 que não corresponda a uma rota mais
específica existente na tabela.

O destino dessa rota é o Internet Gateway criado para o projeto.

## Por que essa rota é necessária?

O Internet Gateway fornece a conexão entre a VPC e a internet, mas é a
Route Table que determina que o tráfego externo deve utilizar esse gateway.

Utilizando nossa analogia:

- Internet Gateway = portão;
- Route Table = placa indicando o caminho até o portão.

---

# 7. Associação da Route Table com a Subnet

Após configurar a tabela de rotas, ela foi associada à subnet:

`sistema-escolar-public-subnet-1a`

## Por que essa associação é necessária?

Uma subnet precisa utilizar uma tabela de rotas para determinar como seu
tráfego será encaminhado.

Ao associar nossa tabela à subnet pública, os recursos dessa subnet passam
a utilizar as rotas configuradas nela.

Entre elas:

`0.0.0.0/0 → Internet Gateway`

Dessa maneira, construímos o caminho de rede necessário para a comunicação
com a internet.

---

# 8. Fluxo da rede

A arquitetura construída até esta etapa pode ser visualizada de forma
simplificada:

Internet
   |
   v
Internet Gateway
   |
   v
VPC — 10.0.0.0/16
   |
   v
Route Table
   |
   |-- 10.0.0.0/16 → local
   |
   |-- 0.0.0.0/0 → Internet Gateway
   |
   v
Subnet Pública — 10.0.1.0/24
   |
   v
EC2

A EC2 será protegida adicionalmente por um Security Group.

---

# 9. Decisões de arquitetura

Nesta primeira versão foram tomadas algumas decisões visando simplicidade,
aprendizado e baixo custo.

### VPC própria

Foi utilizada uma VPC criada especificamente para o projeto, em vez da
VPC padrão da AWS.

**Motivo:** aprender e controlar manualmente a arquitetura de rede.

### IPv4 privado

Foi utilizado o bloco:

`10.0.0.0/16`

**Motivo:** utilizar um espaço de endereçamento privado e possuir espaço
suficiente para futuras subdivisões.

### Uma única Availability Zone

Nesta primeira versão será utilizada apenas uma AZ.

**Motivo:** reduzir a complexidade durante o aprendizado inicial.

Em uma evolução futura, a arquitetura poderá utilizar múltiplas AZs para
alta disponibilidade.

### Uma subnet pública inicial

Foi criada inicialmente uma subnet pública.

**Motivo:** permitir a hospedagem e validação da primeira EC2 da aplicação.

Futuramente, recursos que não precisam de exposição direta à internet,
como um banco de dados, poderão ser colocados em sub-redes privadas.

### Configuração manual

Todos os componentes foram criados manualmente pelo console AWS.

**Motivo:** compreender cada recurso e sua relação antes de automatizar
a infraestrutura.

Em uma etapa futura, essa infraestrutura poderá ser reproduzida utilizando
Infrastructure as Code (IaC), por exemplo com Terraform.

---

# 10. Resultado da etapa

Ao final desta etapa, a camada básica de rede do Sistema Escolar possui:

- VPC própria;
- bloco CIDR definido;
- subnet pública;
- Availability Zone associada à subnet;
- Internet Gateway anexado à VPC;
- Route Table;
- rota local;
- rota `0.0.0.0/0` apontando para o Internet Gateway;
- associação entre Route Table e subnet pública.

Com isso, a base de rede necessária para hospedar a primeira instância EC2
foi construída.

A próxima camada da arquitetura é responsável por controlar quais
comunicações serão permitidas para a instância, utilizando
**Security Groups**.
