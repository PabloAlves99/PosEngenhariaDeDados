--CREATE DATABASE com distribuição entre múltiplos arquivos

CREATE DATABASE VendasFG
ON 
-- =======================================================
-- 1. FILEGROUP PRIMARY (metadata e objetos padrão)
-- =======================================================
PRIMARY
(
    NAME = VendasFG_Primary,
    FILENAME = 'C:\SQLDATA\VendasFG_Primary.mdf',
    SIZE = 50MB,
    FILEGROWTH = 10MB
),

-- =======================================================
-- 2. FILEGROUP SECUNDÁRIO (dados distribuídos)
-- =======================================================
FILEGROUP FG_DADOS
(
    NAME = VendasFG_Dados1,
    FILENAME = 'C:\SQLDATA\VendasFG_Dados1.ndf',
    SIZE = 100MB,
    FILEGROWTH = 50MB
),
(
    NAME = VendasFG_Dados2,
    FILENAME = 'C:\SQLDATA\VendasFG_Dados2.ndf',
    SIZE = 100MB,
    FILEGROWTH = 50MB
)

-- =======================================================
-- 3. ARQUIVO DE LOG
-- =======================================================
LOG ON
(
    NAME = VendasFG_Log,
    FILENAME = 'C:\SQLDATA\VendasFG_Log.ldf',
    SIZE = 50MB,
    FILEGROWTH = 20MB
);
GO


--Criando uma tabela apontando para o filegroup distribuído

USE VendasFG;
GO

CREATE TABLE vendas
(
    id          INT IDENTITY(1,1),
    produto     VARCHAR(100),
    quantidade  INT,
    valor       DECIMAL(10,2)
)
ON FG_DADOS;
GO

-- Inserindo carga para demonstrar a distribuição

INSERT INTO vendas (produto, quantidade, valor)
SELECT TOP (50000)
    CONCAT('produto_', ROW_NUMBER() OVER (ORDER BY (SELECT NULL))),
    ABS(CHECKSUM(NEWID())) % 100,
    (ABS(CHECKSUM(NEWID())) % 5000) / 3.0
FROM sys.all_objects a
CROSS JOIN sys.all_objects b;


-- Consultando distribuição dos dados entre os arquivos
SELECT 
    f.name AS Arquivo,
    f.physical_name,
    fsu.total_page_count * 8 / 1024 AS MB_Usados
FROM sys.dm_db_file_space_usage fsu
JOIN sys.database_files f 
    ON fsu.file_id = f.file_id
WHERE f.data_space_id =
    (SELECT data_space_id FROM sys.filegroups WHERE name = 'FG_DADOS');
