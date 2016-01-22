-- Function: perfiles_procesados.consolidar_proyecto()

-- DROP FUNCTION perfiles_procesados.consolidar_proyecto();

CREATE OR REPLACE FUNCTION perfiles_procesados.consolidar_proyecto()
  RETURNS trigger AS
$BODY$

DECLARE
	/* Variables de Entrada */
	nProyecto$ INTEGER;
	sFecha$		VARCHAR(10);
	sCodTipo$	VARCHAR(10);
	/* Variables temporales */
	nCantidad$ 	INTEGER;
	nCantidadEstado$ 	INTEGER;
	sEstadoProyecto$		VARCHAR(10);
	sTmp1$ 			VARCHAR(200);
	sTmp2$			VARCHAR(200);
	fTmp1$			FLOAT8;
	/*variables lectura Cursor Tablas*/
	--nPerfil$	INTEGER;
	sDia$			VARCHAR(2);
	sMes$			VARCHAR(2);
	sAnio$		VARCHAR(4);
	sPerfil$	VARCHAR(10);
	/*variables lectura cursor Contenido Tabla*/
	fDistancia$				FLOAT8;
	fDistanciaMax$		FLOAT8;
	fProfundidad$			FLOAT8;
	fDistanciaAnt$		FLOAT8;
	fProfundidadAnt$	FLOAT8;
	/*--------------------------------- */
	sQuery$							VARCHAR(200);
	cur_Tablas 					RECORD;
	cur_ContenidoTabla	RECORD;
	sNombreTabla$ 			VARCHAR(200);
	
	/* Variables tabla final */
	fPendiente$	REAL;

	
BEGIN
	
	IF NEW.codestado = 'PENDI' THEN
		
		nProyecto$ := NEW.proyecto;
		sFecha$ = TO_CHAR(new.fechaproyecto,'DD_MM_YYYY');
--Raise notice 'sFecha$ %',sFecha$;
		-- SE SELECCIONAN LAS TABLAS DEL ESQUEMA TEMPORAL PARA LA FECHA DEL PROYECTO
		FOR cur_Tablas in
			SELECT
				tables.table_name
			FROM 
				information_schema.tables
			WHERE 
				tables.table_schema::text = 'temp'::text 
				AND tables.table_type::text = 'BASE TABLE'::text
				AND tables.table_name LIKE '%' ||sFecha$		

		LOOP

			--sTmp1$ := trim(both sFecha$ from sNombreTabla$);--substr(sNombreTabla$,length(sNombreTabla$)-9,10);
			--sDia$:= substr(trim(sTmp1$),1,2);
			--sMes$:= substr(trim(sTmp1$),4,2);		
			--sAnio$:= substr(trim(sTmp1$),7,4);		
			nCantidad$ := 0;
			sNombreTabla$ := cur_Tablas.table_name;
			sTmp1$ := trim(trailing sFecha$ from sNombreTabla$);
			sTmp1$ := upper(sTmp1$);
			sTmp2$ := nProyecto$;
			sPerfil$ := trim(leading sTmp2$ from sTmp1$);
			sPerfil$ := trim(leading 'PERFIL' from trim(sPerfil$));
			--nPerfil$ := cast(COALESCE(sPerfil$, '0') as SMALLINT);
			-- SE VERIFICA SI YA EXISTEN REGISTROS PARA EL PERFIL SELECCIONADO
			SELECT 
				COUNT(*) 
			INTO
				nCantidad$
			FROM 
				"perfiles_procesados"."proyecto_perfiles_detalle"
			WHERE
				proyecto = nProyecto$ AND
				perfil = sPerfil$;
			-- SI NO EXISTEN REGISTRO PARA EL PERFIL, SE CONSOLIDA
			IF nCantidad$ = 0 THEN
			------------------------------------------------------------------------------------------------
				INSERT	INTO 
					"perfiles_procesados"."proyecto_perfiles_resumen"
					(
						proyecto,
						perfil,
						fechacreacion,
						codestado,
						fechaestado,
						numerror
					)
					VALUES
					(
						nProyecto$,
						sPerfil$,
						now(),
						'NUEVO',
						now(),
						0
					);
				fDistanciaMax$:= 0;
				sQuery$ := 'SELECT Max("distancia") 
							FROM "temp"."' || sNombreTabla$ || '"
							WHERE "distancia" IS NOT NULL';
				EXECUTE sQuery$ INTO fDistanciaMax$; 

				sQuery$ := 'SELECT "distancia","profundidad" 
							FROM "temp"."' || sNombreTabla$ || '"
							WHERE "distancia" is not null
							ORDER BY "distancia" ASC';

				fDistanciaAnt$ := 0;
				fProfundidadAnt$	:= 0;
				FOR cur_ContenidoTabla IN
					EXECUTE sQuery$
				LOOP
					fDistancia$ := cur_ContenidoTabla."distancia";
					fProfundidad$ := cur_ContenidoTabla."profundidad";
					fPendiente$:= 0;
					fTmp1$ := 0;

					IF fDistancia$ <> fDistanciaAnt$ THEN
						fTmp1$ := (fProfundidad$ - fProfundidadAnt$)/(fDistancia$ - fDistanciaAnt$);
						fPendiente$ := atan(fTmp1$* (-1))*100/90;
					END IF;

					INSERT INTO
						"perfiles_procesados"."proyecto_perfiles_detalle"
					(
						"proyecto",
						"perfil",
						"fecha",
						"distancia",
						"profundidad",
						"pendiente"
					)
					VALUES
					(
						nProyecto$,
						sPerfil$,
						new.fechaproyecto, --to_date(sAnio$ || sMes$ || sDia$,'YYYYMMDD'),
						fDistanciaMax$ - fDistancia$,
						fProfundidad$,
						fPendiente$
					);

					fDistanciaAnt$ := fDistancia$;
					fProfundidadAnt$	:= fProfundidad$;

				END LOOP;
				
				UPDATE
					"perfiles_procesados"."proyecto_perfiles_resumen"
				SET
					codestado = 'FINAL',
					fechaestado = NOW(),
					numerror = 0,
					mensajerrror = ''
				WHERE
					proyecto = nProyecto$ AND
					perfil = sPerfil$;				
			-----------------------------------------------------------------------------------------------------	
			END IF;

			sQuery$ := 'Drop table "temp"."' || sNombreTabla$ || '"';
			EXECUTE sQuery$; 
						
			
		END LOOP;
		nCantidad$ := 0;
		-- SE VERIFICAN LA CANTIDAD DE PERFILES DEL PROYECTO
		SELECT 
			COUNT(*) 
		INTO
			nCantidad$
		FROM 
			"perfiles_procesados"."proyecto_perfiles_resumen"
		WHERE
			proyecto = nProyecto$;

		nCantidadEstado$ := 0;	
		-- SE VERIFICAN LA CANTIDAD DE PERFILES CORRECTAEMNTE EJECUTADOS DEL PROYECTO	
		SELECT 
			COUNT(*) 
		INTO
			nCantidadEstado$
		FROM 
			"perfiles_procesados"."proyecto_perfiles_resumen"
		WHERE
			proyecto = nProyecto$ AND
			codestado = 'FINAL';
			
		sEstadoProyecto$ := '';
		-- SE VERIFICA EL ESTADO FINAL DEL PROYECTO A PARTIR DE LOS PERFILES EJECUTADOS
		IF nCantidad$ = 0 THEN

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
			END LOOP;
					
			sEstadoProyecto$ := 'VACIO';
		ELSE
			IF nCantidad$ = nCantidadEstado$ THEN
				sEstadoProyecto$ := 'FINAL';
			ELSE
				IF nCantidadEstado$ = 0 THEN
					sEstadoProyecto$ := 'ERROR';
				ELSE
					sEstadoProyecto$ := 'INCOMPLETO';
				END IF;
			END IF;
		END IF;
		-- SE ACTUALIZA EL ESTADO DEL PROYECTO SEGUN EL CALCULO REALIZADO
		UPDATE
			"perfiles_procesados"."proyecto_perfiles"
		SET
			codestado = sEstadoProyecto$,
			fechaestado = now()
		WHERE
			proyecto = nProyecto$;		
	END IF;
	
 RETURN NEW;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION perfiles_procesados.consolidar_proyecto()
  OWNER TO postgres;

  /*
CREATE TRIGGER trg_consolidar_perfiles
AFTER INSERT OR UPDATE ON "perfiles_procesados"."proyecto_perfiles"
    FOR EACH ROW EXECUTE PROCEDURE "perfiles_procesados"."consolidar_proyecto"();
    */
