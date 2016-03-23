#__author__ = 'Arnol'
# Metodos para la interfaz grafica para subir archivos de perfiles

import os, sys
from osgeo import ogr,osr


def LoadPerfilMulti(path,connStr,reprocesa):
    proyectos = next(os.walk(path))[1]
    for i in range(len(proyectos)):
        proy=FormatoProyecto(proyectos[i])
        print "\nCargando proyecto %s (%s/%s)" %(proy,i+1,len(proyectos))
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
        codeError_CargaArchivo = 0
        ficheros = os.listdir(path)
        #print "\nCargando proyecto " + proyecto
        for fichero in ficheros:
            (nombreFichero, extension) = os.path.splitext(fichero)
            perfilM = FormatoNombreFichero2(nombreFichero)
            if(extension.lower() == ".txt" and perfilM.find("PERFIL")==0):
                perfil=perfilM.replace(" ","")
                print 'Leyendo archivo ... "'+str(fichero)+'"'
                dataPerfil = ""
                try:
                    dataPerfil=DatosPerfil(path+fichero)
                except Exception,e:
                    print "ERROR al leer el archivo de perfil " + fichero + " :" + str(e)
                tablename= temp + str(numP) + " " + perfil + " " + proyecto
                #print str(tablename)
                try:
                    codeError_CargaArchivo = CargaArchivoPerfil(connStr,tablename,dataPerfil)
                except Exception,e:
                    print "ERROR al cargar los datos del perfil " + fichero + " :" + str(e)
        # Actualiza tabla proyectos_perfiles
        sql2 = 'select  perfiles_procesados.guarda_proyecto(%d,%s)' %(int(numP),estado)
        EsError = conn.ExecuteSQL(sql2)
        for feature in EsError: # TODO: ver si se puede cambiar el for por otra cosa, pues el resultado es un solo registro... tal vez EsError[0] o algo asi
            codeError = feature.GetField("guarda_proyecto")
            #print str(codeError)
            if codeError==0 and codeError_CargaArchivo == 0:
                print "Proyecto %s procesado exitosamente\n"%(proyecto)
            else:
                print "Proyecto %s procesado con errores\n"%(proyecto)
    except Exception,e:
        print "ERROR al crear proyecto " + proyecto + " :" + str(e)
    conn.Destroy()
#   Fin de la funcion



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
    nombre_new = "PERFIL_" + nombre_new
    return nombre_new
    #Fin de la funcion

def isNumber(str):
    try:
        float(str)
        return 1
    except Exception,e:
        return  0
    #Fin de la funcion



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
        layer.CreateField(ogr.FieldDefn("dem", ogr.OFTReal))
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
        feature.SetField("dem", datos[i][2])
        # Crear layer en la BD
        layer.CreateFeature(feature)
        # Destroy the feature to free resources
        feature.Destroy()
    # Destroy the data source to free resources
    conn.Destroy()
    return codeError
#   Fin de la funcion


def DatosPerfil(filename):
    print 'Leyendo archivo ' + filename + ' ... '
    datos = []
    #file=open(filename)
    lineasprocesadas = 0
    num_lineas = NumLinesInFile(filename)
    with open(filename) as infile:
        infile.seek(0)
        for line in infile:
            Line=line.split("\t")
            # Solo procesar lineas separadas por tabulacion, con al menos 2 columnas
            if len(Line) >= 2:
                # Agregar primera columna (distancia)
                x=Line[0].replace(",",".")
                # Agregar segunda columna (profundidad)
                y=Line[1].replace(",",".")
                z=None
                # Agregar tercera columna (DEM) si existe
                if len(Line) == 3:
                    z=Line[2].replace(",",".")
                # En caso que tenga cabecera los datos no se agregan
                if isNumber(x)==1:
                    try:
                        x=float(x)
                    except ValueError:
                        x=None
                    try:
                        y=float(y)
                    except ValueError:
                        y=None
                    try:
                        z=float(z)
                    except ValueError:
                        z=None
                    datos.append([x, y, z])
                    lineasprocesadas = lineasprocesadas + 1
                    #PrintProgress('lineas procesadas','',lineasprocesadas,num_lineas)
    infile.close()
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