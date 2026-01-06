import pyodbc
from utils.config import (
    SQL_SERVER,
    SQL_DATABASE,
    SQL_USER,
    SQL_PASSWORD,
    SQL_DRIVER
)


def get_connection():
    connection_string = (
        f"DRIVER={{{SQL_DRIVER}}};"
        f"SERVER={SQL_SERVER};"
        f"DATABASE={SQL_DATABASE};"
        f"UID={SQL_USER};"
        f"PWD={SQL_PASSWORD};"
        "TrustServerCertificate=yes;"
    )

    conn = pyodbc.connect(connection_string)
    return conn
