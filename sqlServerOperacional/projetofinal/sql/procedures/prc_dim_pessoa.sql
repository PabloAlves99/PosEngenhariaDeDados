CREATE OR ALTER PROCEDURE dw.prc_dim_pessoa
WITH EXECUTE AS OWNER
AS
BEGIN
    INSERT INTO dw.dim_pessoa (sexo, faixa_etaria, escolaridade)
    SELECT DISTINCT
        SEXO,
        CASE
            WHEN IDADE < 18 THEN '0-17'
            WHEN IDADE BETWEEN 18 AND 29 THEN '18-29'
            WHEN IDADE BETWEEN 30 AND 49 THEN '30-49'
            WHEN IDADE BETWEEN 50 AND 64 THEN '50-64'
            ELSE '65+'
        END,
        ESCOLARIDADE
    FROM staging.pnad_covid_pessoa s
    WHERE NOT EXISTS (
        SELECT 1
        FROM dw.dim_pessoa d
        WHERE d.sexo = s.SEXO
          AND d.escolaridade = s.ESCOLARIDADE
          AND d.faixa_etaria =
              CASE
                  WHEN s.IDADE < 18 THEN '0-17'
                  WHEN s.IDADE BETWEEN 18 AND 29 THEN '18-29'
                  WHEN s.IDADE BETWEEN 30 AND 49 THEN '30-49'
                  WHEN s.IDADE BETWEEN 50 AND 64 THEN '50-64'
                  ELSE '65+'
              END
    );
END;
