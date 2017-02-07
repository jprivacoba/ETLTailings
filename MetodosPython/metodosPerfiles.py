"""
#__author__ = 'Arnol'
# Metodos para subir archivos de perfiles
# Version: 3 (2016-06-20)

"""

import os, sys
from osgeo import ogr, osr

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def LoadPerfilMulti(path,connStr,reprocesa):
    proyectos = next(os.walk(path))[1]
    for i in range(len(proyectos)):
        if(proyectos[i].replace(" ","")=="TOPOBASE"):
            print "\nCargando la TOPO BASE (%s/%s)" %(i+1,len(proyectos))
            logging.info("Cargando la TOPO BASE (%s/%s)", i+1, len(proyectos))
            newpath = path+ "/" + proyectos[i] + "/"
            try:
                LoadTopoBase(newpath,connStr)
            except Exception,e:
                print "ERROR al procesar la TOPO BASE : %s " % (str(e))
        else:
            proy=FormatoProyecto(proyectos[i])
            print "\nCargando proyecto %s (%s/%s)" %(proy,i+1,len(proyectos))
            logging.info("Cargando proyecto %s (%s/%s)", proy, i+1, len(proyectos))
            newpath = path+ "/" + proyectos[i] + "/"
            try:
                LoadPerfilSingle(newpath,proy,connStr,reprocesa)
            except Exception,e:
                print "ERROR al procesar el proyecto %s : %s " % (str(proyectos[i]),str(e))
    logging.info("Ejecucion finalizada.")
#   Fin de la funcion


def LoadPerfilSingle(path,proyecto,connStr,reprocesa):
    temp = "" + "temp."
    fechap =  "'"+proyecto[6:]+"-"+proyecto[3:5]+"-"+proyecto[0:2]+"'"
    estado = "'"+str(reprocesa)+"'"
    conn = ogr.Open(connStr)
    sql1 = 'select  perfiles_procesados.crea_proyecto(%s)' % (fechap)
    try:
        numPresults = conn.ExecuteSQL(sql1)
    except Exception,e:
        print "ERROR con la funcion 'crea_proyecto()' " + proyecto + " :" + str(e)
    try:
        for feature in numPresults:
            numP = str(feature.GetField("crea_proyecto"))

        codeError_CargaArchivo = 0
        ficheros = os.listdir(path)
        numfichero = len(ficheros)
        nextfichero = 1

        for fichero in ficheros:
            (nombreFichero, extension) = os.path.splitext(fichero)
            perfilM = FormatoNombreFichero2(nombreFichero)

            if(extension.lower() == ".txt"):
                perfil=perfilM.replace(" ","")
                print 'Cargando perfil "%s" (%s/%s)... '%(str(fichero),nextfichero,numfichero),
                dataPerfil = ""

                try:
                    dataPerfil=DatosPerfil(path+fichero)
                except Exception,e:
                    print "ERROR al leer el archivo de perfil " + fichero + " :" + str(e)

                tablename= temp + str(numP) + " " + perfil + " " + proyecto
                try:
                    codeError_CargaArchivo = CargaArchivoPerfilBySQL(connStr,tablename,dataPerfil)
                except Exception,e:
                    print "ERROR al cargar los datos del perfil " + fichero + " :" + str(e)
                nextfichero = nextfichero + 1
        # Actualiza tabla proyectos_perfiles
        print "Consolidando proyecto en BD... ",
        sql2 = 'select  perfiles_procesados.guarda_proyecto(%d,''%s'')' %(int(numP),str(estado))
        EsError = conn.ExecuteSQL(sql2)
        for feature in EsError: # TODO: ver si se puede cambiar el for por otra cosa, pues el resultado es un solo registro... tal vez EsError[0] o algo asi
            codeError = feature.GetField("guarda_proyecto")
            #print str(codeError)
            if codeError==0 and codeError_CargaArchivo == 0:
                print "Proyecto %s procesado correctamente\n"%(proyecto)
            else:
                print "Proyecto %s procesado con errores\n"%(proyecto)
    except Exception,e:
        print "ERROR al crear proyecto " + proyecto + " :" + str(e)
    conn.Destroy()
#   Fin de la funcion


def LoadTopoBase(path, connStr, reprocesa=True):
    tablename = "perfiles_procesados.proyecto_perfiles_topo_base"
    conn = ogr.Open(connStr)

    if(reprocesa):
        print "Eliminando TOPO BASE anterior... ",
        sql = "TRUNCATE %s" %(tablename)
        try:
            conn.ExecuteSQL(sql)
            print "ok"
        except Exception,e:
            print "ERROR a eliminar topo base anterior: %s"%(str(e))
            return
    ficheros = os.listdir(path)
    numfichero = len(ficheros)
    nextfichero = 1

    for fichero in ficheros:
        (nombreFichero, extension) = os.path.splitext(fichero)
        perfil = FormatoNombreFichero2(nombreFichero)
        perfil=perfil.replace(" ","")
        if extension.lower() == ".txt":
            print 'Cargando perfil "%s" (%s/%s)... '%(str(fichero),nextfichero,numfichero),
            dataPerfil = ""

            try:
                dataPerfil=DatosPerfil(path+fichero)
            except Exception,e:
                print "ERROR al leer el archivo de perfil " + fichero + " :" + str(e)

            try:
                aux = CargaTopoBasePerfilBySQL(connStr, tablename, perfil, dataPerfil)
            except Exception,e:
                print "ERROR al cargar los datos del perfil " + fichero + " :" + str(e)
            nextfichero += 1
    print "TOPO BASE cargada correctamente"
    conn.Destroy()
#Fin de la funcion LoadTopoBase

def FormatoNombreFichero(nombre_old):
    nombre_new = nombre_old.upper()
    SegundoesNumero = 0
    if len(nombre_new)>=2:
        SegundoesNumero = isNumber(nombre_new[1])
    if nombre_new.find("P")==0 and SegundoesNumero==1:
        nombre_new = nombre_new.replace("P","PERFIL")
    return nombre_new
    #Fin de la funcion


def FormatoNombreFichero2(nombre_old):
    nombre_new = nombre_old.upper()
    return nombre_new
#Fin de la funcion FormatoNombreFichero2


def isNumber(str):
    try:
        float(str)
        return 1
    except Exception,e:
        return  0
    #Fin de la funcion


def CargaArchivoPerfilBySQL(connStr,table,datos): #TODO: dejar solo una conexion y no abrir/cerrar a cada crato
    codeError = 0
    # Abrir la conexion
    try:
        conn = ogr.Open(connStr)
    except Exception,e:
        codeError = 1
        print "ERROR al tratar de conectarse a la BD " + " :" + str(e)

    try:
        # create the spatial reference, WGS84
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(4326) # Este campo no se usa asi que se deja este no mas
    except Exception,e:
        codeError = 1
        print "ERROR al tratar de crear la tabla " + table + " :" + str(e)

    try:
        # Crear la tabla con los campos
        layer = conn.CreateLayer(table, srs, ogr.wkbPoint, ['OVERWRITE=YES'] )
        layer.CreateField(ogr.FieldDefn("distancia", ogr.OFTReal))
        layer.CreateField(ogr.FieldDefn("profundidad", ogr.OFTReal))
        layer.CreateField(ogr.FieldDefn("borde", ogr.OFTReal))
        layer.CreateField(ogr.FieldDefn("dem", ogr.OFTReal))
    except Exception,e:
        codeError = 1
        print "ERROR al tratar de crear los campos de la tabla " + table + " :" + str(e)

    # Leer archivo y cargarlo en BD
    nombretabla = table.split(".")
    StrEsquema = nombretabla[0].lower()
    StrTabla =nombretabla[1].lower()
    try:
        sql = 'INSERT INTO "%s"."%s" ("distancia","profundidad","borde","dem") VALUES '%(StrEsquema, StrTabla)
        N = len(datos)
        for i in range(N):
            # Set the attributes using the values from the data
            dist = str(datos[i][0])
            prof = str(datos[i][1])
            bord = str(datos[i][2])
            dem  = str(datos[i][3])
            if dist == 'None':
                dist = "NULL"
            if prof == 'None':
                prof = "NULL"
            if bord == 'None':
                bord = "NULL"
            if dem  == 'None':
                dem  = "NULL"
            sqlAux = '(%s,%s,%s,%s),'%(dist, prof, bord, dem)
            sql = sql + sqlAux
            # Ejecutar el sql completo
        sql = sql[0:-1]
        conn.ExecuteSQL(sql)
        print '%d registros cargados exitosamente'%(N)
    except Exception,e:
        codeError = 1
        print "ERROR al tratar de cargar los datos en la tabla " + table + " :" + str(e)

    return codeError
#  Fin de la funcion CargaArchivoPerfilBySQL


def CargaTopoBasePerfilBySQL(connStr, table, perfil, datos): #TODO: dejar solo una conexion y no abrir/cerrar a cada crato
    codeError = 0
    # Probar la conexion
    try:
        conn = ogr.Open(connStr)
    except Exception,e:
        codeError = 1
        print "ERROR al tratar de conectarse a la BD " + " :" + str(e)
        return codeError
    # Leer archivo y cargarlo en BD
    nombretabla = table.split(".")
    StrEsquema = nombretabla[0].lower()
    StrTabla =nombretabla[1].lower()
    try:
        sql = 'INSERT INTO "%s"."%s" ("perfil","distancia","topo_base") VALUES '%(StrEsquema, StrTabla)
        N = len(datos)
        for i in range(N):
            # Set the attributes using the values from the data
            perf = str(perfil)
            dist = str(datos[i][0])
            topo = str(datos[i][4])
            if dist == 'None':
                dist = "NULL"
            if topo == 'None':
                topo = "NULL"
            sqlAux = "('%s',%s,%s),"%(perf, dist, topo)
            sql = sql + sqlAux
        # Ejecutar el sql completo
        sql = sql[0:-1]
        conn.ExecuteSQL(sql)
        print '%d registros cargados exitosamente'%(N)
    except Exception,e:
        codeError = 1
        print "ERROR al tratar de cargar los datos en la tabla " + table + " :" + str(e)
    return codeError
#Fin de la funcion CargaTopoBasePerfilBySQL

def DatosPerfil(filename):
    datos = []
    lineasprocesadas = 0
    with open(filename) as infile:
        infile.seek(0)
        for line in infile:
            Line=line.split("\t")
            # Modificar en caso que sea 1 linea separada por varios espacios
            if len(Line) == 1:
                Line = DejaUnSoloEspacio(Line[0])
                Line = Line.split(" ")
            # Procesar si hay al menos 2 columnas
            if len(Line) >= 2:
                # Agregar columnas (distancia, batimetria, borde, dem, topo)
                col1=Line[0].replace(",",".")
                col2=Line[1].replace(",",".")
                col3=Line[2].replace(",",".")
                col4=Line[3].replace(",",".")
                col5=Line[4].replace(",",".")
                # En caso que tenga cabecera los datos no se agregan
                if isNumber(col1)==1:
                    try:
                        col1=float(col1)
                    except ValueError:
                        col1=None
                    try:
                        col2=float(col2)
                    except ValueError:
                        col2=None
                    try:
                        col3=float(col3)
                    except ValueError:
                        col3=None
                    try:
                        col4=float(col4)
                    except ValueError:
                        col4=None
                    try:
                        col5=float(col5)
                    except ValueError:
                        col5=None
                    datos.append([col1, col2, col3, col4, col5])
                    lineasprocesadas += 1
    infile.close()
    return datos
#Fin de la funcion DatosPerfil

def FormatoProyecto(StrAux):
    if len(StrAux)>7:
        StrAux = StrAux.replace("_conv","")
        dia = StrAux[0:2]
        mes = StrAux[3:5]
        anno = StrAux[6:]
        if len(anno)==2:
            anno = "20"+anno
        newStr = dia + "_" + mes + "_" + anno
    else:
        newStr = "00_00_0000"
    return newStr

def PrintProgress(texto_pre,texto_post, progreso, total):
    #out = '%s (%s/%s) %s ...      ' %(texto_pre, progreso, total, texto_post)  # The output
    #bs = '\b' * 100            # The backspace
    out = '%s (%s/%s) %s ...      \r' %(texto_pre, progreso, total, texto_post)  # The output'
    #print bs,
    print out,
    if progreso == total:
        print ''
# Fin de la funcion


def NumLinesInFile(file):
    # devuelve el numero de lineas no 'nulas'
    with open(file) as infile:
        num_lines = sum(1 for line in infile if line.strip())
    infile.close()
    return num_lines
# Fin de la funcion


def DejaUnSoloEspacio(texto):
    if texto.find("  ") > -1:
        texto = texto.replace("  "," ")
        texto = DejaUnSoloEspacio(texto)
    return texto.strip()
# Fin de la funcion
