CREATE TABLE DW.DIM_DATE (
    sk_date     NUMBER,
    date_value  DATE,
    year        NUMBER(4),
    month       NUMBER(2),
    day         NUMBER(2),
    CONSTRAINT PK_DIM_DATE
        PRIMARY KEY (sk_date)
);
