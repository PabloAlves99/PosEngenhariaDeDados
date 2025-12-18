import oracledb

DB_CONFIG = {
    "user": "sys",
    "password": "oracle",
    "dsn": "localhost:1521/freepdb1",
    "mode": oracledb.SYSDBA
}


def create_dim_customer(cursor):
    cursor.execute("""CREATE TABLE DW.DIM_CUSTOMER (
                        sk_customer      NUMBER,
                        bk_customer_id   VARCHAR2(30),
                        name             VARCHAR2(200),
                        email            VARCHAR2(200),
                        document         VARCHAR2(20),
                        dt_inicial       DATE,
                        dt_final         DATE,
                        fl_ativo         CHAR(1),
                        CONSTRAINT PK_DIM_CUSTOMER
                            PRIMARY KEY (sk_customer)
                    )
                    """)


def create_dim_date(cursor):
    cursor.execute("""CREATE TABLE DW.DIM_DATE (
                        sk_date     NUMBER,
                        date_value  DATE,
                        year        NUMBER(4),
                        month       NUMBER(2),
                        day         NUMBER(2),
                        CONSTRAINT PK_DIM_DATE
                            PRIMARY KEY (sk_date)
                    )
                    """)


def create_dim_product(cursor):
    cursor.execute("""CREATE TABLE DW.DIM_PRODUCT (
                        sk_product     NUMBER,
                        bk_product_id  VARCHAR2(30),
                        name           VARCHAR2(200),
                        category       VARCHAR2(100),
                        dt_inicial     DATE,
                        dt_final       DATE,
                        fl_ativo       CHAR(1),
                        CONSTRAINT PK_DIM_PRODUCT
                            PRIMARY KEY (sk_product)
                    )
                    """)


def create_log(cursor):
    cursor.execute("""CREATE TABLE STAGING.ETL_EXECUTION_LOG (
                        execution_id   NUMBER,
                        start_time     TIMESTAMP DEFAULT SYSTIMESTAMP,
                        end_time       TIMESTAMP,
                        status         VARCHAR2(20),
                        total_records  NUMBER,
                        error_message  CLOB,
                        CONSTRAINT PK_ETL_EXECUTION_LOG
                            PRIMARY KEY (execution_id)
                    )
                   """)


def create_fct_sales(cursor):
    cursor.execute("""CREATE TABLE DW.FCT_SALES (
                        sk_sale           NUMBER,
                        sk_customer       NUMBER NOT NULL,
                        sk_product        NUMBER NOT NULL,
                        sk_order_date     NUMBER NOT NULL,
                        order_id          VARCHAR2(30),
                        quantity          NUMBER(10),
                        unit_price        NUMBER(12,2),
                        discount_value    NUMBER(12,2),
                        shipping_value    NUMBER(12,2),
                        gross_amount      NUMBER(12,2),
                        net_amount        NUMBER(12,2),
                        payment_method    VARCHAR2(30),
                        payment_status    VARCHAR2(30),
                        load_datetime     TIMESTAMP DEFAULT SYSTIMESTAMP,
                        CONSTRAINT PK_FCT_SALES
                            PRIMARY KEY (sk_sale),
                        CONSTRAINT FK_FCT_SALES_CUSTOMER
                            FOREIGN KEY (sk_customer)
                            REFERENCES DW.DIM_CUSTOMER (sk_customer),
                        CONSTRAINT FK_FCT_SALES_PRODUCT
                            FOREIGN KEY (sk_product)
                            REFERENCES DW.DIM_PRODUCT (sk_product),
                        CONSTRAINT FK_FCT_SALES_DATE
                            FOREIGN KEY (sk_order_date)
                            REFERENCES DW.DIM_DATE (sk_date)
                    )
                   """)


def create_stg_sales(cursor):
    cursor.execute("""CREATE TABLE STAGING.STG_SALES (
                        batch_id           NUMBER,
                        id_mongo           VARCHAR2(50),
                        order_id           VARCHAR2(50),
                        order_date_utc     TIMESTAMP,
                        customer_id        VARCHAR2(50),
                        customer_name      VARCHAR2(200),
                        customer_email     VARCHAR2(200),
                        customer_document  VARCHAR2(20),
                        product_id         VARCHAR2(50),
                        product_name       VARCHAR2(300),
                        product_category   VARCHAR2(200),
                        quantity           NUMBER(10),
                        unit_price         NUMBER(12,2),
                        discount_value     NUMBER(12,2),
                        payment_method     VARCHAR2(50),
                        payment_status     VARCHAR2(50),
                        installments       NUMBER(3),
                        shipping_city      VARCHAR2(100),
                        shipping_state     VARCHAR2(50),
                        shipping_country   VARCHAR2(50),
                        shipping_value     NUMBER(12,2),
                        load_datetime      TIMESTAMP DEFAULT SYSTIMESTAMP,
                        source_system      VARCHAR2(30) DEFAULT 'MONGODB'
                    )

                        """)

    cursor.execute("""
                        CREATE INDEX IDX_STG_SALES_ORDER_PROD
                        ON STAGING.STG_SALES (order_id, product_id)
                    """)

    cursor.execute("""
                        CREATE INDEX IDX_STG_SALES_IDMONGO
                        ON STAGING.STG_SALES (id_mongo)
                    """)

    cursor.execute("""
                        CREATE INDEX IDX_STG_SALES_ORDERDATE
                        ON STAGING.STG_SALES (order_date_utc)
                    """)


def bootstrap():
    conn = oracledb.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # STAGING
    create_stg_sales(cursor)
    create_log(cursor)

    # DIMENSÕES
    create_dim_date(cursor)
    create_dim_customer(cursor)
    create_dim_product(cursor)

    # FATO
    create_fct_sales(cursor)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    bootstrap()
