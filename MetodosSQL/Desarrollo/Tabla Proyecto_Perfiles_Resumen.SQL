-- Table: perfiles_procesados.proyecto_perfiles_resumen

-- DROP TABLE perfiles_procesados.proyecto_perfiles_resumen;

CREATE TABLE perfiles_procesados.proyecto_perfiles_resumen
(
  proyecto integer NOT NULL,
  perfil character varying(20) NOT NULL,
  fechacreacion date,
  codestado character varying(10),
  fechaestado date,
  numerror integer,
  mensajerrror character varying(200),

  CONSTRAINT proyecto_perfiles_resumen_pk PRIMARY KEY (proyecto, perfil)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE perfiles_procesados.proyecto_perfiles_resumen
  OWNER TO postgres;
