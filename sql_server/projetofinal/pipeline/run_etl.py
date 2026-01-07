import os
import pandas as pd
import pyodbc
from datetime import datetime

# Conexão com SQL Server
CONN_STR = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost,1433;"
    "DATABASE=master;"
    "UID=sa;"
    "PWD=SenhaForte123!;"
    "TrustServerCertificate=yes;"
)

# Caminho do CSV
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_file_path = os.path.join(BASE_DIR, "data", "PNAD_COVID.csv")

# Leitura do CSV
df = pd.read_csv(csv_file_path, sep=",", dtype=str)

# Conversão segura das colunas
df['NU_ANO'] = pd.to_numeric(df['Ano'], errors='coerce').astype('Int64')
df['NU_MES'] = pd.to_numeric(df['V1013'], errors='coerce').astype('Int64')
df['UF'] = df['UF']

df['CO_MUNICIPIO'] = pd.to_numeric(
    df['CAPITAL'], errors='coerce').fillna(0).astype('Int64')
df['ID_DOMICILIO'] = pd.to_numeric(
    df['V1008'], errors='coerce').fillna(0).astype('Int64')
df['ID_PESSOA'] = pd.to_numeric(
    df['A001'], errors='coerce').fillna(0).astype('Int64')

df['SEXO'] = df['A003']

df['IDADE'] = pd.to_numeric(df['A002'], errors='coerce').astype('Int64')

df['ESCOLARIDADE'] = pd.to_numeric(df['A005'].replace(
    {'9': None, '': None}), errors='coerce').astype('Int64')
df['OCUPACAO'] = pd.to_numeric(df['C007'].replace(
    {'9': None, '': None}), errors='coerce').astype('Int64')

# Tratamento seguro de rendimento


def parse_float(x):
    try:
        if pd.isna(x) or x in ["", "NA", "Ignorado"]:
            return None
        return float(str(x).replace(',', '.'))
    except:
        return None


df['RENDIMENTO'] = df['C01012'].apply(parse_float)

# Soma de sintomas (ignora valores inválidos e vazios)
sintoma_cols = ['B0011', 'B0012', 'B0013', 'B0014', 'B0015', 'B0016', 'B0017', 'B0018', 'B0019', 'B00110',
                'B00111', 'B00112']
df['SINTOMAS'] = df[sintoma_cols].apply(
    lambda row: sum(pd.to_numeric(row, errors='coerce').fillna(0).astype(int)), axis=1
)

df['INTERNADO'] = df['B005'].replace({'1': 'S', '2': 'N', '3': 'N', '9': None})
df['TESTE_COVID'] = df['B006'].replace({'1': 'S', '2': 'N', '9': None})
df['DT_CARGA'] = datetime.now()

cols_to_insert = ['NU_ANO', 'NU_MES', 'UF', 'CO_MUNICIPIO', 'ID_DOMICILIO', 'ID_PESSOA', 'SEXO', 'IDADE',
                  'ESCOLARIDADE', 'OCUPACAO', 'RENDIMENTO', 'SINTOMAS', 'INTERNADO', 'TESTE_COVID', 'DT_CARGA']

# Conexão e inserção no SQL Server
conn = pyodbc.connect(CONN_STR)
cursor = conn.cursor()

insert_sql = """
INSERT INTO staging.pnad_covid_pessoa
(NU_ANO, NU_MES, UF, CO_MUNICIPIO, ID_DOMICILIO, ID_PESSOA, SEXO, IDADE, ESCOLARIDADE, OCUPACAO,
 RENDIMENTO, SINTOMAS, INTERNADO, TESTE_COVID, DT_CARGA)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

# Loop de inserção com tratamento de tipos
for index, row in df.iterrows():
    values = []
    for col in cols_to_insert:
        val = row[col]
        if pd.isna(val):
            values.append(None)
        else:
            # Força tipos compatíveis
            if isinstance(val, (pd.Int64Dtype().type, int)):
                values.append(int(val))
            elif isinstance(val, (float,)):
                values.append(float(val))
            else:
                values.append(val)
    cursor.execute(insert_sql, tuple(values))

conn.commit()
cursor.close()
conn.close()
