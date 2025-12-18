CREATE TABLE DW.FCT_SALES (
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
);
