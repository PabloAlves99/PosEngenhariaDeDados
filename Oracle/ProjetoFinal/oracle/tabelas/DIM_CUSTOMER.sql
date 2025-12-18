CREATE TABLE DW.DIM_CUSTOMER (
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
);
