__author__ = 'Arnol'


#from __future__ import division
import metodosPerfiles as met


GlobalValues = {}
GlobalValues['host'] = "" + "54.94.215.131"
GlobalValues['port'] = "" + "5432"
GlobalValues['dbname'] = "HGI"  # "HGI_TeckAndacollo"  # "HGI_test"  # "HGI_SierraGorda"  #
GlobalValues['user'] = "" + "postgres"
GlobalValues['password'] = "" + "Admin321"




GlobalValues['connString'] = "PG: host='%s' port='%s' dbname='%s' user='%s' password='%s'" %(GlobalValues['host'],
                                                                                  GlobalValues['port'],
                                                                                  GlobalValues['dbname'],
                                                                                  GlobalValues['user'],
                                                                                  GlobalValues['password'])

path = 'C:/Users/Arnol/Desktop/test tailings'
connStr = GlobalValues['connString']
rep = 1



met.LoadPerfilMulti(path,connStr,rep)

