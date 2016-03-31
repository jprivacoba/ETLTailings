__author__ = 'Arnol'


#from __future__ import division
import string
import os
import metodosPerfiles as met
import Parametros as par

def istext(filename,mode='r'):
    s=open(filename, mode).read(512)
    #print s
    text_characters = "".join(map(chr, range(32, 127)) + list("\n\r\t\b"))
    _null_trans = string.maketrans("", "")
    if not s:
        # Empty files are considered text
        return True
    if "\0" in s:
        # Files with null bytes are likely binary
        print 'null'
        return False
    # Get the non-text characters (maps a character to itself then
    # use the 'remove' option to get rid of the text characters.)
    t = s.translate(_null_trans, text_characters)
    # If more than 30% non-text characters, then
    # this is considered a binary file
    if float(len(t))/float(len(s)) > 0.30:
        return False
    return True


def TestFormatoDIrectorio(path):
    proyectos = next(os.walk(path))[1]
    for i in range(len(proyectos)):
        newpath = path+ "/" + proyectos[i] + "/"
        ficheros = os.listdir(newpath)
        print "Testeando ruta %s" %(newpath)
        for fichero in ficheros:
            #(nombreFichero, extension) = os.path.splitext(fichero)
            """try:
                es_texto = istext(fichero)
                print "El fichero %s es texto : %s" %(fichero,es_texto)
            except Exception,e:
                print "Error al leer el archivo %s : %s" %(fichero,str(e))
                """
            #print newpath+fichero
            es_texto = istext(newpath+fichero)
            print "El fichero %s es texto : %s" %(fichero,es_texto)
#   Fin de la funcion


dir1 = 'C:/Users/Arnol/Downloads/Archive/10 Octubre/06.10.2015/Perfil 1.txt'
dir2 = 'C:/Users/Arnol/Downloads/Archive/11 Noviembre/04.11.2015/P1.txt'
dir3 = 'C:/Users/Arnol/GitHub/ETLTailings/MacroVB/data_procesada/04.02.2016/D1.txt'

"""
print dir1 + ' es un archivo txt? = ' + str(istext(dir1))
print dir2 + ' es un archivo txt? = ' + str(istext(dir2))
print dir3 + ' es un archivo txt? = ' + str(istext(dir3))
"""

#print next(os.walk('C:/Users/Arnol/Downloads/test'))[1]

#print met.NumLinesInFile(dir3)

#met.DatosPerfil("C:/Users/Arnol/GitHub/ETLTailings/MacroVB/data_procesada/04.02.2016/D1.txt")
path = 'C:/Users/Arnol/GitHub/ETLTailings/MacroVB/data_procesada'
connStr = par.GlobalValues['connString']
rep = 0

#met.LoadPerfilMulti(path,connStr,rep)

test_path ='C:/Users/Arnol/Desktop/Archive/nuevos_procesados_test'
#TestFormatoDIrectorio(test_path)

#open('C:/Users/Arnol/Desktop/Archive/nuevos_procesados_test/08.11.2015/1.TXT')


