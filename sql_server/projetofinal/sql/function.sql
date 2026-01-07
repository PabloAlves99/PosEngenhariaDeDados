CREATE FUNCTION dbo.fn_normalizar_texto(@texto VARCHAR(150))
RETURNS VARCHAR(150)
AS
BEGIN
    DECLARE @resultado VARCHAR(150);

    -- Remove espaços extras
    SET @resultado = LTRIM(RTRIM(@texto));

    -- Converte para Title Case
    DECLARE @i INT = 1;
    DECLARE @letra CHAR(1);
    DECLARE @novoTexto VARCHAR(150) = '';
    DECLARE @maiuscula BIT = 1;

    WHILE @i <= LEN(@resultado)
    BEGIN
        SET @letra = SUBSTRING(@resultado, @i, 1);

        IF @maiuscula = 1
            SET @novoTexto = @novoTexto + UPPER(@letra);
        ELSE
            SET @novoTexto = @novoTexto + LOWER(@letra);

        -- Próxima letra será maiúscula se a letra atual for espaço
        SET @maiuscula = CASE WHEN @letra = ' ' THEN 1 ELSE 0 END;

        SET @i = @i + 1;
    END

    RETURN @novoTexto;
END;


CREATE FUNCTION dbo.fn_faixa_etaria(@idade INT)
RETURNS VARCHAR(30)
AS
BEGIN
    DECLARE @faixa VARCHAR(30);

    IF @idade BETWEEN 0 AND 17
        SET @faixa = 'Criança / Adolescente';
    ELSE IF @idade BETWEEN 18 AND 29
        SET @faixa = 'Jovem Adulto';
    ELSE IF @idade BETWEEN 30 AND 59
        SET @faixa = 'Adulto';
    ELSE IF @idade >= 60
        SET @faixa = 'Idoso';
    ELSE
        SET @faixa = 'Não informado';

    RETURN @faixa;
END;

