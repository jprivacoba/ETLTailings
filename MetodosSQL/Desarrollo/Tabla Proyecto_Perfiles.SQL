-- Table: perfiles_procesados.proyecto_perfiles

-- DROP TABLE perfiles_procesados.proyecto_perfiles;

CREATE TABLE perfiles_procesados.proyecto_perfiles
(
  proyecto serial NOT NULL,
  fechaproyecto date,
  codigoproceso character varying(10),
  fechacreacion date,
  codestado character varying(10),
  fechaestado date,
  CONSTRAINT proyecto_perfiles_pkey PRIMARY KEY (proyecto)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE perfiles_procesados.proyecto_perfiles
  OWNER TO postgres;

