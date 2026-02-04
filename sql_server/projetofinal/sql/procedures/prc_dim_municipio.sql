CREATE OR ALTER PROCEDURE dw.prc_dim_municipio
WITH EXECUTE AS OWNER
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO dw.dim_municipio (co_municipio, sg_uf, no_municipio)
    SELECT DISTINCT
        s.CO_MUNICIPIO,
        s.UF,
        NULL
    FROM staging.pnad_covid_pessoa s
    WHERE s.CO_MUNICIPIO IS NOT NULL
      AND NOT EXISTS (
          SELECT 1
          FROM dw.dim_municipio d
          WHERE d.co_municipio = s.CO_MUNICIPIO
      );
END;
GO
