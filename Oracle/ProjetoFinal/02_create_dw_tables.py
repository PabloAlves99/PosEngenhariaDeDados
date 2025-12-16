import oracledb

# =========================
# CONEXÃO DW
# =========================
DB_CONFIG = {
    "user": "dw",
    "password": "dw",
    "dsn": "localhost:1521/freepdb1"
}


def safe_execute(cursor, ddl):
    try:
        cursor.execute(ddl)
        print("OK")
    except oracledb.DatabaseError as e:
        error, = e.args
        if error.code == 955:
            print("IGNORADO:", error.message)
        else:
            raise


def create_objects():
    conn = oracledb.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # =========================
    # DIM_CUSTOMER (SCD2)
    # =========================
    safe_execute(cursor, """
    CREATE TABLE DIM_CUSTOMER
    (
        sk_customer     NUMBER NOT NULL,
        bk_customer_id  VARCHAR2(30) NOT NULL,
        name            VARCHAR2(200),
        email           VARCHAR2(200),
        document        VARCHAR2(20),
        dt_inicial      DATE NOT NULL,
        dt_final        DATE,
        fl_ativo        CHAR(1) NOT NULL
    )
    """)

    safe_execute(cursor,
                 "ALTER TABLE DIM_CUSTOMER ADD CONSTRAINT PK_DIM_CUSTOMER PRIMARY KEY (sk_customer)"
                 )

    safe_execute(cursor, "CREATE SEQUENCE SEQ_DIM_CUSTOMER")

    # =========================
    # DIM_PRODUCT (SCD2)
    # =========================
    safe_execute(cursor, """
    CREATE TABLE DIM_PRODUCT
    (
        sk_product      NUMBER NOT NULL,
        bk_product_id   VARCHAR2(30) NOT NULL,
        name            VARCHAR2(200),
        category        VARCHAR2(100),
        dt_inicial      DATE NOT NULL,
        dt_final        DATE,
        fl_ativo        CHAR(1) NOT NULL
    )
    """)

    safe_execute(cursor,
                 "ALTER TABLE DIM_PRODUCT ADD CONSTRAINT PK_DIM_PRODUCT PRIMARY KEY (sk_product)"
                 )

    safe_execute(cursor, "CREATE SEQUENCE SEQ_DIM_PRODUCT")

    # =========================
    # DIM_DATE
    # =========================
    safe_execute(cursor, """
    CREATE TABLE DIM_DATE
    (
        sk_date     NUMBER(8) NOT NULL,
        date_value  DATE NOT NULL,
        year        NUMBER(4),
        month       NUMBER(2),
        day         NUMBER(2)
    )
    """)

    safe_execute(cursor,
                 "ALTER TABLE DIM_DATE ADD CONSTRAINT PK_DIM_DATE PRIMARY KEY (sk_date)"
                 )

    # =========================
    # FCT_SALES
    # =========================
    safe_execute(cursor, """
    CREATE TABLE FCT_SALES
    (
        sk_sale         NUMBER NOT NULL,
        sk_customer     NUMBER NOT NULL,
        sk_product      NUMBER NOT NULL,
        sk_order_date   NUMBER NOT NULL,
        order_id        VARCHAR2(30),
        quantity        NUMBER(10),
        unit_price      NUMBER(12,2),
        discount_value  NUMBER(12,2),
        shipping_value  NUMBER(12,2),
        gross_amount    NUMBER(12,2),
        net_amount      NUMBER(12,2),
        payment_method  VARCHAR2(30),
        payment_status  VARCHAR2(30),
        load_datetime   TIMESTAMP DEFAULT SYSTIMESTAMP
    )
    """)

    safe_execute(cursor,
                 "ALTER TABLE FCT_SALES ADD CONSTRAINT PK_FCT_SALES PRIMARY KEY (sk_sale)"
                 )

    safe_execute(cursor, "CREATE SEQUENCE SEQ_FCT_SALES")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_objects()
