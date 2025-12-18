CREATE TABLE STAGING.ETL_EXECUTION_LOG (
    execution_id   NUMBER,
    start_time     TIMESTAMP DEFAULT SYSTIMESTAMP,
    end_time       TIMESTAMP,
    status         VARCHAR2(20),
    total_records  NUMBER,
    error_message  CLOB,
    CONSTRAINT PK_ETL_EXECUTION_LOG
        PRIMARY KEY (execution_id)
);
