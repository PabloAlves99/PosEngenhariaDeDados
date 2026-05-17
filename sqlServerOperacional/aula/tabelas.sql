-- Criar Banco de Dados

CREATE DATABASE DW_Educacao;
GO

USE DW_Educacao;
GO

CREATE SCHEMA stg;
GO

CREATE SCHEMA dw;
GO

CREATE TABLE stg.censo_escolar_matricula (
    ano_censo        INT          NOT NULL,
    co_entidade      BIGINT       NOT NULL,
    no_entidade      VARCHAR(200) NOT NULL,
    co_municipio     INT          NOT NULL,
    uf               CHAR(2)      NOT NULL,
    tp_rede          TINYINT      NOT NULL,
    tp_etapa_ensino  INT          NOT NULL,
    qt_matricula     INT          NOT NULL,
    dt_carga         DATETIME2    DEFAULT SYSDATETIME()
);
GO

CREATE TABLE dw.dim_tempo (
    sk_tempo      INT IDENTITY(1,1) PRIMARY KEY,
    ano           INT      NOT NULL,
    mes           TINYINT  NOT NULL,
    dia           TINYINT  NOT NULL,
    dt_calendario DATE     NOT NULL
);
GO

CREATE TABLE dw.dim_municipio (
    sk_municipio   INT IDENTITY(1,1) PRIMARY KEY,
    co_municipio   INT          NOT NULL,
    uf             CHAR(2)      NOT NULL,
    nome_municipio VARCHAR(200) NOT NULL
);
GO

CREATE TABLE dw.dim_etapa_ensino (
    sk_etapa_ensino INT IDENTITY(1,1) PRIMARY KEY,
    tp_etapa_ensino INT          NOT NULL,
    ds_etapa_ensino VARCHAR(200) NOT NULL
);
GO

CREATE TABLE dw.dim_escola (
    sk_escola    INT IDENTITY(1,1) PRIMARY KEY,
    co_entidade  BIGINT       NOT NULL,
    no_entidade  VARCHAR(200) NOT NULL,
    co_municipio INT          NOT NULL,
    tp_rede      TINYINT      NOT NULL,
    dt_inicio    DATE         NOT NULL,
    dt_fim       DATE         NULL,
    fl_ativo     CHAR(1)      NOT NULL
);
GO

CREATE TABLE dw.fact_matricula (
    sk_tempo        INT NOT NULL,
    sk_escola       INT NOT NULL,
    sk_municipio    INT NOT NULL,
    sk_etapa_ensino INT NOT NULL,
    qt_matricula    INT NOT NULL,
    dt_carga        DATETIME2 DEFAULT SYSDATETIME(),

    CONSTRAINT fk_fact_tempo 
        FOREIGN KEY (sk_tempo) REFERENCES dw.dim_tempo(sk_tempo),

    CONSTRAINT fk_fact_escola 
        FOREIGN KEY (sk_escola) REFERENCES dw.dim_escola(sk_escola),

    CONSTRAINT fk_fact_municipio 
        FOREIGN KEY (sk_municipio) REFERENCES dw.dim_municipio(sk_municipio),

    CONSTRAINT fk_fact_etapa 
        FOREIGN KEY (sk_etapa_ensino) REFERENCES dw.dim_etapa_ensino(sk_etapa_ensino)
);
GO

CREATE TABLE dw.log_matricula_invalida (
    id_log INT IDENTITY(1,1) PRIMARY KEY,
    co_entidade BIGINT NOT NULL,
    co_municipio INT NOT NULL,
    tp_etapa_ensino INT NOT NULL,
    qt_matricula INT NOT NULL,
    dt_carga DATETIME2 NOT NULL DEFAULT SYSDATETIME()
);
GO

CREATE TABLE dw.log_auditoria_dimensoes (
    id_log INT IDENTITY(1,1) PRIMARY KEY,
    tabela VARCHAR(100) NOT NULL,     
    chave_natural BIGINT NOT NULL,     
    usuario NVARCHAR(128) NOT NULL,    
    operacao VARCHAR(10) NOT NULL,       
    data_execucao DATETIME2 NOT NULL DEFAULT SYSDATETIME()
);
GO
