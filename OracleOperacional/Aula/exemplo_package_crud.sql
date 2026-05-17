CREATE OR REPLACE PACKAGE hr.regions_pkg IS

  -- Tipo de registro correspondente à tabela
  TYPE region_rec IS RECORD (
    region_id   hr.regions.region_id%TYPE,
    region_name hr.regions.region_name%TYPE
  );

  -- CRUD
  PROCEDURE create_region (
    p_region_id   IN hr.regions.region_id%TYPE,
    p_region_name IN hr.regions.region_name%TYPE
  );

  PROCEDURE update_region (
    p_region_id   IN hr.regions.region_id%TYPE,
    p_region_name IN hr.regions.region_name%TYPE
  );

  PROCEDURE delete_region (
    p_region_id IN hr.regions.region_id%TYPE
  );

  FUNCTION get_region (
    p_region_id IN hr.regions.region_id%TYPE
  ) RETURN region_rec;

  FUNCTION list_regions
  RETURN SYS_REFCURSOR;

END regions_pkg;



CREATE OR REPLACE PACKAGE BODY hr.regions_pkg IS

  --------------------------------------------------------------------
  -- INSERT
  --------------------------------------------------------------------
  PROCEDURE create_region (
    p_region_id   IN hr.regions.region_id%TYPE,
    p_region_name IN hr.regions.region_name%TYPE
  ) IS
  BEGIN
    INSERT INTO hr.regions (region_id, region_name)
    VALUES (p_region_id, p_region_name);
  EXCEPTION
    WHEN DUP_VAL_ON_INDEX THEN
      RAISE_APPLICATION_ERROR(-20001, 'Region ID já existe.');
  END create_region;

  --------------------------------------------------------------------
  -- UPDATE
  --------------------------------------------------------------------
  PROCEDURE update_region (
    p_region_id   IN hr.regions.region_id%TYPE,
    p_region_name IN hr.regions.region_name%TYPE
  ) IS
  BEGIN
    UPDATE hr.regions
       SET region_name = p_region_name
     WHERE region_id = p_region_id;

    IF SQL%ROWCOUNT = 0 THEN
      RAISE_APPLICATION_ERROR(-20002, 'Region ID não encontrado.');
    END IF;
  END update_region;

  --------------------------------------------------------------------
  -- DELETE
  --------------------------------------------------------------------
  PROCEDURE delete_region (
    p_region_id IN hr.regions.region_id%TYPE
  ) IS
  BEGIN
    DELETE FROM hr.regions
     WHERE region_id = p_region_id;

    IF SQL%ROWCOUNT = 0 THEN
      RAISE_APPLICATION_ERROR(-20003, 'Region ID não encontrado.');
    END IF;
  END delete_region;

  --------------------------------------------------------------------
  -- GET BY ID
  --------------------------------------------------------------------
  FUNCTION get_region (
    p_region_id IN hr.regions.region_id%TYPE
  ) RETURN region_rec IS
    v_rec region_rec;
  BEGIN
    SELECT region_id, region_name
      INTO v_rec
      FROM hr.regions
     WHERE region_id = p_region_id;

    RETURN v_rec;

  EXCEPTION
    WHEN NO_DATA_FOUND THEN
      RAISE_APPLICATION_ERROR(-20004, 'Region ID não encontrado.');
  END get_region;

  --------------------------------------------------------------------
  -- LIST (consulta geral)
  --------------------------------------------------------------------
  FUNCTION list_regions
  RETURN SYS_REFCURSOR IS
    v_cur SYS_REFCURSOR;
  BEGIN
    OPEN v_cur FOR
      SELECT region_id, region_name
        FROM hr.regions
       ORDER BY region_id;

    RETURN v_cur;
  END list_regions;

END regions_pkg;


