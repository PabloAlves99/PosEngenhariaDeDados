DECLARE
	TYPE dept_info_type IS RECORD (
		department_id   hr.departments.department_id%TYPE,
		department_name hr.departments.department_name%TYPE);
	
	TYPE emp_dept_type IS RECORD (
		first_name hr.employees.first_name%TYPE,
		last_name  hr.employees.last_name%TYPE,
		dept_info  dept_info_type);
	
	v_emp_dept_rec emp_dept_type;
	
	CURSOR cur_emps IS
		SELECT e.first_name, e.last_name, d.department_id, d.department_name
		FROM hr.employees e JOIN hr.departments d
			 ON e.department_id = e.department_id;
		
BEGIN
	OPEN cur_emps;

	LOOP
		FETCH cur_emps
		INTO v_emp_dept_rec.first_name,
			 v_emp_dept_rec.last_name,
			 v_emp_dept_rec.dept_info.department_id,
			 v_emp_dept_rec.dept_info.department_name;
		EXIT WHEN cur_emps%NOTFOUND;
			
			DBMS_OUTPUT.PUT_LINE(
				v_emp_dept_rec.first_name || ' - ' ||
				v_emp_dept_rec.dept_info.department_name
			);
		
	END LOOP;
		
	CLOSE cur_emps;
	
END;
