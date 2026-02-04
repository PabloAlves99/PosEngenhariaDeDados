import pyodbc

# ---------- CONFIGURAÇÃO ----------
CONN_STR = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost,1433;"
    "DATABASE=pnad_covid_dw;"
    "UID=sa;"
    "PWD=SenhaForte123!;"
    "TrustServerCertificate=yes;"
)

PROCEDURES = [
    "dw.prc_dim_municipio",
    "dw.prc_dim_pessoa",
    "dw.prc_dim_tempo",
    "dw.prc_fato_pnad_covid"
]

# ---------- EXECUÇÃO ----------


def run_procedures():
    conn = pyodbc.connect(CONN_STR)
    cursor = conn.cursor()

    for proc in PROCEDURES:
        print(f"EXEC {proc}")
        cursor.execute(f"EXEC {proc}")
        conn.commit()

    cursor.close()
    conn.close()


if __name__ == "__main__":
    run_procedures()
