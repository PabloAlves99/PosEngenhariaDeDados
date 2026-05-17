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


CREATE TABLE hr.error_log (
	e_user	VARCHAR2(100), 
	e_date  DATE, 
	error_code NUMBER, 
	error_message VARCHAR2(255)
);

SELECT * FROM hr.error_log;
