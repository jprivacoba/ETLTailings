#__author__ = 'Arnol'
# Metodos para la interfaz grafica para subir archivos de perfiles

import os
from osgeo import ogr,osr

def UploadPerfil(path,proyecto,connStr):
    files = []
    #Lista con todos los archivos del directorio:
    ficheros = os.listdir(path)
    #Crea una lista de los ficheros jpg que existen en el directorio y los incluye a la lista.
    for fichero in ficheros:
        (nombreFichero, extension) = os.path.splitext(fichero)
        if(extension == ".txt"):
            perfil=nombreFichero.split(" ")
            print perfil
            dataPerfil=DatosPerfil(path+fichero)
            tablename=nombreFichero+" " + proyecto
            CargaArchivoPerfil(connStr,tablename,dataPerfil)
            files.append(nombreFichero+extension)
    # TODO: Inserta nuevo registro en la tabla proyectos_perfiles o actualizar si ya existe
    conn = ogr.Open(connStr)
    #sql = 'ALTER TABLE %s DROP COLUMN "wkb_geometry","ogc_fid";' %(table)
    #conn.ExecuteSQL(sql)

#   Fin de la funcion


def CargaArchivoPerfil(connStr,table,datos):
    # Abrir la coneccion
    conn = ogr.Open(connStr)
    # create the spatial reference, WGS84
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326) # Este campo no se usa asi que se deja este no mas
    # Crear la tabla con los campos
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
        x=float(Line[0])
        y=float(Line[1])
        datos.append([x,y])
        line=file.readline()
    file.close()
    return datos
#   Fin de la funcion


