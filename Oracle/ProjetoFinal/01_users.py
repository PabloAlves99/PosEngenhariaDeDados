import oracledb

DB_CONFIG = {
    "user": "sys",
    "password": "oracle",
    "dsn": "localhost:1521/freepdb1",
    "mode": oracledb.SYSDBA
}


def create_user(cursor, username, password):
    try:
        cursor.execute(f"CREATE USER {username} IDENTIFIED BY {password}")
        cursor.execute(
            f"GRANT CREATE SESSION, CREATE TABLE, CREATE SEQUENCE TO {username}")
        cursor.execute(f"ALTER USER {username} QUOTA UNLIMITED ON USERS")
        print(f"{username} criado com sucesso")

    except oracledb.DatabaseError as e:
        error, = e.args
        if error.code in (955, 1920):  # usuário já existe
            print(f"{username} já existe. Ignorado.")
        else:
            raise


def bootstrap():
    conn = oracledb.connect(**DB_CONFIG)
    cursor = conn.cursor()

    create_user(cursor, "STAGING", "staging")
    create_user(cursor, "DW", "dw")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    bootstrap()
