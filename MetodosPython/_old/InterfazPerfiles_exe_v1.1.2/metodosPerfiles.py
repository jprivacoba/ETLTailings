#__author__ = 'Arnol'
# Metodos para la interfaz grafica para subir archivos de perfiles

import os
from osgeo import ogr,osr


def LoadPerfilMulti(path,connStr,reprocesa):
    proyectos = os.listdir(path)
    for i in range(len(proyectos)):
        proy=FormatoProyecto(proyectos[i])
        newpath = path+ "/" + proyectos[i] + "/"
        try:
            LoadPerfilSingle(newpath,proy,connStr,reprocesa)
        except Exception,e:
            print "ERROR al procesar el proyecto %s : %s "%(str(proyectos[i]),str(e))
#   Fin de la funcion

def LoadPerfilSingle(path,proyecto,connStr,reprocesa):
    temp = "" + "temp."
    fechap =  "'"+proyecto[6:]+"-"+proyecto[3:5]+"-"+proyecto[0:2]+"'"
    estado = "'"+str(reprocesa)+"'"
    conn = ogr.Open(connStr)
    sql1 = 'select  perfiles_procesados.crea_proyecto(%s)' %(fechap)
    try:
        numPresults = conn.ExecuteSQL(sql1)
    except Exception,e:
        print "ERROR con la funcion 'crea_proyecto()' " + proyecto + " :" + str(e)
    try:
        for feature in numPresults:
            numP = str(feature.GetField("crea_proyecto"))
        #files = [] # Al parecer esto no es necesario
        #Lista con todos los archivos del directorio:
        ficheros = os.listdir(path)
        print "/nCargando proyecto " + proyecto
        for fichero in ficheros:
            (nombreFichero, extension) = os.path.splitext(fichero)
            perfilM = nombreFichero.upper()
            if(extension == ".txt" and perfilM.find("PERFIL")==0):
                perfil=nombreFichero.replace(" ","")
                print 'Cargando archivo "'+str(fichero)+'"'
                dataPerfil = ""
                try:
                    dataPerfil=DatosPerfil(path+fichero)
                except Exception,e:
                    print "ERROR al leer el archivo de perfil" + fichero + " :" + str(e)
                tablename= temp + str(numP) + " " + perfil + " " + proyecto
                codeError_CargaArchivo = 0
                try:
                    codeError_CargaArchivo = CargaArchivoPerfil(connStr,tablename,dataPerfil)
                except Exception,e:
                    print "ERROR al cargar los datos del perfil " + fichero + " :" + str(e)
                #files.append(nombreFichero+extension) # Al parecer esto no es necesario
        # Actualiza tabla proyectos_perfiles
        sql2 = 'select  perfiles_procesados.guarda_proyecto(%d,%s)' %(int(numP),estado)
        EsError = conn.ExecuteSQL(sql2)
        for feature in EsError:
            codeError = feature.GetField("guarda_proyecto")
            if codeError==0 and codeError_CargaArchivo == 0:
                print "Proyecto %s procesado exitosamente\n"%(proyecto)
            else:
                print "Proyecto %s procesado con errores\n"%(proyecto)
    except Exception,e:
        print "ERROR al crear proyecto " + proyecto + " :" + str(e)
    conn.Destroy()
#   Fin de la funcion


def CargaArchivoPerfil(connStr,table,datos): #TODO: dejar solo una conexion y no abrir/cerrar a cada crato
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
    except Exception,e:
        codeError = 1
        print "ERROR al tratar de crear los campos distancia y profundidad en la tabla " + table + " :" + str(e)

    # Leer archivo y cargarlo en BD
    N = len(datos)
    for i in range(N):
        # create the feature
        feature = ogr.Feature(layer.GetLayerDefn())
        # Set the attributes using the values from the data
        feature.SetField("distancia", datos[i][0])
        feature.SetField("profundidad", datos[i][1])
        # Crear layer en la BD
        layer.CreateFeature(feature)
        # Destroy the feature to free resources
        feature.Destroy()
    # Destroy the data source to free resources
    conn.Destroy()
    return codeError
#   Fin de la funcion


def DatosPerfil(filename):
    datos = []
    file=open(filename)
    line=file.readline()
    # Encabezado
    line=file.readline()
    while (line != "" and line!="\n"): # Termina si llega al final del archivo o si hay una linea en blanco
        Line=line.split("\t")
        x=float(Line[0].replace(",","."))
        y=float(Line[1].replace(",","."))
        datos.append([x,y])
        line=file.readline()
    file.close()
    return datos
#   Fin de la funcion

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