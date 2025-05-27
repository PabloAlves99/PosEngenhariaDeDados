# 🧩 Estrutura – Concessionária de Veículos (Modelo Atualizado)

## 🔹 Entidades e Atributos

### TipoVeiculo
- **id_tipo** (PK) – Identificador único do tipo
- **descricao** – Descrição do tipo (Ex: Carro, Moto)

---

### Marca
- **id_marca** (PK) – Identificador único da marca
- **nome_marca** – Nome da marca (Ex: Ford, Honda, Yamaha)

---

### Modelo
- **id_modelo** (PK) – Identificador único do modelo
- **marca_id** (FK) → Marca(id_marca) – Marca associada ao modelo
- **nome_modelo** – Nome do modelo (Ex: Civic, Fazer 250)

---

### Versao
- **id_versao** (PK) – Identificador único da versão
- **modelo_id** (FK) → Modelo(id_modelo) – Modelo associado
- **nome_versao** – Nome da versão (Ex: EXL, Sport)
- **motorizacao** – Detalhes da motorização (Ex: 1.5 Turbo, 250cc)
- **cambio** – Tipo de câmbio (Ex: Manual, Automático, CVT)

---

### ItemSerie
- **id_item** (PK) – Identificador único do item
- **nome_item** – Nome do item de série (Ex: Airbag, ABS, Ar-condicionado)
- **categoria** – Categoria do item (Ex: Segurança, Conforto, Tecnologia, Visual)

---

### Veiculo
- **id_veiculo** (PK) – Identificador único do veículo
- **placa** – Placa do veículo (Ex: ABC1D23)
- **chassi** – Código VIN, único
- **renavam** – Registro Nacional de Veículos Automotores
- **cor** – Cor do veículo
- **ano_fabricacao** – Ano de fabricação
- **ano_modelo** – Ano do modelo
- **quilometragem_atual** – Quilometragem atual
- **tipo_combustivel** – Ex: Gasolina, Etanol, Flex, Diesel, Elétrico
- **tipo_veiculo_id** (FK) → TipoVeiculo(id_tipo) – Tipo do veículo
- **modelo_id** (FK) → Modelo(id_modelo) – Modelo associado
- **versao_id** (FK) → Versao(id_versao) – Versão do modelo
- **status_veiculo** – Disponibilidade do veículo (Ex: Disponível, Vendido, Reservado)

---

### VeiculoItemSerie
- **id_vis** (PK) – Identificador da relação
- **veiculo_id** (FK) → Veiculo(id_veiculo) – Veículo associado
- **id_item_serie** (FK) → ItemSerie(id_item) – Item de série associado

---

### HistoricoKM
- **id_hist** (PK) – Identificador do registro
- **veiculo_id** (FK) → Veiculo(id_veiculo) – Veículo relacionado
- **data_hist** – Data da medição
- **quilometragem** – Quilometragem registrada

---

### Endereco
- **id_endereco** (PK) – Identificador único do endereço
- **logradouro** – Nome da rua/avenida
- **numero** – Número do imóvel
- **complemento** – Complemento (se houver)
- **bairro** – Bairro
- **cidade** – Cidade
- **estado** – Estado (UF)
- **cep** – Código postal

---

### Cliente
- **id_cliente** (PK) – Identificador único do cliente
- **nome** – Nome completo (PF) ou razão social (PJ)
- **endereco_id** (FK) → Endereco(id_endereco) – Endereço completo
- **telefone_contato** – Número com DDD
- **email** – E-mail válido
- **tipo_cliente** – Física ou Jurídica
- **data_cadastro** – Data de registro

---

### ClientePF (Especialização de Cliente)
- **id_cliente** (PK, FK) → Cliente(id_cliente)
- **cpf** – Cadastro de Pessoa Física
- **sexo** – Masculino, Feminino, Outro
- **data_nascimento** – Data de nascimento

---

### ClientePJ (Especialização de Cliente)
- **id_cliente** (PK, FK) → Cliente(id_cliente)
- **nome_fantasia** – Nome comercial
- **cnpj** – Cadastro Nacional de Pessoa Jurídica

---

### Funcionario
- **id_funcionario** (PK) – Identificador único do funcionário
- **nome** – Nome completo
- **cargo** – Função (Ex: Vendedor, Gerente)
- **data_admissao** – Data de admissão
- **salario** – Valor do salário

---

### FormaPagamento
- **id_pagamento** (PK) – Identificador único da forma de pagamento
- **metodo_pagamento** – Ex: Dinheiro, Cartão, Financiamento
- **quantidade_parcelas** – Total de parcelas (padrão 1)
- **valor_parcela** – Valor de cada parcela

---

### Venda
- **id_venda** (PK) – Identificador único da venda
- **data_venda** – Data da venda
- **id_cliente** (FK) → Cliente(id_cliente) – Cliente comprador
- **id_funcionario** (FK) → Funcionario(id_funcionario) – Funcionário responsável
- **id_veiculo** (FK) → Veiculo(id_veiculo) – Veículo vendido
- **id_pagamento** (FK) → FormaPagamento(id_pagamento) – Forma de pagamento
- **valor_venda** – Valor final
- **desconto_aplicado** – Desconto aplicado (padrão 0.00)
- **comissao_vendedor** – Comissão do vendedor (padrão 0.00)

---

## 🔗 Relacionamentos

- **Veiculo** → **TipoVeiculo** (N:1)  
- **Veiculo** → **Modelo** (N:1)  
- **Modelo** → **Marca** (N:1)  
- **Veiculo** → **Versao** (N:1)  
- **Veiculo** → **ItemSerie** (N:N via VeiculoItemSerie)  
- **Veiculo** → **HistoricoKM** (1:N)  
- **Cliente** → **Endereco** (N:1)  
- **Cliente** → **Venda** (1:N)  
- **Funcionario** → **Venda** (1:N)  
- **Venda** → **Veiculo** (1:1)  
- **Venda** → **FormaPagamento** (N:1)  
- **Cliente** → **ClientePF** ou **ClientePJ** (Especialização total e disjunta)

---
