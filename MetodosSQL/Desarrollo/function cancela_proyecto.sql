-- Function: perfiles_procesados.cancela_proyecto(integer)

-- DROP FUNCTION perfiles_procesados.cancela_proyecto(integer);

CREATE OR REPLACE FUNCTION perfiles_procesados.cancela_proyecto(integer)
  RETURNS integer AS
$BODY$
DECLARE
	/* Variables de Entrada */
	nNumProyecto$	ALIAS FOR $1;	
	/* Variables temporales */
	sTipo$	VARCHAR(10);
	nCantidad$ integer;


BEGIN

	
	nCantidad$ := 0;

			
		
	DELETE FROM
		"perfiles_procesados"."proyecto_perfiles_detalle"
	WHERE
		proyecto = 	nNumProyecto$;

	DELETE FROM
		"perfiles_procesados"."proyecto_perfiles_resumen"
	WHERE
		proyecto = 	nNumProyecto$;					
			



	UPDATE
		"perfiles_procesados"."proyecto_perfiles"
	SET
		codigoproceso = UPPER(sTipo$),
		codestado = 'CANCELADO',
		fechaestado = now()
	WHERE
		proyecto = nNumProyecto$;
			
	nCantidad$:= 0;


 RETURN nCantidad$;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION perfiles_procesados.cancela_proyecto(integer)
  OWNER TO postgres;
