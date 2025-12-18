CREATE TABLE STAGING.STG_SALES (
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
);

CREATE INDEX IDX_STG_SALES_ORDER_PROD
ON STAGING.STG_SALES (
    order_id,
    product_id
);

CREATE INDEX IDX_STG_SALES_IDMONGO
ON STAGING.STG_SALES (
    id_mongo
);

CREATE INDEX IDX_STG_SALES_ORDERDATE
ON STAGING.STG_SALES (
    order_date_utc
);
