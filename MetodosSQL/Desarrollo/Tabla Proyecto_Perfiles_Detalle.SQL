-- Table: perfiles_procesados.proyecto_perfiles_detalle

-- DROP TABLE perfiles_procesados.proyecto_perfiles_detalle;

CREATE TABLE perfiles_procesados.proyecto_perfiles_detalle
(
  proyecto integer NOT NULL,
  perfil character varying(20) NOT NULL,
  fecha date,
  distancia real NOT NULL,
  profundidad real,
  pendiente real,
  CONSTRAINT proyecto_perfiles_detalle_pk PRIMARY KEY (proyecto, perfil, distancia)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE perfiles_procesados.proyecto_perfiles_detalle
  OWNER TO postgres;
