import os
import pandas as pd
import pyodbc
import numpy as np

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

# ---------- FUNÇÕES ----------


def read_csv(file_path):
    df = pd.read_csv(file_path, encoding='utf-8', sep=',')
    return df


def clean_data(df):
    """
    Limpeza e padronização básica:
    - Substituir valores ignorados por NaN
    - Converter colunas numéricas
    - Arredondar para 2 casas decimais
    """
    # Substituir ' ' ou campos vazios por NaN
    df.replace(['', ' '], pd.NA, inplace=True)

    # Colunas numéricas (exemplo, sua lista original)
    numeric_cols = [
        'Ano', 'UF', 'CAPITAL', 'V1008', 'V1012', 'V1013', 'V1016',
        'Estrato', 'UPA', 'V1022', 'V1023', 'V1030', 'V1031', 'V1032',
        'posest', 'A001', 'A001A', 'A001B1', 'A001B2', 'A001B3', 'A002', 'A003',
        'A004', 'A005', 'B0011', 'B0012', 'B0013', 'B0014', 'B0015', 'B0016', 'B0017',
        'B0018', 'B0019', 'B00110', 'B00111', 'B00112', 'B002', 'B0031', 'B0032', 'B0033',
        'B0034', 'B0035', 'B0036', 'B0037', 'B0041', 'B0042', 'B0043', 'B0044', 'B0045', 'B0046',
        'B005', 'B006', 'B007', 'C001', 'C002', 'C003', 'C004', 'C005', 'C0051', 'C0052', 'C0053',
        'C006', 'C007', 'C007A', 'C007B', 'C007C', 'C007D', 'C007E', 'C007E1', 'C007E2',
        'C008', 'C009', 'C010', 'C0101', 'C01011', 'C01012', 'C0102', 'C01021', 'C01022',
        'C0103', 'C0104', 'C011A', 'C011A1', 'C011A11', 'C011A12', 'C011A2', 'C011A21', 'C011A22',
        'C012', 'C013', 'C014', 'C015', 'C016', 'C017A', 'D0011', 'D0013', 'D0021', 'D0023',
        'D0031', 'D0033', 'D0041', 'D0043', 'D0051', 'D0053', 'D0061', 'D0063', 'D0071', 'D0073',
        'F001', 'F0021', 'F0022', 'F0061', 'F006'
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].round(2)  # Arredonda para 2 casas decimais

    return df


def load_to_sql(df, table_name, conn_str):
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Cria tabela se não existir
    col_defs = []
    for c in df.columns:
        if pd.api.types.is_numeric_dtype(df[c]):
            col_defs.append(f"[{c}] FLOAT")
        else:
            col_defs.append(f"[{c}] NVARCHAR(MAX)")
    create_table_sql = f"""
    IF OBJECT_ID('{table_name}', 'U') IS NULL
    CREATE TABLE {table_name} ({', '.join(col_defs)})
    """
    cursor.execute(create_table_sql)
    conn.commit()

    # Limpa staging
    cursor.execute(f"TRUNCATE TABLE {table_name}")
    conn.commit()

    # Converte NaN para None
    df = df.where(pd.notnull(df), None)

    # Inserção linha por linha (mais segura que executemany)
    placeholders = ", ".join(["?"] * len(df.columns))
    insert_sql = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({placeholders})"

    for idx, row in enumerate(df.itertuples(index=False, name=None), 1):
        try:
            cursor.execute(insert_sql, row)
        except Exception as e:
            print(f"Erro na linha {idx}: {e} -> {row}")

    conn.commit()
    cursor.close()
    conn.close()
    print(f"{len(df)} registros carregados na tabela {table_name}")


def etl_pipeline(csv_file, table_name, conn_str):
    print("Lendo CSV...")
    df = read_csv(csv_file)

    print("Limpando dados...")
    df = clean_data(df)

    print("Carregando para SQL Server...")
    load_to_sql(df, table_name, conn_str)

    print("ETL concluído com sucesso!")


# ---------- EXECUÇÃO ----------
if __name__ == "__main__":
    etl_pipeline(CSV_FILE, TABLE_STAGING, CONN_STR)
