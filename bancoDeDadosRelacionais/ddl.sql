CREATE DATABASE IF NOT EXISTS Concessionaria;
USE Concessionaria;

CREATE TABLE TipoVeiculo (
	id_tipo INT AUTO_INCREMENT PRIMARY KEY,
    descricao VARCHAR(50) NOT NULL
);

CREATE TABLE Marca (
	id_marca INT AUTO_INCREMENT PRIMARY KEY,
    nome_marca VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE Modelo (
	id_modelo INT AUTO_INCREMENT PRIMARY KEY,
    marca_id INT NOT NULL,
    nome_modelo VARCHAR(50) NOT NULL UNIQUE,
    
    FOREIGN KEY (marca_id) REFERENCES Marca(id_marca)
		ON DELETE RESTRICT
		ON UPDATE CASCADE
);

CREATE TABLE Versao (
	id_versao INT AUTO_INCREMENT PRIMARY KEY,
    modelo_id INT NOT NULL,
    nome_versao VARCHAR(50) NOT NULL,
    motorizacao VARCHAR(50) NOT NULL,
    cambio VARCHAR(50) NOT NULL,
    
    FOREIGN KEY (modelo_id) REFERENCES Modelo(id_modelo)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
    
    CONSTRAINT chk_cambio CHECK (cambio IN ('Manual', 'Automático', 'Automatizado', 'CVT')),
    
    UNIQUE (modelo_id, nome_versao)

);

CREATE TABLE ItemSerie (
	id_item INT AUTO_INCREMENT PRIMARY KEY,
    nome_item VARCHAR(50) NOT NULL UNIQUE,
    categoria VARCHAR(50) NOT NULL,
    
    CONSTRAINT chk_categoria CHECK (categoria IN ('Segurança', 'Conforto', 'Tecnologia', 'Visual'))
);

CREATE TABLE Veiculo (
	id_veiculo INT PRIMARY KEY AUTO_INCREMENT,
    placa VARCHAR(8) NOT NULL UNIQUE,
    chassi VARCHAR(50) NOT NULL UNIQUE,
    renavam VARCHAR(11) NOT NULL UNIQUE,
    cor VARCHAR(50) NOT NULL,
    ano_fabricacao YEAR NOT NULL,
    ano_modelo YEAR NOT NULL,
    quilometragem_atual INT NOT NULL,
    tipo_combustivel VARCHAR(50) NOT NULL,
    tipo_veiculo_id INT NOT NULL,
    modelo_id INT NOT NULL,
    versao_id INT NOT NULL,
    status_veiculo VARCHAR(50) NOT NULL,
    
    FOREIGN KEY (tipo_veiculo_id) REFERENCES TipoVeiculo(id_tipo)
		ON DELETE RESTRICT
		ON UPDATE CASCADE,

	FOREIGN KEY (modelo_id) REFERENCES Modelo(id_modelo)
		ON DELETE RESTRICT
		ON UPDATE CASCADE,

	FOREIGN KEY (versao_id) REFERENCES Versao(id_versao)
		ON DELETE RESTRICT
		ON UPDATE CASCADE,

    CONSTRAINT chk_status CHECK (status_veiculo IN ('Disponível', 'Vendido', 'Reservado')),
    CONSTRAINT chk_combustivel CHECK (tipo_combustivel IN ('Gasolina', 'Etanol', 'Diesel', 'Flex', 'Elétrico'))
);

CREATE TABLE VeiculoItemSerie (
	id_vis INT PRIMARY KEY AUTO_INCREMENT,
    veiculo_id INT NOT NULL,
    item_serie_id INT NOT NULL,
    
    FOREIGN KEY (veiculo_id) REFERENCES Veiculo(id_veiculo)
		ON DELETE CASCADE
		ON UPDATE CASCADE,

	FOREIGN KEY (item_serie_id) REFERENCES ItemSerie(id_item)
		ON DELETE RESTRICT
		ON UPDATE CASCADE
);

CREATE TABLE HistoricoKM (
	id_hist INT PRIMARY KEY AUTO_INCREMENT,
    veiculo_id INT NOT NULL,
    data_hist DATE NOT NULL,
    quilometragem INT NOT NULL,
    
    FOREIGN KEY (veiculo_id) REFERENCES Veiculo(id_veiculo)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

CREATE TABLE Endereco (
    id_endereco INT AUTO_INCREMENT PRIMARY KEY,
    logradouro VARCHAR(100) NOT NULL,
    numero VARCHAR(10) NOT NULL,
    complemento VARCHAR(50),
    bairro VARCHAR(50) NOT NULL,
    cidade VARCHAR(50) NOT NULL,
    estado CHAR(2) NOT NULL,
    cep VARCHAR(8) NOT NULL
);

CREATE TABLE Cliente (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    endereco_id INT NOT NULL,
    telefone_contato VARCHAR(11) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    tipo_cliente VARCHAR(10) NOT NULL,
    data_cadastro DATE NOT NULL,
    
    FOREIGN KEY (endereco_id) REFERENCES Endereco(id_endereco)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,

    CONSTRAINT chk_tipo_cliente CHECK (tipo_cliente IN ('Física', 'Jurídica'))
);

CREATE TABLE ClientePF (
    id_cliente INT PRIMARY KEY,
    cpf VARCHAR(11) NOT NULL UNIQUE,
    sexo VARCHAR(10) NOT NULL,
    data_nascimento DATE NOT NULL,

    CONSTRAINT chk_sexo CHECK (sexo IN ('Masculino', 'Feminino', 'Outro')),

    FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE ClientePJ (
    id_cliente INT PRIMARY KEY,
    nome_fantasia VARCHAR(100) NOT NULL,
    cnpj VARCHAR(14) NOT NULL UNIQUE,

    FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Funcionario (
    id_funcionario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cargo VARCHAR(50) NOT NULL,
    data_admissao DATE NOT NULL,
    salario DECIMAL(10,2) NOT NULL
);

CREATE TABLE FormaPagamento (
    id_pagamento INT AUTO_INCREMENT PRIMARY KEY,
    metodo_pagamento VARCHAR(20) NOT NULL,
    quantidade_parcelas INT DEFAULT 1,
    valor_parcela DECIMAL(10,2),

    CONSTRAINT chk_metodo_pagamento CHECK (metodo_pagamento IN ('Dinheiro', 'Cartão', 'Financiamento'))
);

CREATE TABLE Venda (
    id_venda INT AUTO_INCREMENT PRIMARY KEY,
    data_venda DATE NOT NULL,
    id_cliente INT NOT NULL,
    id_funcionario INT NOT NULL,
    id_veiculo INT NOT NULL,
    id_pagamento INT NOT NULL,
    valor_venda DECIMAL(10,2) NOT NULL,
    desconto_aplicado DECIMAL(10,2) DEFAULT 0.00,
    comissao_vendedor DECIMAL(10,2) DEFAULT 0.00,

    FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    FOREIGN KEY (id_funcionario) REFERENCES Funcionario(id_funcionario)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    FOREIGN KEY (id_veiculo) REFERENCES Veiculo(id_veiculo)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    FOREIGN KEY (id_pagamento) REFERENCES FormaPagamento(id_pagamento)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE INDEX idx_status ON Veiculo(status_veiculo);
CREATE INDEX idx_combustivel ON Veiculo(tipo_combustivel);
CREATE INDEX idx_data_venda ON Venda(data_venda);




