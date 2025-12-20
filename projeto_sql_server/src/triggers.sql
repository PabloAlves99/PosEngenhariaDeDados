CREATE OR ALTER TRIGGER stg.trg_validar_matricula
ON stg.censo_escolar_matricula
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO dw.log_matricula_invalida (
        co_entidade,
        co_municipio,
        tp_etapa_ensino,
        qt_matricula,
        dt_carga
    )
    SELECT
        i.co_entidade,
        i.co_municipio,
        i.tp_etapa_ensino,
        i.qt_matricula,
        SYSDATETIME()
    FROM inserted i
    WHERE i.qt_matricula <= 0;
END;
GO


CREATE OR ALTER TRIGGER dw.trg_auditoria_dim_escola
ON dw.dim_escola
AFTER INSERT, UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO dw.log_auditoria_dimensoes (
        tabela,
        chave_natural,
        usuario,
        operacao,
        data_execucao
    )
    SELECT
        'dim_escola' AS tabela,
        i.co_entidade AS chave_natural,
        SUSER_SNAME() AS usuario,
        CASE 
            WHEN d.co_entidade IS NULL THEN 'INSERT'
            ELSE 'UPDATE'
        END AS operacao,
        SYSDATETIME() AS data_execucao
    FROM inserted i
    LEFT JOIN deleted d
        ON i.sk_escola = d.sk_escola;
END;
GO
