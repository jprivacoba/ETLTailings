CREATE TRIGGER trg_consolidar_perfiles
  AFTER INSERT OR UPDATE
  ON perfiles_procesados.proyecto_perfiles
  FOR EACH ROW
  EXECUTE PROCEDURE perfiles_procesados.consolidar_proyecto();