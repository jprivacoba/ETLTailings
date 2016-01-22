-- Function: perfiles_procesados.drop_tablas(integer)

-- DROP FUNCTION perfiles_procesados.drop_tablas(integer);

CREATE OR REPLACE FUNCTION perfiles_procesados.drop_tablas(integer)
  RETURNS integer AS
$BODY$

DECLARE
	/* Variables de Entrada */
		nProyecto$	ALIAS FOR $1;	

	nCantidad$ 	INTEGER;

	sQuery$							VARCHAR(200);
	cur_Tablas 					RECORD;
	sNombreTabla$ 			VARCHAR(200);
	
BEGIN
	
		
		nCantidad$ := 0;


			FOR cur_Tablas in
				SELECT
					tables.table_name
				FROM 
					information_schema.tables
				WHERE 
					tables.table_schema::text = 'temp'::text 
					AND tables.table_type::text = 'BASE TABLE'::text
					AND tables.table_name LIKE nProyecto$ || ' %'

			LOOP
				sNombreTabla$ := cur_Tablas.table_name;
				sQuery$ := 'Drop table "temp"."' || sNombreTabla$ || '"';
				EXECUTE sQuery$; 
				nCantidad$ := nCantidad$  +1;
			END LOOP;
							
RETURN nCantidad$;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION perfiles_procesados.drop_tablas(integer)
  OWNER TO postgres;
