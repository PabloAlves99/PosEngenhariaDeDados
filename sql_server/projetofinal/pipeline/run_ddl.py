import os
import pyodbc

# Caminhos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STAGING_SQL = os.path.join(BASE_DIR, "sql", "staging.sql")
DW_SQL = os.path.join(BASE_DIR, "sql", "dw.sql")
PROCEDURES_SQL = os.path.join(BASE_DIR, "sql", "procedures.sql")

# Conexão SQL Server
CONN_STR = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost,1433;"
    "DATABASE=pnad_covid_dw;"
    "UID=sa;"
    "PWD=SenhaForte123!;"
    "TrustServerCertificate=yes;"
)


def executar_sql(arquivo_sql):
    with open(arquivo_sql, "r", encoding="utf-8") as f:
        script = f.read()

    comandos = [cmd.strip() for cmd in script.split("GO") if cmd.strip()]

    conn = pyodbc.connect(CONN_STR)
    cursor = conn.cursor()

    for comando in comandos:
        cursor.execute(comando)

    conn.commit()
    cursor.close()
    conn.close()


def executar_procedure(arquivo_sql):
    with open(arquivo_sql, "r", encoding="utf-8") as f:
        script = f.read()

    conn = pyodbc.connect(CONN_STR)
    cursor = conn.cursor()

    cursor.execute(script)

    conn.commit()
    cursor.close()
    conn.close()


def main():
    executar_sql(STAGING_SQL)
    executar_sql(DW_SQL)
    executar_procedure("sql/procedures/prc_dim_tempo.sql")
    executar_procedure("sql/procedures/prc_dim_municipio.sql")
    executar_procedure("sql/procedures/prc_dim_pessoa.sql")
    executar_procedure("sql/procedures/prc_fato_pnad_covid.sql")


if __name__ == "__main__":
    main()
