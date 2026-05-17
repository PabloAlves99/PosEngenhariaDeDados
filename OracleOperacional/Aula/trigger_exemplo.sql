--  Criar tabela de auditoria

CREATE TABLE hr.log_employees (
    log_id           NUMBER PRIMARY KEY,
    EMPLOYEE_ID        NUMBER NOT NULL,
    usuario          VARCHAR2(50) NOT NULL,
    data_alteracao   DATE NOT NULL,
    SALARY_OLD     NUMBER(10,2),
    SALARY_NEW       NUMBER(10,2)
);

--  Criar sequence para identificação

CREATE SEQUENCE hr.seq_log_employees
    START WITH 1
    INCREMENT BY 1
    NOCACHE;

-- Criar Trigger para gerar ID

CREATE OR REPLACE TRIGGER hr.trg_log_employees_pk
BEFORE INSERT ON hr.log_employees
FOR EACH ROW
BEGIN
    IF :NEW.log_id IS NULL THEN
        :NEW.log_id := hr.seq_log_employees.NEXTVAL;
    END IF;
END;

-- Criar Trigger de auditoria

CREATE OR REPLACE TRIGGER hr.trg_auditoria_employees
AFTER UPDATE ON hr.employees
FOR EACH ROW
BEGIN
    INSERT INTO hr.log_employees
    (EMPLOYEE_ID, usuario, data_alteracao, SALARY_OLD, SALARY_NEW)
    VALUES
    (:OLD.EMPLOYEE_ID, USER, SYSDATE, :OLD.SALARY, :NEW.SALARY);
END;


-- Testes

SELECT * FROM HR.employees WHERE EMPLOYEE_ID  =  100;
SELECT *  FROM HR.LOG_EMPLOYEES;
UPDATE HR.employees SET salary = 19000 WHERE EMPLOYEE_ID  =  100;

