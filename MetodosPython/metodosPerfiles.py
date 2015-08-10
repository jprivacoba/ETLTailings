#__author__ = 'Arnol'
# Metodos para la interfaz grafica para subir archivos de perfiles

import os
from osgeo import ogr,osr

def LoadPerfilSingle(path,proyecto,connStr,reprocesa):
    fechap =  "'"+proyecto[6:]+"-"+proyecto[3:5]+"-"+proyecto[0:2]+"'"
    estado = "'"+str(reprocesa)+"'"
    conn = ogr.Open(connStr)
    sql1 = 'select  perfiles_procesados.crea_proyecto(%s)' %(fechap)
    numPresults = conn.ExecuteSQL(sql1)
    for feature in numPresults:
        numP = str(feature.GetField("crea_proyecto"))
        print "numP es: "+numP #TODO: eliminar despues de testear
    files = []
    #Lista con todos los archivos del directorio:
    ficheros = os.listdir(path)
    for fichero in ficheros:
        (nombreFichero, extension) = os.path.splitext(fichero)
        if(extension == ".txt"):
            perfil=nombreFichero.replace(" ","")
            print perfil
            dataPerfil=DatosPerfil(path+fichero)
            tablename=str(numP) + " " + perfil + " " + proyecto
            CargaArchivoPerfil(connStr,tablename,dataPerfil)
            files.append(nombreFichero+extension)
    # Actualiza tabla proyectos_perfiles
    sql2 = 'select  perfiles_procesados.guarda_proyecto(%d,%s)' %(int(numP),estado)
    EsError = conn.ExecuteSQL(sql2)
    print sql2,EsError
    for feature in EsError:
        print "El codigo de error es " + str(feature.GetField("guarda_proyecto"))
    conn.Destroy()
#   Fin de la funcion


def CargaArchivoPerfil(connStr,table,datos): #TODO: dejar solo una conexion y no abrir/cerrar a cada crato
    # Abrir la coneccion
    conn = ogr.Open(connStr)
    # create the spatial reference, WGS84
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326) # Este campo no se usa asi que se deja este no mas
    # Crear la tabla con los campos
    #print table
    layer = conn.CreateLayer(table, srs, ogr.wkbPoint, ['OVERWRITE=YES'] )
    layer.CreateField(ogr.FieldDefn("distancia", ogr.OFTReal))
    layer.CreateField(ogr.FieldDefn("profundidad", ogr.OFTReal))

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

def LoadPerfilMulti(path,connStr,reprocesa):
    proyectos = os.listdir(path)
    for i in range(len(proyectos)):
        proy=proyectos[i].replace(".","_")
        newpath = path+ "/" + proyectos[i] + "/"
        LoadPerfilSingle(newpath,proy,connStr,reprocesa)
#   Fin de la funcion

def FormatoProyecto(StrAux):
    newStr = "00_00_0000"
    try:
        dia = StrAux[0:2]
        mes = StrAux[3:5]
        anno = StrAux[6:]
        if len(anno)==2:
            anno = "20"+anno
        newStr = dia + "_" + mes + "_" + anno
    except Exception:
        print "Error en el formato del nombre de proyecto: Nombre "+ StrAux+" no valido, debe ser en formato dd_mm_aaaa o dd.mm.aaaa"
    return newStr