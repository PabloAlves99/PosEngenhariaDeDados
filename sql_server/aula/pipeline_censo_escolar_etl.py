# pipeline_censo_escolar_etl.py

from utils.logger import setup_logging
from utils.db_connection import get_engine
from utils.config import ANO_CENSO_DEFAULT, PATH_CSV
from load.load_csv_staging import limpar_staging, carregar_csv_para_staging
from transform.dw_processing import processar_dw

import logging


def executar_pipeline():
    setup_logging()
    logging.info("======= INÍCIO DO PIPELINE CENSO ESCOLAR =======")

    engine = get_engine()
    logging.info("Conexão com SQL Server estabelecida.")

    limpar_staging(ANO_CENSO_DEFAULT, engine)

    carregar_csv_para_staging(PATH_CSV, ANO_CENSO_DEFAULT, engine)
    
    processar_dw(ANO_CENSO_DEFAULT, engine)

    logging.info("======= PIPELINE FINALIZADO COM SUCESSO =======")

if __name__ == "__main__":
    executar_pipeline()
