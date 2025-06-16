INSERT INTO TipoVeiculo (descricao) VALUES 
('Carro'), 
('Moto'), 
('Caminhão');

INSERT INTO Marca (nome_marca) VALUES 
('Toyota'), 
('Honda'), 
('Ford');

INSERT INTO Modelo (marca_id, nome_modelo) VALUES 
(1, 'Corolla'), 
(2, 'Civic'), 
(3, 'Ranger');

INSERT INTO Versao (modelo_id, nome_versao, motorizacao, cambio) VALUES 
(1, 'XEI', '2.0 Flex', 'Automático'),
(2, 'EXL', '2.0 Flex', 'CVT'),
(3, 'XLS', '3.2 Diesel', 'Automatizado');

INSERT INTO ItemSerie (nome_item, categoria) VALUES 
('Airbag', 'Segurança'),
('Ar Condicionado', 'Conforto'),
('GPS', 'Tecnologia'),
('Rodas de Liga Leve', 'Visual');

-- Endereços para os clientes
INSERT INTO Endereco (logradouro, numero, complemento, bairro, cidade, estado, cep) VALUES 
('Av. Brasil', '1000', NULL, 'Centro', 'São Paulo', 'SP', '01000000'),
('Rua da Bahia', '500', 'Sala 10', 'Funcionários', 'Belo Horizonte', 'MG', '30160011'),
('Av. Amazonas', '1200', NULL, 'Centro', 'Belo Horizonte', 'MG', '30180000');


-- Clientes (2 PF e 1 PJ)
INSERT INTO Cliente (nome, endereco_id, telefone_contato, email, tipo_cliente, data_cadastro) VALUES 
('João da Silva', 1, '11999999999', 'joao@gmail.com', 'Física', CURDATE()),
('Maria Oliveira', 2, '31988887777', 'maria@gmail.com', 'Física', CURDATE()),
('Auto Center Ltda', 1, '1133334444', 'contato@autocenter.com', 'Jurídica', CURDATE()),
('Auto Bits LTDA', 2, '31999887766', 'contato@autobits.com', 'Jurídica', CURDATE()),
('Concessionária BH Veículos', 3, '3122223333', 'vendas@bhveiculos.com', 'Jurídica', CURDATE());

-- Pessoa Física (ligando ao cliente 1 e 2)
INSERT INTO ClientePF (id_cliente, cpf, sexo, data_nascimento) VALUES 
(1, '12345678900', 'Masculino', '1990-01-01'),
(2, '98765432100', 'Feminino', '1985-05-10');

-- Pessoa Jurídica (ligando ao cliente 3)
INSERT INTO ClientePJ (id_cliente, nome_fantasia, cnpj) VALUES 
(3, 'Auto Center', '11222333000188'),
(4, 'Auto Bits', '11277333000198'),
(3, 'BH Veículos', '11777333000177');


INSERT INTO Funcionario (nome, cargo, data_admissao, salario) VALUES 
('Maria Souza', 'Vendedora', '2020-02-01', 3500.00),
('Carlos Lima', 'Gerente', '2019-01-15', 5500.00),
('Fernanda Costa', 'Vendedora', '2021-07-10', 3200.00);

INSERT INTO Veiculo (placa, chassi, renavam, cor, ano_fabricacao, ano_modelo, quilometragem_atual, tipo_combustivel, tipo_veiculo_id, modelo_id, versao_id, status_veiculo) VALUES 
('DEF2G45', '9BWZZZ377VT004252', '98765432101', 'Branco', 2021, 2022, 15000, 'Flex', 1, 1, 1, 'Disponível'),
('GHI3J67', '9BWZZZ377VT004253', '12312312345', 'Prata', 2022, 2023, 8000, 'Flex', 1, 2, 2, 'Vendido'),
('JKL4M89', '9BWZZZ377VT004254', '32132132109', 'Preto', 2020, 2021, 30000, 'Diesel', 1, 3, 3, 'Reservado');


INSERT INTO VeiculoItemSerie (veiculo_id, item_serie_id) VALUES 
(1, 1),
(1, 2);

INSERT INTO HistoricoKM (veiculo_id, data_hist, quilometragem) VALUES 
(1, '2024-06-01', 9000),
(1, '2025-01-01', 10000);

INSERT INTO FormaPagamento (metodo_pagamento, quantidade_parcelas, valor_parcela) VALUES 
('Cartão', 10, 3500.00),
('Dinheiro', 1, 30000.00),
('Financiamento', 24, 1800.00);

INSERT INTO Venda (data_venda, id_cliente, id_funcionario, id_veiculo, id_pagamento, valor_venda, desconto_aplicado, comissao_vendedor) VALUES 
(CURDATE(), 1, 1, 1, 1, 35000.00, 2000.00, 500.00),
(CURDATE(), 2, 2, 2, 2, 30000.00, 0.00, 0.00),
(CURDATE(), 3, 3, 3, 3, 43200.00, 1200.00, 800.00);
