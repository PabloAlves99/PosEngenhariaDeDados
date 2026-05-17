CREATE OR ALTER FUNCTION dw.fn_normalizar_texto (
    @texto VARCHAR(200)
)
RETURNS VARCHAR(200)
AS
BEGIN
    IF @texto IS NULL
        RETURN NULL;

    RETURN UPPER(LTRIM(RTRIM(
        TRANSLATE(
            @texto,
            'аюбцихймлнсртузышгАЮБЦИХЙМЛНСРТУЗЫШГ',
            'AAAAEEEIIIOOOOUUUCaaaaeeeiiioooouuuc'
        )
    )));
END;
GO
