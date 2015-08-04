#__author__ = 'Arnol'

import os
from osgeo import ogr,osr
from Tkinter import *
from tkFileDialog import *
import metodosPerfiles as metPer


dbServer = "152.231.85.226"
dbName = "Testing_ETL"
dbUser = "postgres"
dbPW = "admin"
connString = "PG: host=%s dbname=%s user=%s password=%s" %(dbServer,dbName,dbUser,dbPW)


# Interfaz grafica
def subeArchivos():
    path = str(rutaP.get())
    connStr = connString
    metPer.LoadPerfilMulti(path,connStr,checkvar.get())
# Fin funcion

def formatoRuta(rutaAux):
    aux=rutaAux.replace("\\","/")
    if aux[-1]!="/":
        aux=aux+"/"
    return aux
#Fin funcion

def rutaDir():
    rutadeldirectorio=askdirectory()
    rutaP.set(rutadeldirectorio)
#   Fin funcion

def salir():
    os._exit(0)

def test():
    print checkvar.get()

# Inicializar Interfaz Grafica para carga masiva
w1 = Tk()

# Titulo de la ventana
l = Label(w1, text='Cargador masivo de archivos de perfiles')
l.grid(row=1,column=2)
# Espacio en blanco
aux = Label(w1, text='').grid(row=2,column=2)

# 3era fila
l3 = Label(w1, text='Ruta:')
l3.grid(row=3,column=1)
rutaP = StringVar()
rutaP.set("C:\Users\Arnol\Desktop\TestPerfiles") #TODO: Solo para testing
e3 = Entry(w1, textvariable=rutaP).grid(row=3,column=2) # Extrae ruta
b3 = Button(w1, text='Seleccionar carpeta',command=rutaDir).grid(row=3,column=3)

# 4ta fila en blanco
checkvar = IntVar()
c4 = Checkbutton(w1, text="Reprocesar", variable=checkvar).grid(row=4,column=2)
#aux2 = Label(w1, text='').grid(row=4,column=2)

# 5ta fila
b5 = Button(w1, text='Cargar archivos',command=test).grid(row=5,column=2)
exitB = Button(w1, text='Salir', command=salir).grid(row=5,column=3)

w1.mainloop()