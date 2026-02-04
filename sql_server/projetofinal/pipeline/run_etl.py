import os
import math
import pandas as pd
import pyodbc
from datetime import datetime

# ---------- CONFIGURAÇÃO ----------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_FILE = os.path.join(BASE_DIR, "data", "PNAD_COVID.csv")
TABLE_STAGING = "stg_pnad_covid"

CONN_STR = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost,1433;"
    "DATABASE=pnad_covid_dw;"
    "UID=sa;"
    "PWD=SenhaForte123!;"
    "TrustServerCertificate=yes;"
)

# ---------- FUNÇÕES DE CONVERSÃO ----------


def is_null(v):
    return (
        v is None
        or (isinstance(v, float) and math.isnan(v))
        or str(v).strip() == ""
    )


def to_int(v):
    return None if is_null(v) else int(float(v))


def to_bigint(v):
    return None if is_null(v) else int(float(v))


def to_char(v, size):
    return None if is_null(v) else str(v).strip()[:size]


def to_decimal(v):
    return None if is_null(v) else round(float(v), 2)

# ---------- REGRA DE SINTOMAS ----------


def calcula_sintomas(row):
    sintomas = [
        "B0011", "B0012", "B0013", "B0014", "B0015", "B0016",
        "B0017", "B0018", "B0019", "B00110", "B00111", "B00112"
    ]
    return sum(
        1 for c in sintomas
        if c in row and not is_null(row[c]) and str(row[c]) == "1"
    )

# ---------- ETL ----------


def etl_pipeline():
    print("Lendo CSV...")
    df = pd.read_csv(CSV_FILE, sep=",", dtype=str, low_memory=False)

    registros = []

    print("Transformando dados...")
    for _, row in df.iterrows():
        registros.append((
            to_int(row.get("Ano")),          # NU_ANO
            to_int(row.get("V1013")),        # NU_MES
            to_char(row.get("UF"), 2),       # UF
            to_int(row.get("CAPITAL")),      # CO_MUNICIPIO
            to_bigint(row.get("V1008")),     # ID_DOMICILIO
            to_bigint(row.get("A001")),      # ID_PESSOA
            to_char(row.get("A003"), 1),     # SEXO
            to_int(row.get("A002")),         # IDADE
            to_int(row.get("A005")),         # ESCOLARIDADE
            to_int(row.get("C007C")),        # OCUPACAO
            to_decimal(row.get("C01012")),   # RENDIMENTO
            calcula_sintomas(row),           # SINTOMAS
            to_char(row.get("B005"), 1),     # INTERNADO
            to_char(row.get("A001A"), 1),    # TESTE_COVID
            datetime.now()                   # DT_CARGA
        ))

    print("Conectando ao SQL Server...")
    conn = pyodbc.connect(CONN_STR)
    cursor = conn.cursor()
    cursor.fast_executemany = True

    print("Limpando staging...")
    cursor.execute(f"TRUNCATE TABLE {TABLE_STAGING}")
    conn.commit()

    insert_sql = """
        INSERT INTO staging.pnad_covid_pessoa (
            NU_ANO,
            NU_MES,
            UF,
            CO_MUNICIPIO,
            ID_DOMICILIO,
            ID_PESSOA,
            SEXO,
            IDADE,
            ESCOLARIDADE,
            OCUPACAO,
            RENDIMENTO,
            SINTOMAS,
            INTERNADO,
            TESTE_COVID,
            DT_CARGA
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

    print("Carregando dados na staging...")
    cursor.executemany(insert_sql, registros)

    conn.commit()
    cursor.close()
    conn.close()

    print("ETL concluído com sucesso.")


# ---------- EXECUÇÃO ----------
if __name__ == "__main__":
    etl_pipeline()
