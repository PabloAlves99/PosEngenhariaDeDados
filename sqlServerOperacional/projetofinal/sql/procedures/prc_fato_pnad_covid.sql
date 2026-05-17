CREATE OR ALTER PROCEDURE dw.prc_fato_pnad_covid
WITH EXECUTE AS OWNER
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO dw.fato_pnad_covid
    (
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
        MAX(s.OCUPACAO)        AS ocupacao,
        AVG(s.RENDIMENTO)     AS rendimento,
        SUM(s.SINTOMAS)       AS sintomas,
        MAX(s.INTERNADO)      AS internado,
        MAX(s.TESTE_COVID)    AS teste_covid
    FROM staging.pnad_covid_pessoa s
    JOIN dw.dim_tempo t
        ON t.nu_ano = s.NU_ANO
       AND t.nu_mes = s.NU_MES
    JOIN dw.dim_municipio m
        ON m.co_municipio = s.CO_MUNICIPIO
    JOIN dw.dim_pessoa p
        ON p.sexo = s.SEXO
       AND p.escolaridade = s.ESCOLARIDADE
       AND p.faixa_etaria =
           CASE
               WHEN s.IDADE < 18 THEN '0-17'
               WHEN s.IDADE BETWEEN 18 AND 29 THEN '18-29'
               WHEN s.IDADE BETWEEN 30 AND 49 THEN '30-49'
               WHEN s.IDADE BETWEEN 50 AND 64 THEN '50-64'
               ELSE '65+'
           END
    WHERE NOT EXISTS (
        SELECT 1
        FROM dw.fato_pnad_covid f
        WHERE f.sk_tempo = t.sk_tempo
          AND f.sk_municipio = m.sk_municipio
          AND f.sk_pessoa = p.sk_pessoa
    )
    GROUP BY
        t.sk_tempo,
        m.sk_municipio,
        p.sk_pessoa;
END;
GO
