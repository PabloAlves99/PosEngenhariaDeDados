CREATE OR ALTER PROCEDURE dw.prc_dim_tempo
WITH EXECUTE AS OWNER
AS
BEGIN
    INSERT INTO dw.dim_tempo (nu_ano, nu_mes, no_mes)
    SELECT DISTINCT
        NU_ANO,
        NU_MES,
        DATENAME(MONTH, DATEFROMPARTS(NU_ANO, NU_MES, 1))
    FROM staging.pnad_covid_pessoa s
    WHERE NOT EXISTS (
        SELECT 1
        FROM dw.dim_tempo d
        WHERE d.nu_ano = s.NU_ANO
          AND d.nu_mes = s.NU_MES
    );
END;
