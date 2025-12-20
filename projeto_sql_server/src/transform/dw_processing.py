# transform/dw_processing.py

import logging
from sqlalchemy import text


def processar_dw(ano_censo: int, engine):
    """Executa a stored procedure principal no SQL Server."""

    logging.info("Iniciando processamento DW (SCD2 + Fato)...")

    with engine.begin() as conn:
        conn.execute(
            text("EXEC dw.usp_processar_censo_escolar_ano :ano"),
            {"ano": ano_censo}
        )

    logging.info("Processamento DW concluído para ano %s.", ano_censo)
