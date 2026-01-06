CREATE SCHEMA dw;
GO

CREATE TABLE dw.dim_tempo
(
    sk_tempo INT IDENTITY(1,1) NOT NULL,
    nu_ano INT NOT NULL,
    nu_mes INT NOT NULL,
    no_mes VARCHAR(20) NOT NULL,

    CONSTRAINT pk_dim_tempo PRIMARY KEY (sk_tempo)
);

CREATE TABLE dw.dim_municipio
(
    sk_municipio INT IDENTITY(1,1) NOT NULL,
    co_municipio INT NOT NULL,
    sg_uf CHAR(2) NOT NULL,
    no_municipio VARCHAR(150) NOT NULL,

    CONSTRAINT pk_dim_municipio PRIMARY KEY (sk_municipio),
    CONSTRAINT uq_dim_municipio UNIQUE (co_municipio)
);

CREATE TABLE dw.dim_pessoa
(
    sk_pessoa INT IDENTITY(1,1) NOT NULL,
    sexo CHAR(1) NOT NULL,
    faixa_etaria VARCHAR(30) NOT NULL,
    escolaridade INT NOT NULL,

    CONSTRAINT pk_dim_pessoa PRIMARY KEY (sk_pessoa)
);

CREATE TABLE dw.fato_pnad_covid
(
    sk_tempo INT NOT NULL,
    sk_municipio INT NOT NULL,
    sk_pessoa INT NOT NULL,
    ocupacao INT,
    rendimento DECIMAL(12,2),
    sintomas INT,
    internado CHAR(1),
    teste_covid CHAR(1),

    CONSTRAINT pk_fato_pnad_covid PRIMARY KEY (sk_tempo, sk_municipio, sk_pessoa),

    CONSTRAINT fk_fato_tempo 
        FOREIGN KEY (sk_tempo) 
        REFERENCES dw.dim_tempo (sk_tempo),

    CONSTRAINT fk_fato_municipio 
        FOREIGN KEY (sk_municipio) 
        REFERENCES dw.dim_municipio (sk_municipio),

    CONSTRAINT fk_fato_pessoa 
        FOREIGN KEY (sk_pessoa) 
        REFERENCES dw.dim_pessoa (sk_pessoa)
);
