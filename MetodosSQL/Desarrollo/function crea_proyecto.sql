-- Function: perfiles_procesados.crea_proyecto(character varying)

-- DROP FUNCTION perfiles_procesados.crea_proyecto(character varying);

CREATE OR REPLACE FUNCTION perfiles_procesados.crea_proyecto(character varying)
  RETURNS integer AS
$BODY$
DECLARE
	/* Variables de Entrada */
	sFecha$ ALIAS FOR $1;	
	/* Variables temporales */
	nNumProyecto$	integer;
	sQuery$			VARCHAR(200);
	cur_Tablas 		RECORD;
	sNombreTabla$ 	VARCHAR(200);	

BEGIN

	nNumProyecto$ := 0;

	SELECT 
		proyecto 
	INTO
		nNumProyecto$
	FROM
		"perfiles_procesados"."proyecto_perfiles"
	WHERE
		fechaproyecto = to_date(sFecha$,'YYYY-MM-DD');
		
	IF NOT FOUND THEN
		nNumProyecto$ := nextval('perfiles_procesados.proyecto_perfiles_proyecto_seq');
		INSERT	INTO 
			"perfiles_procesados"."proyecto_perfiles"
			(
				proyecto,
				fechaproyecto,
				fechacreacion,
				codestado,
				fechaestado
			)
			VALUES
			(
				nNumProyecto$,
				to_date(sFecha$,'YYYY-MM-DD'),
				now(),
				'NUEVO',
				now()			
			);
	ELSE	
		
		FOR cur_Tablas in
			SELECT
				tables.table_name
			FROM 
				information_schema.tables
			WHERE 
				tables.table_schema::text = 'temp'::text 
				AND tables.table_type::text = 'BASE TABLE'::text
				AND tables.table_name LIKE nNumProyecto$ || ' %'

		LOOP
			sNombreTabla$ := cur_Tablas.table_name;
			sQuery$ := 'Drop table "temp"."' || sNombreTabla$ || '"';
			EXECUTE sQuery$; 
		END LOOP;		
		
		UPDATE
			"perfiles_procesados"."proyecto_perfiles"
		SET
			codestado = 'NUEVO',
			fechaestado = now()
		WHERE
			proyecto = 	nNumProyecto$;

	END IF;
	

 RETURN nNumProyecto$;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION perfiles_procesados.crea_proyecto(character varying)
  OWNER TO postgres;
