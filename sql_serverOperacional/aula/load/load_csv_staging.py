# extract/load_csv_staging.py

import os
import logging
import pandas as pd
from sqlalchemy import text
from datetime import datetime


def limpar_staging(ano_censo, engine):
    """Remove dados do ano informado na staging."""
    logging.info("Limpando staging para ano %s...", ano_censo)
    with engine.begin() as conn:
        conn.execute(
            text("DELETE FROM stg.censo_escolar_matricula WHERE ano_censo = :ano"),
            {"ano": ano_censo}
        )
    logging.info("Staging limpa para ano %s.", ano_censo)


def carregar_csv_para_staging(path_csv, ano_censo, engine):
    """Carrega o CSV em chunks para a tabela staging.censo_escolar_matricula."""

    logging.info("Início da carga CSV → Staging. Arquivo: %s", path_csv)

    if not os.path.exists(path_csv):
        raise FileNotFoundError(f"Arquivo CSV inexistente: {path_csv}")

    # Colunas de interesse
    columns = [
        "NU_ANO_CENSO","SG_UF","CO_MUNICIPIO","NO_MUNICIPIO",
        "CO_ENTIDADE","NO_ENTIDADE","TP_DEPENDENCIA",
        "QT_MAT_INF","QT_MAT_FUND","QT_MAT_MED","QT_MAT_PROF"
    ]

    chunks = pd.read_csv(
        path_csv,
        sep=";",          # ajuste se necessário
        encoding="latin1",
        chunksize=100_000,
        low_memory=False
    )

    total = 0
    
    for i, chunk in enumerate(chunks, start=1):
        df = chunk[columns].copy()

        df.rename(columns={
            "NU_ANO_CENSO": "ano_censo",
            "SG_UF": "uf",
            "TP_DEPENDENCIA": "tp_rede"
        }, inplace=True)

        df_melt = df.melt(
            id_vars=[
                "ano_censo",
                "CO_ENTIDADE",
                "NO_ENTIDADE",
                "CO_MUNICIPIO",
                "NO_MUNICIPIO",
                "uf",
                "tp_rede"
            ],
            value_vars=[
                "QT_MAT_INF",
                "QT_MAT_FUND",
                "QT_MAT_MED",
                "QT_MAT_PROF"
            ],
            var_name="tp_etapa_ensino",
            value_name="qt_matricula"
        )

        etapa_map = {
            "QT_MAT_INF": 1,
            "QT_MAT_FUND": 2,
            "QT_MAT_MED": 3,
            "QT_MAT_PROF": 4
        }

        df_melt["tp_etapa_ensino"] = df_melt["tp_etapa_ensino"].map(etapa_map)

        df_melt = df_melt[df_melt["qt_matricula"].notna()]
        df_melt = df_melt[df_melt["qt_matricula"] > 0]

        df_final = df_melt.rename(columns={
            "CO_ENTIDADE": "co_entidade",
            "NO_ENTIDADE": "no_entidade",
            "CO_MUNICIPIO": "co_municipio"
        })[
            [
                "ano_censo",
                "co_entidade",
                "no_entidade",
                "co_municipio",
                "uf",
                "tp_rede",
                "tp_etapa_ensino",
                "qt_matricula"
            ]
        ]

        df_final.to_sql(
            "censo_escolar_matricula",
            schema="stg",
            con=engine,
            if_exists="append",
            index=False,
            chunksize=200
        )

        total += len(df_final)
        logging.info("Chunk %s carregado: %s linhas (total: %s)", i, len(df), total)

    logging.info("Carga para staging concluída. Total linhas: %s", total)