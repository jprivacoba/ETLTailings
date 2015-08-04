#__author__ = 'Arnol'

import os
import metodosPerfiles as metPer


dbServer = "152.231.85.226"
dbName = "Testing_ETL"
dbUser = "postgres"
dbPW = "admin"
connString = "PG: host=%s dbname=%s user=%s password=%s" %(dbServer,dbName,dbUser,dbPW)


#path = "C:\Users\Arnol\Desktop\TestPerfiles"
#ficheros = os.listdir(path)
#ficheros2 = ficheros[0].replace(".","_")
#print ficheros,ficheros2



#metPer.LoadPerfilMulti(path,connString)


proyecto = "03_06_2015"

fechap =  "'"+proyecto[6:]+"-"+proyecto[3:5]+"-"+proyecto[0:2]+"'"
estado = "'FALSE'"
sql = 'select  perfiles_procesados.guarda_proyecto(%s,%s)' %(fechap,estado)

print sql