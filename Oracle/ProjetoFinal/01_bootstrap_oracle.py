import oracledb

# =========================
# CONEXÃO SYSDBA
# =========================
DB_CONFIG = {
    "user": "sys",
    "password": "oracle",
    "dsn": "localhost:1521/freepdb1",
    "mode": oracledb.SYSDBA
}


def safe_execute(cursor, sql):
    try:
        cursor.execute(sql)
        print("OK")
    except oracledb.DatabaseError as e:
        error, = e.args
        if error.code in (955, 1920):
            print("IGNORADO:", error.message)
        else:
            raise


def bootstrap():
    conn = oracledb.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # =========================
    # USUÁRIO STAGING
    # =========================
    safe_execute(cursor, """
    BEGIN
        EXECUTE IMMEDIATE 'CREATE USER STAGING IDENTIFIED BY staging';
    EXCEPTION
        WHEN OTHERS THEN
            IF SQLCODE != -1920 THEN RAISE; END IF;
    END;
    """)

    safe_execute(cursor, """
    GRANT CREATE SESSION, CREATE TABLE, CREATE SEQUENCE
    TO STAGING
    """)

    # =========================
    # USUÁRIO DW
    # =========================
    safe_execute(cursor, """
    BEGIN
        EXECUTE IMMEDIATE 'CREATE USER DW IDENTIFIED BY dw';
    EXCEPTION
        WHEN OTHERS THEN
            IF SQLCODE != -1920 THEN RAISE; END IF;
    END;
    """)

    safe_execute(cursor, """
    GRANT CREATE SESSION, CREATE TABLE, CREATE SEQUENCE
    TO DW
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    bootstrap()
