CREATE OR ALTER PROCEDURE DW.sp_carga_municipio 
	@ano_censo INT
AS
BEGIN
	MERGE [DW].[dim_municipio] AS tgt
	USING (
		SELECT DISTINCT
			   co_municipio,
			   no_municipio,
			   sg_uf
		FROM [Staging].[Censo_Escolar_Matricula]
		WHERE nu_ano_censo = @ano_censo
	) AS src
		ON tgt.co_municipio = src.co_municipio
	WHEN NOT MATCHED BY TARGET THEN
		INSERT (co_municipio, no_municipio, uf)
		VALUES (src.co_municipio, src.no_municipio, src.sg_uf);
END;
GO

CREATE OR ALTER PROCEDURE DW.sp_carga_etapa_ensino 
AS
BEGIN
	INSERT INTO DW.dim_etapa_ensino (tp_dependencia, ds_dependencia) 
	VALUES (1, 'Educação Infantil'),
		   (2, 'Ensino Fundamental'),
		   (3, 'Ensino Médio'),
		   (4, 'Educação Profissional');
END;
GO

CREATE OR ALTER PROCEDURE DW.sp_processar_censo
	@ano_censo INT
AS
BEGIN
	EXEC DW.sp_carga_municipio @ano_censo;
	EXEC DW.sp_carga_etapa_ensino @ano_censo;
	--EXEC DW.sp_carga_escola @ano_censo;
	--EXEC DW.sp_carga_fato @ano_censo;
END