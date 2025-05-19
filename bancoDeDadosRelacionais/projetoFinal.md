## 🧩 Estrutura – Concessionária de Veículos

### 🔹 Entidades e Atributos

#### **Veiculo**
- *PK* id_veiculo – Identificador único do veículo
- chassi – Código VIN (Vehicle Identification Number), único por veículo
- marca – Ex: Ford, Honda, Yamaha
- modelo – Ex: Civic, Fazer 250
- ano_fabricacao – Ex: 2022
- ano_modelo – Ex: 2023
- valor_tabela – Valor base do veículo (R$)
- tipo_combustivel – Ex: Gasolina, Etanol, Flex, Diesel, Elétrico
- cambio – Ex: Manual, Automático, CVT
- tipo_veiculo – Ex: Carro, Moto
- disponivel – Indica se está disponível para venda *(booleano)*

#### **Carro** *(Especialização de Veiculo)*
- *PK, FK* id_veiculo → Veiculo
- num_portas – Quantidade de portas (ex: 2, 4)
- tipo_motor – Ex: 1.0, 1.6 Turbo, 2.0
- tipo_airbag – Ex: Nenhum, Frontal, Completo
- possui_abs – Indica se possui sistema de freio ABS *(booleano)*

#### **Moto** *(Especialização de Veiculo)*
- *PK, FK* id_veiculo → Veiculo
- cilindradas – Potência do motor (ex: 150, 600)
- tipo_partida – Ex: Pedal, Elétrica, Mista
- possui_abs – Indica se possui freio ABS *(booleano)*

---

#### **Cliente**
- *PK* id_cliente – Identificador único do cliente
- nome – Nome completo (PF) ou razão social (PJ)
- endereco – Endereço completo
- telefone_contato – Número com DDD (ex: 11999990000)
- email – Endereço de e-mail válido
- tipo_cliente – Define o tipo: Física ou Jurídica
- data_cadastro – Data de registro do cliente no sistema

#### **Cliente_PF** *(Especialização de Cliente)*
- *PK, FK* id_cliente → Cliente
- cpf – Cadastro de Pessoa Física (formato: 00000000000)
- sexo – Masculino, Feminino, Outro
- data_nascimento – Data de nascimento do cliente

#### **Cliente_PJ** *(Especialização de Cliente)*
- *PK, FK* id_cliente → Cliente
- nome_fantasia – Nome comercial da empresa
- cnpj – Cadastro Nacional de Pessoa Jurídica (formato: 00000000000100)

---

#### **Funcionario**
- *PK* id_funcionario – Identificador único do funcionário
- nome – Nome completo
- cargo – Função exercida (ex: Vendedor, Gerente)
- data_admissao – Data de início das atividades
- salario – Valor atual do salário 

---

#### **Venda**
- *PK* id_venda – Identificador único da venda
- data_venda – Data em que a venda foi realizada
- *FK* id_cliente → Cliente – Cliente que realizou a compra
- *FK* id_funcionario → Funcionario – Funcionário responsável pela venda
- *FK* id_veiculo → Veiculo – Veículo vendido
- *FK* id_pagamento → Forma_Pagamento – Forma de pagamento escolhida
- valor_venda – Valor final da venda 
- desconto_aplicado – Valor de desconto, se houver
- comissao_vendedor – Valor da comissão do vendedor

---

#### **Forma_Pagamento**
- *PK* id_pagamento – Identificador da forma de pagamento
- metodo_pagamento – Ex: Dinheiro, Cartão de Crédito, Financiamento
- quantidade_parcelas – Número total de parcelas
- valor_parcela – Valor de cada parcela


---

### 🔗 Relacionamentos

- **Cliente** realiza **Venda**
- **Funcionario** efetua **Venda**
- **Veiculo** é vendido em **Venda**
- **Venda** utiliza uma **Forma_Pagamento**
- **Veiculo** se especializa em **Carro** ou **Moto**
- **Cliente** se especializa em **Cliente_PF** ou **Cliente_PJ**  
