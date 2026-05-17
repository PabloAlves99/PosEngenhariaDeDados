CREATE TABLE DW.DIM_PRODUCT (
    sk_product     NUMBER,
    bk_product_id  VARCHAR2(30),
    name           VARCHAR2(200),
    category       VARCHAR2(100),
    dt_inicial     DATE,
    dt_final       DATE,
    fl_ativo       CHAR(1),
    CONSTRAINT PK_DIM_PRODUCT
        PRIMARY KEY (sk_product)
);
