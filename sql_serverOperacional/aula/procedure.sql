CREATE OR ALTER PROCEDURE dw.usp_processar_censo_escolar_ano
    @ano INT
AS
BEGIN
    SET NOCOUNT ON;

    IF NOT EXISTS (
        SELECT 1
        FROM dw.dim_tempo
        WHERE ano = @ano
          AND mes = 1
          AND dia = 1
    )
    BEGIN
        INSERT INTO dw.dim_tempo (ano, mes, dia, dt_calendario)
        VALUES (@ano, 1, 1, DATEFROMPARTS(@ano, 1, 1));
    END;

    BEGIN
        INSERT INTO dw.dim_municipio (co_municipio, uf, nome_municipio)
        SELECT DISTINCT
            s.co_municipio,
            CASE
                WHEN s.uf IN ('AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT',
                              'MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO',
                              'RR','SC','SP','SE','TO')
                THEN s.uf
                ELSE 'XX'
            END,
            CONCAT('MUNICIPIO ', s.co_municipio)
        FROM stg.censo_escolar_matricula s
        LEFT JOIN dw.dim_municipio d
            ON d.co_municipio = s.co_municipio
        WHERE s.ano_censo = @ano
          AND d.co_municipio IS NULL;
    END;

    BEGIN
        INSERT INTO dw.dim_etapa_ensino (tp_etapa_ensino, ds_etapa_ensino)
        SELECT DISTINCT
            s.tp_etapa_ensino,
            CONCAT('ETAPA ', s.tp_etapa_ensino)
        FROM stg.censo_escolar_matricula s
        LEFT JOIN dw.dim_etapa_ensino d
            ON d.tp_etapa_ensino = s.tp_etapa_ensino
        WHERE s.ano_censo = @ano
          AND d.sk_etapa_ensino IS NULL;
    END;

    BEGIN
        UPDATE d
        SET d.dt_fim = CAST(GETDATE() AS DATE),
            d.fl_ativo = 'N'
        FROM dw.dim_escola d
        JOIN stg.censo_escolar_matricula s
          ON d.co_entidade = s.co_entidade
        WHERE s.ano_censo = @ano
          AND d.fl_ativo = 'S'
          AND d.no_entidade <> dw.fn_normalizar_texto(s.no_entidade);

        INSERT INTO dw.dim_escola (
            co_entidade,
            no_entidade,
            co_municipio,
            tp_rede,
            dt_inicio,
            dt_fim,
            fl_ativo
        )
        SELECT DISTINCT
            s.co_entidade,
            dw.fn_normalizar_texto(s.no_entidade),
            s.co_municipio,
            s.tp_rede,
            CAST(GETDATE() AS DATE),
            NULL,
            'S'
        FROM stg.censo_escolar_matricula s
        LEFT JOIN dw.dim_escola d
            ON d.co_entidade = s.co_entidade
           AND d.fl_ativo = 'S'
        WHERE s.ano_censo = @ano
          AND (d.co_entidade IS NULL
               OR d.no_entidade <> dw.fn_normalizar_texto(s.no_entidade));
    END;

    BEGIN
        INSERT INTO dw.fact_matricula (
            sk_tempo,
            sk_escola,
            sk_municipio,
            sk_etapa_ensino,
            qt_matricula,
            dt_carga
        )
        SELECT
            t.sk_tempo,
            e.sk_escola,
            m.sk_municipio,
            et.sk_etapa_ensino,
            SUM(s.qt_matricula),
            SYSDATETIME()
        FROM stg.censo_escolar_matricula s
        JOIN dw.dim_tempo t
            ON t.ano = s.ano_censo
           AND t.mes = 1
           AND t.dia = 1
        JOIN dw.dim_escola e
            ON e.co_entidade = s.co_entidade
           AND e.fl_ativo = 'S'
        JOIN dw.dim_municipio m
            ON m.co_municipio = s.co_municipio
        JOIN dw.dim_etapa_ensino et
            ON et.tp_etapa_ensino = s.tp_etapa_ensino
        WHERE s.ano_censo = @ano
        GROUP BY
            t.sk_tempo,
            e.sk_escola,
            m.sk_municipio,
            et.sk_etapa_ensino;
    END;

END;
GO
