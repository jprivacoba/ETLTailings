create index 
	proyecto_perfiles_detalle_idx 
on 
	"perfiles_procesados"."proyecto_perfiles_detalle"
	(
		perfil,
		fecha
	);