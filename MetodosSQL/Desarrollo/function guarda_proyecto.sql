-- Function: perfiles_procesados.guarda_proyecto(integer, character varying)

-- DROP FUNCTION perfiles_procesados.guarda_proyecto(integer, character varying);

CREATE OR REPLACE FUNCTION perfiles_procesados.guarda_proyecto(
    integer,
    character varying)
  RETURNS integer AS
$BODY$
DECLARE
	/* Variables de Entrada */
	nNumProyecto$	ALIAS FOR $1;	
	sVarTipo$ ALIAS FOR $2;	
	/* Variables temporales */
	sTipo$	VARCHAR(10);
	nCantidad$ integer;
	sTmp1$ varchar(200);
	sTmp2$ varchar(200);
	
/*
sTipo$ = '1':
	se reprocesa todo, es decir, se elimina lo que exista, y se comienza desde 0
sTipo$ = '0':
	solo se actualiza el registro, y al consolidar solo se consolidan los no existentes
*/


BEGIN

	IF sVarTipo$ = '1' THEN
		sTipo$ := 'REPROCESA';
	ELSE
		sTipo$ := 'COMBINA';
	END IF;
	
	nCantidad$ := 0;

			
	IF UPPER(sTipo$) = 'REPROCESA' THEN
		
		DELETE FROM
			"perfiles_procesados"."proyecto_perfiles_detalle"
		WHERE
			proyecto = 	nNumProyecto$;

		DELETE FROM
			"perfiles_procesados"."proyecto_perfiles_resumen"
		WHERE
			proyecto = 	nNumProyecto$;					
			
	END IF;


	UPDATE
		"perfiles_procesados"."proyecto_perfiles"
	SET
		codigoproceso = UPPER(sTipo$),
		codestado = 'PENDI',
		fechaestado = now()
	WHERE
		proyecto = nNumProyecto$;
			
	nCantidad$:= 0;


 RETURN nCantidad$;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION perfiles_procesados.guarda_proyecto(integer, character varying)
  OWNER TO postgres;
