use puc;
CREATE TABLE indEstadoindestado (
  id int(6) NOT NULL,
  ano int(4) NOT NULL,
  cod_estado int(2) NOT NULL,
  nome_estado varchar(40) NOT NULL,
  cod_municipio int(6) NOT NULL,
  nome_municipio varchar(40) NOT NULL,
  esperanca_nascer varchar(7) NOT NULL,
  mortalidade varchar(7) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
