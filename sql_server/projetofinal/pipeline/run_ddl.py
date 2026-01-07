import os
import pyodbc

# Caminhos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STAGING_SQL = os.path.join(BASE_DIR, "sql", "staging.sql")
DW_SQL = os.path.join(BASE_DIR, "sql", "dw.sql")
# procedure = os.path.join(BASE_DIR, "sql", "usp_carregar_fato.sql")

# Conexão SQL Server
CONN_STR = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost,1433;"
    "DATABASE=master;"
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


def main():
    executar_sql(STAGING_SQL)
    executar_sql(DW_SQL)
    # executar_sql(procedure)


if __name__ == "__main__":
    main()
