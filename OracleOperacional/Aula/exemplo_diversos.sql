ALTER SESSION SET CURRENT_SCHEMA = HR;

CREATE SEQUENCE HR.depto_seq
	START WITH 901
	INCREMENT BY 1
	NOCACHE;

CREATE OR REPLACE PROCEDURE HR.add_dept (
	v_dept_name IN  HR.DEPARTMENTS.DEPARTMENT_NAME%TYPE, 
	v_dept_id   OUT HR.DEPARTMENTS.DEPARTMENT_ID%TYPE)
IS
BEGIN
	v_dept_id := HR.depto_seq.NEXTVAL;

	INSERT INTO HR.DEPARTMENTS(DEPARTMENT_ID, DEPARTMENT_NAME) 
    VALUES(v_dept_id, v_dept_name);	
END;

DECLARE
	v_dept_id NUMBER;
BEGIN
	HR.add_dept('TI 2', v_dept_id);
	DBMS_OUTPUT.PUT_LINE('Codigo departamento gerado: ' || v_dept_id);
END;

----------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE format_phone
	(p_phone_no IN OUT VARCHAR2) 
IS
	v_length NUMBER;
BEGIN
	v_length := LENGTH(p_phone_no);

	IF v_length = 10 THEN
		p_phone_no := '(' || SUBSTR(p_phone_no, 1, 2) || ')' || 
		                     SUBSTR(p_phone_no, 3, 4) || '-' || 
                             SUBSTR(p_phone_no, 7, 4);
	ELSIF v_length = 11 THEN
			p_phone_no := '(' || SUBSTR(p_phone_no, 1, 2) || ')' || 
		                         SUBSTR(p_phone_no, 3, 5) || '-' || 
                                 SUBSTR(p_phone_no, 8, 4);
	ELSE
		RAISE_APPLICATION_ERROR(-20002, 'Telefone deve conter 10 ou 11 dígitos.');
	END IF;

END format_phone;

DECLARE
	a_phone_no VARCHAR2(13);
BEGIN
	a_phone_no := '800633052275' ;
	format_phone(a_phone_no);
	DBMS_OUTPUT.PUT_LINE('The formatted number is: ' || a_phone_no);
END;

----------------------------------------------------------------------

DECLARE
	e_insert_excep EXCEPTION;
	PRAGMA EXCEPTION_INIT(e_insert_excep, -01400);

	v_error_code NUMBER;
	v_error_message VARCHAR2(255);
BEGIN
	INSERT INTO HR.departments
	(department_id, department_name)
	VALUES (280, NULL);
EXCEPTION
	WHEN e_insert_excep THEN
		v_error_code    := SQLCODE;
		v_error_message := SQLERRM;
		
		DBMS_OUTPUT.PUT_LINE(USER || '-' || SYSDATE);
		
		INSERT INTO HR.error_log(e_user, e_date, error_code, error_message)
		VALUES(USER, SYSDATE, v_error_code, v_error_message);	
END;



SELECT * FROM hr.employees;









