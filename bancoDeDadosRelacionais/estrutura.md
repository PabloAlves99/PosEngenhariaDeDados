## 🧩 Estrutura – Concessionária de Veículos (Modelo Atualizado)

### 🔹 Entidades e Atributos

#### **TipoVeiculo**
- *PK* id – Identificador único do tipo
- descricao – Descrição do tipo (Ex: Carro, Moto)

---

#### **Marca**
- *PK* id – Identificador único da marca
- nome – Nome da marca (Ex: Ford, Honda, Yamaha)

---

#### **Modelo**
- *PK* id – Identificador único do modelo
- *FK* marca_id → Marca – Marca associada ao modelo
- nome – Nome do modelo (Ex: Civic, Fazer 250)

---

#### **Versao**
- *PK* id – Identificador único da versão
- *FK* modelo_id → Modelo – Modelo associado
- nome – Nome da versão (Ex: EXL, Sport)
- motorizacao – Detalhes da motorização (Ex: 1.5 Turbo, 250cc)
- cambio – Tipo de câmbio (Ex: Manual, Automático, CVT)

---

#### **ItemSerie**
- *PK* id – Identificador único do item
- nome – Nome do item de série (Ex: Airbag, ABS, Ar-condicionado)
- categoria - (Ex: segurança, conforto, tecnologia)

---

#### **Veiculo**
- *PK* id – Identificador único do veículo
- placa – Placa do veículo (Ex: ABC1D23)
- chassi – Código VIN, único
- renavam – Registro Nacional de Veículos Automotores
- cor – Cor do veículo
- ano_fabricacao – Ano de fabricação
- ano_modelo – Ano do modelo
- quilometragem_atual – Quilometragem atual
- tipo_combustivel – Ex: Gasolina, Etanol, Flex, Diesel, Elétrico
- *FK* tipo_veiculo_id → TipoVeiculo – Tipo do veículo
- *FK* modelo_id → Modelo – Modelo associado
- *FK* versao_id → Versao – Versão do modelo
- status – Disponibilidade do veículo (Ex: Disponível, Vendido, Reservado)

---

#### **Veiculo_ItemSerie**
- *PK* id – Identificador da relação
- *FK* veiculo_id → Veiculo – Veículo associado
- *FK* item_serie_id → ItemSerie – Item de série associado

---

#### **Historico_Quilometragem**
- *PK* id – Identificador do registro
- *FK* veiculo_id → Veiculo – Veículo relacionado
- data – Data da medição
- quilometragem – Quilometragem registrada

---

#### **Cliente**
- *PK* id_cliente – Identificador único do cliente
- nome – Nome completo (PF) ou razão social (PJ)
- endereco – Endereço completo
- telefone_contato – Número com DDD
- email – E-mail válido
- tipo_cliente – Física ou Jurídica
- data_cadastro – Data de registro

---

#### **Cliente_PF** *(Especialização de Cliente)*
- *PK, FK* id_cliente → Cliente
- cpf – Cadastro de Pessoa Física
- sexo – Masculino, Feminino, Outro
- data_nascimento – Data de nascimento

---

#### **Cliente_PJ** *(Especialização de Cliente)*
- *PK, FK* id_cliente → Cliente
- nome_fantasia – Nome comercial
- cnpj – Cadastro Nacional de Pessoa Jurídica

---

#### **Funcionario**
- *PK* id_funcionario – Identificador único do funcionário
- nome – Nome completo
- cargo – Função (Ex: Vendedor, Gerente)
- data_admissao – Data de admissão
- salario – Valor do salário

---

#### **Venda**
- *PK* id_venda – Identificador único da venda
- data_venda – Data da venda
- *FK* id_cliente → Cliente – Cliente comprador
- *FK* id_funcionario → Funcionario – Funcionário responsável
- *FK* id_veiculo → Veiculo – Veículo vendido
- *FK* id_pagamento → Forma_Pagamento – Forma de pagamento
- valor_venda – Valor final
- desconto_aplicado – Desconto, se houver
- comissao_vendedor – Comissão do vendedor

---

#### **Forma_Pagamento**
- *PK* id_pagamento – Identificador único
- metodo_pagamento – Ex: Dinheiro, Cartão, Financiamento
- quantidade_parcelas – Total de parcelas
- valor_parcela – Valor de cada parcela

---

### 🔗 Relacionamentos

- **Veiculo** → **TipoVeiculo** *(N:1)*  
  Cada veículo pertence a um tipo de veículo.

- **Veiculo** → **Modelo** *(N:1)*  
  Cada veículo pertence a um modelo.

- **Modelo** → **Marca** *(N:1)*  
  Cada modelo pertence a uma marca.

- **Veiculo** → **Versao** *(N:1)*  
  Cada veículo possui uma versão específica.

- **Veiculo** → **ItemSerie** *(N:N via Veiculo_ItemSerie)*  
  Cada veículo possui vários itens de série e cada item pode pertencer a vários veículos.

- **Veiculo** → **Historico_Quilometragem** *(1:N)*  
  Cada veículo pode ter vários registros históricos de quilometragem.

- **Cliente** → **Venda** *(1:N)*  
  Cada cliente pode participar de várias vendas.

- **Funcionario** → **Venda** *(1:N)*  
  Cada funcionário pode efetuar várias vendas.

- **Venda** → **Veiculo** *(1:1)*  
  Cada venda refere-se a um único veículo.

- **Venda** → **Forma_Pagamento** *(N:1)*  
  Cada venda utiliza uma forma de pagamento.

- **Cliente** → **Cliente_PF** ou **Cliente_PJ**  
  Especialização total e disjunta.

