SELECT * FROM "perfiles_procesados"."proyecto_perfiles";
-- delete from "perfiles_procesados"."proyecto_perfiles"

SELECT * FROM "perfiles_procesados"."proyecto_perfiles_resumen";
--delete from "perfiles_procesados"."proyecto_perfiles_resumen"

SELECT count(*) FROM "perfiles_procesados"."proyecto_perfiles_detalle";
--delete from "perfiles_procesados"."proyecto_perfiles_detalle"

update "perfiles_procesados"."proyecto_perfiles" 
set codestado = 'PENDI'
,fechaproyecto = '2014-03-26'--'0014-03-26'

WHERE proyecto = 10;