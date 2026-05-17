-- Criar Banco de Dados

CREATE DATABASE DW_Educacao;
GO

USE DW_Educacao;
GO

CREATE SCHEMA Staging;
GO

CREATE SCHEMA DW;
GO

-- Tabela Staging

CREATE TABLE Staging.Censo_Escolar_Matricula(
	[nu_ano_censo] [int] NOT NULL,
	[sg_uf] [varchar](20) NOT NULL,
	[co_municipio] [int] NOT NULL,
	[no_municipio] [varchar](250) NOT NULL,
	[co_entidade] [bigint] NOT NULL,
	[no_entidade] [varchar](250) NOT NULL,
	[tp_dependencia] [tinyint] NOT NULL,
	[qt_mat_inf] [int] NULL,
	[qt_mat_fund] [int] NULL,
	[qt_mat_med] [int] NULL,
	[qt_mat_prof] [int] NULL,
	[dt_carga] [datetime2](7) NULL
) ON [gp_staging]
GO

--TABELAS DE DIMENSÃO
CREATE TABLE dw.dim_tempo (
    sk_tempo INT IDENTITY(1,1) PRIMARY KEY,
    ano INT,
    mes TINYINT,
    dia TINYINT,
    dt_calendario DATE UNIQUE
);
GO

CREATE TABLE dw.dim_municipio (
    sk_municipio INT IDENTITY(1,1) PRIMARY KEY,
    co_municipio INT UNIQUE,
    uf CHAR(2),
    no_municipio VARCHAR(200)
);
GO

CREATE TABLE dw.dim_etapa_ensino (
    sk_etapa_ensino INT IDENTITY(1,1) PRIMARY KEY,
    tp_dependencia VARCHAR(100) NOT NULL
);
GO

CREATE TABLE dw.dim_escola (
    sk_escola INT IDENTITY(1,1) PRIMARY KEY,
    co_entidade BIGINT NOT NULL,
    no_entidade VARCHAR(200),
    co_municipio INT NOT NULL,
    tp_dependencia TINYINT,
    dt_inicio DATE NOT NULL,
    dt_fim DATE NOT NULL,
    fl_ativo CHAR(1) NOT NULL,
    CONSTRAINT uq_escola UNIQUE (co_entidade, fl_ativo)
);
GO

--TABELA FATO
CREATE TABLE dw.fact_matricula (
    sk_tempo INT,
    sk_escola INT,
    sk_municipio INT,
    sk_etapa_ensino INT,
    qt_matricula INT,
    dt_carga DATETIME2 DEFAULT SYSUTCDATETIME(),

    FOREIGN KEY (sk_tempo) REFERENCES dw.dim_tempo(sk_tempo),
    FOREIGN KEY (sk_escola) REFERENCES dw.dim_escola(sk_escola),
    FOREIGN KEY (sk_municipio) REFERENCES dw.dim_municipio(sk_municipio),
    FOREIGN KEY (sk_etapa_ensino) REFERENCES dw.dim_etapa_ensino(sk_etapa_ensino)
);
GO