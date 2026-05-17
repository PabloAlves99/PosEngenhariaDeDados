------------------------------------------------------------
-- PROJETO ETL & DATA WAREHOUSE - CENSO ESCOLAR (INEP)
-- SCRIPT ÚNICO COMPLETO
------------------------------------------------------------

-- 1. CRIAÇÃO DO BANCO

CREATE DATABASE DW_Educacao;
GO

USE DW_Educacao;
GO

-- 2. SCHEMAS
CREATE SCHEMA staging;
GO

CREATE SCHEMA dw;
GO

-- 3. TABELAS DE STAGING
CREATE TABLE staging.censo_escolar_matricula
(
	nu_ano_censo 	int 		 NOT NULL,
	sg_uf			varchar(20)  NOT NULL,
	co_municipio  	int  	  	 NOT NULL,
	no_municipio  	varchar(250) NOT NULL,
	co_entidade		bigint   NOT NULL,
	no_entidade		varchar(250) NOT NULL,
	tp_dependencia	tinyint  	 NOT NULL,
	qt_mat_inf		int		  	 NULL,
	qt_mat_fund		int		  	 NULL,
	qt_mat_med		int		  	 NULL,
	qt_mat_prof		int		  	 NULL,
    dt_carga 		DATETIME2 	 NOT NULL DEFAULT SYSUTCDATETIME()
);
GO

-- select * from staging.censo_escolar_matricula;


CREATE TABLE staging.log_execucao_etl
(
    id_execucao 	INT IDENTITY(1,1) PRIMARY KEY,
    processo 		VARCHAR(100),
    ano_censo 		INT,
    dt_inicio 		DATETIME2 DEFAULT SYSUTCDATETIME(),
    dt_fim 			DATETIME2,
    status_exec 	VARCHAR(20),
    mensagem_erro 	VARCHAR(4000)
);
GO

-- 4. TABELAS DE DIMENSÃO
CREATE TABLE dw.dim_tempo
(
    sk_tempo 		INT IDENTITY(1,1) PRIMARY KEY,
    ano 			INT,
    mes 			TINYINT,
    dia 			TINYINT,
    dt_calendario 	DATE UNIQUE
);
GO

CREATE TABLE dw.dim_municipio
(
    sk_municipio 	INT IDENTITY(1,1) PRIMARY KEY,
    co_municipio 	INT UNIQUE,
    uf 				CHAR(2),
    no_municipio 	VARCHAR(200)
);
GO

CREATE TABLE dw.dim_etapa_ensino
(
    sk_etapa_ensino INT IDENTITY(1,1) PRIMARY KEY,
    etapa_ensino 	VARCHAR(50) NOT NULL,
    descricao 		VARCHAR(200) NOT NULL
);
GO

CREATE TABLE dw.dim_escola
(
    sk_escola 		INT IDENTITY(1,1) PRIMARY KEY,
    co_entidade 	BIGINT NOT NULL,
    no_entidade 	VARCHAR(200),
    co_municipio 	INT NOT NULL,
    tp_rede 		TINYINT,
    dt_inicio 		DATE NOT NULL,
    dt_fim 			DATE NOT NULL,
    fl_ativo 		CHAR(1) NOT NULL,
    CONSTRAINT uq_escola UNIQUE (co_entidade, fl_ativo)
);
GO

-- 5. TABELA FATO
CREATE TABLE dw.fact_matricula
(
    sk_tempo 		INT NOT NULL,
    sk_escola 		INT NOT NULL,
    sk_municipio 	INT NOT NULL,
    sk_etapa_ensino INT NOT NULL,
    qt_matricula 	INT NOT NULL,
    dt_carga 		DATETIME2  NOT NULL DEFAULT SYSUTCDATETIME(),

    FOREIGN KEY (sk_tempo) REFERENCES dw.dim_tempo(sk_tempo),
    FOREIGN KEY (sk_escola) REFERENCES dw.dim_escola(sk_escola),
    FOREIGN KEY (sk_municipio) REFERENCES dw.dim_municipio(sk_municipio),
    FOREIGN KEY (sk_etapa_ensino) REFERENCES dw.dim_etapa_ensino(sk_etapa_ensino)
);
GO

-- 6. LOG DE INCONSISTÊNCIAS
CREATE TABLE dw.log_matricula_invalida
(
    id_log 				INT IDENTITY(1,1) PRIMARY KEY,
    sk_escola 			INT,
    sk_municipio 		INT,
    sk_etapa_ensino 	INT,
    qt_matricula 		INT,
    dt_carga 			DATETIME2,
    motivo 				VARCHAR(200),
    dt_log 				DATETIME2 DEFAULT SYSUTCDATETIME()
);
GO

-- 7. FUNCTIONS
CREATE OR ALTER FUNCTION dw.fn_normalizar_texto 
	(@texto NVARCHAR(4000))
RETURNS NVARCHAR(4000)
AS
BEGIN
    IF @texto IS NULL RETURN NULL;
    RETURN UPPER(LTRIM(RTRIM(@texto)));
END;
GO

-- 8. STORED PROCEDURES
CREATE OR ALTER PROCEDURE dw.usp_carregar_dim_tempo
    @ano INT
AS
BEGIN
    DECLARE @d DATE = DATEFROMPARTS(@ano,1,1);
    WHILE @d <= DATEFROMPARTS(@ano,12,31)
    BEGIN
        IF NOT EXISTS (SELECT 1
        FROM dw.dim_tempo
        WHERE dt_calendario=@d)
        INSERT INTO dw.dim_tempo
            (ano,mes,dia,dt_calendario)
        VALUES
            (YEAR(@d), MONTH(@d), DAY(@d), @d);
        SET @d = DATEADD(DAY,1,@d);
    END
END;
GO

CREATE OR ALTER PROCEDURE dw.usp_carregar_dim_municipio
    @ano INT
AS
BEGIN
    INSERT INTO dw.dim_municipio
        (co_municipio, no_municipio, uf)
    SELECT DISTINCT
        se.co_municipio,
        se.no_municipio,
        se.sg_uf
    FROM staging.censo_escolar_matricula se
    WHERE se.nu_ano_censo = @ano
        AND se.co_municipio NOT IN (SELECT co_municipio
        FROM dw.dim_municipio);
END;
GO


CREATE OR ALTER PROCEDURE dw.usp_carregar_dim_etapa_ensino
AS
BEGIN
    IF NOT EXISTS (SELECT 1
    FROM dw.dim_etapa_ensino)
    BEGIN
        INSERT INTO dw.dim_etapa_ensino
            (etapa_ensino, descricao)
        VALUES
            ('INFANTIL', 'Educação Infantil'),
            ('FUNDAMENTAL', 'Ensino Fundamental'),
            ('MEDIO', 'Ensino Médio'),
            ('PROFISSIONAL', 'Educação Profissional / Técnica');
    END
END;
GO

CREATE OR ALTER PROCEDURE dw.usp_dim_escola_scd2
    @ano INT
AS
BEGIN
    ;WITH
        base
        AS
        (
            SELECT DISTINCT
                co_entidade,
                no_entidade = dw.fn_normalizar_texto(no_entidade),
                co_municipio,
                tp_dependencia
            FROM staging.censo_escolar_matricula
            WHERE nu_ano_censo = @ano
        )
    MERGE dw.dim_escola AS tgt
    USING base AS src
       ON tgt.co_entidade = src.co_entidade
        AND tgt.fl_ativo = 'S'
    WHEN MATCHED AND (
            tgt.no_entidade <> src.no_entidade
        OR tgt.co_municipio <> src.co_municipio
        OR tgt.tp_rede <> src.tp_dependencia
    )
        THEN UPDATE SET
            fl_ativo = 'N',
            dt_fim = DATEFROMPARTS(@ano,12,31)
    WHEN NOT MATCHED BY TARGET
        THEN INSERT (co_entidade, no_entidade, co_municipio, tp_rede, dt_inicio, dt_fim, fl_ativo)
             VALUES (src.co_entidade, src.no_entidade, src.co_municipio,
                     src.tp_dependencia, DATEFROMPARTS(@ano,1,1), '9999-12-31', 'S');
END;
GO

CREATE OR ALTER PROCEDURE dw.usp_fact_matricula_load
    @ano INT
AS
BEGIN
    -- Limpar fato do ano
    DELETE f
      FROM dw.fact_matricula f
        JOIN dw.dim_tempo t ON t.sk_tempo = f.sk_tempo
     WHERE t.ano = @ano;

    INSERT INTO dw.fact_matricula
        (sk_tempo, sk_escola, sk_municipio, sk_etapa_ensino, qt_matricula)
    SELECT
        t.sk_tempo,
        e.sk_escola,
        m.sk_municipio,
        et.sk_etapa_ensino,
        x.qt_matricula
    FROM staging.censo_escolar_matricula se
        JOIN dw.dim_tempo t
        ON t.ano = se.nu_ano_censo AND t.mes = 1 AND t.dia = 1
        JOIN dw.dim_escola e
        ON e.co_entidade = se.co_entidade AND e.fl_ativo = 'S'
        JOIN dw.dim_municipio m
        ON m.co_municipio = se.co_municipio
    CROSS APPLY (
        VALUES
            ('INFANTIL', se.QT_MAT_INF),
            ('FUNDAMENTAL', se.QT_MAT_FUND),
            ('MEDIO', se.QT_MAT_MED),
            ('PROFISSIONAL', se.QT_MAT_PROF)
    ) AS x(etapa_ensino, qt_matricula)
        JOIN dw.dim_etapa_ensino et
        ON et.etapa_ensino = x.etapa_ensino
    WHERE se.nu_ano_censo = @ano
        AND x.qt_matricula > 0;
END;
GO

CREATE OR ALTER PROCEDURE staging.usp_limpar_staging_ano
    @ano INT
AS
BEGIN
    DELETE FROM staging.censo_escolar_matricula
    WHERE nu_ano_censo = @ano;
END;
GO

CREATE OR ALTER PROCEDURE dw.usp_processar_censo_escolar_ano
    @ano INT
AS
BEGIN
    SET NOCOUNT ON;

    EXEC dw.usp_carregar_dim_tempo        @ano;
    EXEC dw.usp_carregar_dim_municipio    @ano;
    EXEC dw.usp_carregar_dim_etapa_ensino;
    EXEC dw.usp_dim_escola_scd2           @ano;
    EXEC dw.usp_fact_matricula_load       @ano;
END;
GO

CREATE OR ALTER PROCEDURE dw.usp_reprocessar_ano
    @ano INT
AS
BEGIN
    EXEC staging.usp_limpar_staging_ano        @ano;
    -- Python recarrega a staging
    EXEC dw.usp_processar_censo_escolar_ano @ano;
END;
GO


