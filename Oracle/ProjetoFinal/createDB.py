import oracledb
from data_generator.config import (
    MONGO_URI,
    DB_NAME,
    COLLECTION_NAME
)


# =========================
# CONFIGURAÇÃO DE CONEXÃO
# =========================
DB_CONFIG = {
    "user": "SEU_USUARIO",
    "password": "SUA_SENHA",
    "dsn": "HOST:PORT/SERVICE_NAME",  # Ex: localhost:1521/XEPDB1
}

# =========================
# LISTA DE DDLs
# =========================
DDL_COMMANDS = [

    # =========================
    # STAGING.STG_SALES
    # =========================
    """
CREATE TABLE STAGING.STG_SALES
(
    batch_id            NUMBER               NOT NULL,
    id_mongo            VARCHAR2(50)          NOT NULL,
    order_id            VARCHAR2(50),
    order_date_utc      TIMESTAMP,
    customer_id         VARCHAR2(50),
    customer_name       VARCHAR2(200),
    customer_email      VARCHAR2(200),
    customer_document   VARCHAR2(20),
    product_id          VARCHAR2(50),
    product_name        VARCHAR2(300),
    product_category    VARCHAR2(200),
    quantity            NUMBER(10),
    unit_price          NUMBER(12,2),
    discount_value      NUMBER(12,2),
    payment_method      VARCHAR2(50),
    payment_status      VARCHAR2(50),
    installments        NUMBER(3),
    shipping_city       VARCHAR2(100),
    shipping_state      VARCHAR2(50),
    shipping_country    VARCHAR2(50),
    shipping_value      NUMBER(12,2),
    load_datetime       TIMESTAMP DEFAULT SYSTIMESTAMP,
    source_system       VARCHAR2(30) DEFAULT 'MONGODB'
)
""",

    """
CREATE INDEX IDX_STG_SALES_ORDER_PROD
ON STAGING.STG_SALES (order_id, product_id)
""",

    """
CREATE INDEX IDX_STG_SALES_IDMONGO
ON STAGING.STG_SALES (id_mongo)
""",

    """
CREATE INDEX IDX_STG_SALES_ORDERDATE
ON STAGING.STG_SALES (order_date_utc)
""",

    # =========================
    # STAGING.ETL_EXECUTION_LOG
    # =========================
    """
CREATE TABLE STAGING.ETL_EXECUTION_LOG
(
    execution_id    NUMBER        NOT NULL,
    start_time      TIMESTAMP     DEFAULT SYSTIMESTAMP,
    end_time        TIMESTAMP,
    status          VARCHAR2(20),
    total_records   NUMBER,
    error_message   CLOB
)
""",

    """
ALTER TABLE STAGING.ETL_EXECUTION_LOG
ADD CONSTRAINT PK_ETL_EXECUTION_LOG
PRIMARY KEY (execution_id)
""",

    """
CREATE SEQUENCE STAGING.SEQ_ETL_EXECUTION_LOG
START WITH 1
INCREMENT BY 1
""",

    # =========================
    # DIM_CUSTOMER
    # =========================
    """
CREATE TABLE DW.DIM_CUSTOMER
(
    sk_customer     NUMBER        NOT NULL,
    bk_customer_id  VARCHAR2(30)  NOT NULL,
    name            VARCHAR2(200),
    email           VARCHAR2(200),
    document        VARCHAR2(20),
    dt_inicial      DATE          NOT NULL,
    dt_final        DATE,
    fl_ativo        CHAR(1)        NOT NULL
)
""",

    """
ALTER TABLE DW.DIM_CUSTOMER
ADD CONSTRAINT PK_DIM_CUSTOMER
PRIMARY KEY (sk_customer)
""",

    """
ALTER TABLE DW.DIM_CUSTOMER
ADD CONSTRAINT UK_DIM_CUSTOMER_BK
UNIQUE (bk_customer_id, dt_inicial)
""",

    # =========================
    # DIM_PRODUCT
    # =========================
    """
CREATE TABLE DW.DIM_PRODUCT
(
    sk_product      NUMBER        NOT NULL,
    bk_product_id   VARCHAR2(30)  NOT NULL,
    name            VARCHAR2(200),
    category        VARCHAR2(100),
    dt_inicial      DATE          NOT NULL,
    dt_final        DATE,
    fl_ativo        CHAR(1)        NOT NULL
)
""",

    """
ALTER TABLE DW.DIM_PRODUCT
ADD CONSTRAINT PK_DIM_PRODUCT
PRIMARY KEY (sk_product)
""",

    """
ALTER TABLE DW.DIM_PRODUCT
ADD CONSTRAINT UK_DIM_PRODUCT_BK
UNIQUE (bk_product_id, dt_inicial)
""",

    # =========================
    # DIM_DATE
    # =========================
    """
CREATE TABLE DW.DIM_DATE
(
    sk_date     NUMBER(8)   NOT NULL,
    date_value  DATE        NOT NULL,
    year        NUMBER(4),
    month       NUMBER(2),
    day         NUMBER(2)
)
""",

    """
ALTER TABLE DW.DIM_DATE
ADD CONSTRAINT PK_DIM_DATE
PRIMARY KEY (sk_date)
""",

    # =========================
    # FCT_SALES
    # =========================
    """
CREATE TABLE DW.FCT_SALES
(
    sk_sale         NUMBER        NOT NULL,
    sk_customer     NUMBER        NOT NULL,
    sk_product      NUMBER        NOT NULL,
    sk_order_date   NUMBER        NOT NULL,
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
""",

    """
ALTER TABLE DW.FCT_SALES
ADD CONSTRAINT PK_FCT_SALES
PRIMARY KEY (sk_sale)
""",

    """
ALTER TABLE DW.FCT_SALES
ADD CONSTRAINT FK_FCT_SALES_CUSTOMER
FOREIGN KEY (sk_customer)
REFERENCES DW.DIM_CUSTOMER (sk_customer)
""",

    """
ALTER TABLE DW.FCT_SALES
ADD CONSTRAINT FK_FCT_SALES_PRODUCT
FOREIGN KEY (sk_product)
REFERENCES DW.DIM_PRODUCT (sk_product)
""",

    """
ALTER TABLE DW.FCT_SALES
ADD CONSTRAINT FK_FCT_SALES_DATE
FOREIGN KEY (sk_order_date)
REFERENCES DW.DIM_DATE (sk_date)
"""
]

# =========================
# EXECUÇÃO
# =========================


def execute_ddls():
    connection = oracledb.connect(**DB_CONFIG)
    cursor = connection.cursor()

    for ddl in DDL_COMMANDS:
        try:
            cursor.execute(ddl)
            print("OK:", ddl.split("(")[0].strip())
        except oracledb.DatabaseError as e:
            error, = e.args
            print("ERRO:", error.message)

    connection.commit()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    execute_ddls()
