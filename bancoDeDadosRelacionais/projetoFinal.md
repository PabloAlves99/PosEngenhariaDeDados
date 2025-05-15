## 🧩 Estrutura – Concessionária de Veículos

### 🔹 Entidades e Atributos

#### **Veiculo**
- *PK* id_veiculo
- marca
- modelo
- ano
- preco_atual
- tipo_combustivel
- cambio
- tipo *(Carro, Moto)*

#### **Carro** *(Especialização de Veiculo)*
- *PK, FK* id_veiculo → Veiculo
- num_portas
- tipo_motor

#### **Moto** *(Especialização de Veiculo)*
- *PK, FK* id_veiculo → Veiculo
- cilindradas
- tipo_partida

---

#### **Cliente**
- *PK* id_cliente
- nome
- endereco
- telefone
- tipo_cliente *(Física, Jurídica)*

#### **Cliente_PF** *(Especialização de Cliente)*
- *PK, FK* id_cliente → Cliente
- cpf
- sexo

#### **Cliente_PJ** *(Especialização de Cliente)*
- *PK, FK* id_cliente → Cliente
- nome_fantasia
- cnpj

---

#### **Funcionario**
- *PK* id_funcionario
- nome
- cargo
- data_admissao
- salario

---
#### **Venda**
- *PK* id_venda
- data_venda
- *FK* id_cliente → Cliente
- *FK* id_funcionario → Funcionario
- *FK* id_veiculo → Veiculo
- *FK* id_pagamento → Forma_Pagamento
- valor_venda

  
#### **Forma_Pagamento**
- *PK* id_pagamento
- metodo_pagamento *(Ex: Dinheiro, Cartão, Financiamento)*
- num_parcelas
- valor_parcela

---

### 🔗 Relacionamentos

- **Cliente** realiza **Venda**
- **Funcionario** efetua **Venda**
- **Veiculo** é vendido em **Venda**
- **Venda** utiliza uma **Forma_Pagamento**
- **Veiculo** se especializa em **Carro** ou **Moto**
- **Cliente** se especializa em **Cliente_PF** ou **Cliente_PJ**  
