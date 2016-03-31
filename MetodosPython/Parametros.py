__author__ = 'Arnol'


#TODO: dejar los parametros de conexion en un archivo config.txt
#TODO: borrar valores iniciales de configuarcion
GlobalValues = {}
GlobalValues['host'] = "" + "54.94.215.131"# "152.231.85.226"
GlobalValues['port'] = "" + "5432"
GlobalValues['dbname'] = "" + "HGI_test" #"Testing_ETL"
GlobalValues['user'] = "" + "postgres"
GlobalValues['password'] = "" + "Admin321" #"admin"




GlobalValues['connString'] = "PG: host='%s' port='%s' dbname='%s' user='%s' password='%s'" %(GlobalValues['host'],
                                                                                  GlobalValues['port'],
                                                                                  GlobalValues['dbname'],
                                                                                  GlobalValues['user'],
                                                                                  GlobalValues['password'])