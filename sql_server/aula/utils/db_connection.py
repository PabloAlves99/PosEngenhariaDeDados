# utils/db_connection.py

from sqlalchemy import create_engine
from urllib.parse import quote_plus
from utils.config import DB_CONFIG


def get_engine():
    user = DB_CONFIG["UID"]
    password = quote_plus(DB_CONFIG["PWD"])
    server = DB_CONFIG["SERVER"]
    database = DB_CONFIG["DATABASE"]
    driver = DB_CONFIG["DRIVER"].replace(" ", "+")

    conn_str = (
        f"mssql+pyodbc://{user}:{password}@{server}/{database}"
        f"?driver={driver}&Encrypt=no"
    )

    return create_engine(conn_str, fast_executemany=True)
