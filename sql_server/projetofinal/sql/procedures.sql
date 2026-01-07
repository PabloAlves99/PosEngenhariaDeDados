CREATE PROCEDURE usp_carregar_dim_municipio
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO dw.dim_municipio (co_municipio, sg_uf, no_municipio)
    SELECT DISTINCT
        CO_MUNICIPIO,
        UF,
        '' -- não há coluna de nome de município na staging, manter vazio ou preencher manualmente
    FROM staging.pnad_covid_pessoa s
    WHERE NOT EXISTS (
        SELECT 1
        FROM dw.dim_municipio d
        WHERE d.co_municipio = s.CO_MUNICIPIO
    );
END;

CREATE PROCEDURE usp_carregar_dim_pessoa
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO dw.dim_pessoa (sexo, faixa_etaria, escolaridade)
    SELECT DISTINCT
        UPPER(SEXO) AS sexo,
        dbo.fn_faixa_etaria(IDADE) AS faixa_etaria,
        ESCOLARIDADE
    FROM staging.pnad_covid_pessoa s
    WHERE NOT EXISTS (
        SELECT 1
        FROM dw.dim_pessoa d
        WHERE d.sexo = UPPER(s.SEXO)
          AND d.faixa_etaria = dbo.fn_faixa_etaria(s.IDADE)
          AND d.escolaridade = s.ESCOLARIDADE
    );
END;

CREATE PROCEDURE usp_carregar_dim_tempo
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO dw.dim_tempo (nu_ano, nu_mes, no_mes)
    SELECT DISTINCT
        NU_ANO,
        NU_MES,
        DATENAME(MONTH, DATEFROMPARTS(NU_ANO, NU_MES, 1)) AS no_mes
    FROM staging.pnad_covid_pessoa s
    WHERE NOT EXISTS (
        SELECT 1
        FROM dw.dim_tempo d
        WHERE d.nu_ano = s.NU_ANO
          AND d.nu_mes = s.NU_MES
    );
END;

CREATE PROCEDURE usp_carregar_fato
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO dw.fato_pnad_covid (
        sk_tempo,
        sk_municipio,
        sk_pessoa,
        ocupacao,
        rendimento,
        sintomas,
        internado,
        teste_covid
    )
    SELECT
        t.sk_tempo,
        m.sk_municipio,
        p.sk_pessoa,
        s.OCUPACAO,
        s.RENDIMENTO,
        s.SINTOMAS,
        s.INTERNADO,
        s.TESTE_COVID
    FROM staging.pnad_covid_pessoa s
    INNER JOIN dw.dim_tempo t
        ON t.nu_ano = s.NU_ANO
       AND t.nu_mes = s.NU_MES
    INNER JOIN dw.dim_municipio m
        ON m.co_municipio = s.CO_MUNICIPIO
    INNER JOIN dw.dim_pessoa p
        ON p.sexo = UPPER(s.SEXO)
       AND p.faixa_etaria = dbo.fn_faixa_etaria(s.IDADE)
       AND p.escolaridade = s.ESCOLARIDADE
    WHERE NOT EXISTS (
        SELECT 1
        FROM dw.fato_pnad_covid f
        WHERE f.sk_tempo = t.sk_tempo
          AND f.sk_municipio = m.sk_municipio
          AND f.sk_pessoa = p.sk_pessoa
    );
END;
