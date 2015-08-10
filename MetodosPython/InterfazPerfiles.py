#__author__ = 'Arnol'

import os
from osgeo import ogr,osr
from Tkinter import *
from tkFileDialog import *
import metodosPerfiles as metPer
import sys


#dbServer0 = "152.231.85.226"
#dbName0 = "Testing_ETL"
#dbUser0 = "postgres"
#dbPW0 = "admin"
#connString0 = "PG: host=%s dbname=%s user=%s password=%s" %(dbServer0,dbName0,dbUser0,dbPW0)
#TODO: dejar los parametros de conexion en un archivo config.txt
GlobalValues = {}
GlobalValues['host'] = "" + "152.231.85.226"
GlobalValues['dbname'] = "" + "Testing_ETL"
GlobalValues['user'] = "" + "postgres"
GlobalValues['password'] = "" + "admin"
GlobalValues['connString'] = 'PG: host=%s dbname=%s user=%s password=%s' %(GlobalValues['host'],
                                                                           GlobalValues['dbname'],
                                                                           GlobalValues['user'],
                                                                           GlobalValues['password'])


# Interfaz grafica
def subeArchivos():
    path = str(rutaP.get())
    connStr = GlobalValues['connString']
    rep = str(checkvar.get())
    metPer.LoadPerfilMulti(path,connStr,rep)
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
#   Fin funcion

def testConn(dbServer,dbName,dbUser,dbPW):
    connString = 'PG: host=%s dbname=%s user=%s password=%s' %(dbServer,dbName,dbUser,dbPW)
    testConnString(connString)
    # Fin funcion

def testConnString(connStr,esTest=1):
    ogr.UseExceptions()
    texto =""
    esError = 0
    try:
        conn = ogr.Open(connStr)
        texto = "Conexion exitosa"
        conn.Destroy()
    except Exception:
        texto= "Error de conexion"
        esError = 1
    if esTest==1:
        EdoConexion(texto)
    if esTest==0 and esError==1: #TODO: ver si esto funciona o hacer un try/except al llamar a subeArchivo()
        EdoConexion(texto)
        sys.exit(1)

def paramConeccion():
    # Ventana de coneccion a BD
    w2 = Toplevel()
    dbServer = StringVar()
    dbServer.set(GlobalValues['host'])
    Lserver = Label(w2, text='DB Server').grid(row=1,column=1)
    Eserver = Entry(w2, textvariable=dbServer).grid(row=1,column=2)
    dbName = StringVar()
    dbName.set(GlobalValues['dbname'])
    Lname = Label(w2, text='DB Name').grid(row=2,column=1)
    Ename = Entry(w2, textvariable=dbName).grid(row=2,column=2)
    dbUser = StringVar()
    dbUser.set(GlobalValues['user'])
    Luser = Label(w2, text='User').grid(row=3,column=1)
    Euser = Entry(w2, textvariable=dbUser).grid(row=3,column=2)
    dbPW = StringVar()
    dbPW.set(GlobalValues['password'])
    Lpass = Label(w2, text='Password').grid(row=4,column=1)
    Epass = Entry(w2, textvariable=dbPW).grid(row=4,column=2)
    bTest = Button(w2, text='Test',command=lambda: testConn(dbServer.get(),
                                                            dbName.get(),
                                                            dbUser.get(),
                                                            dbPW.get())).grid(row=5,column=2)
    #TODO: revisar si dejar el check o que el usuario siempre tenga que ingresar los parametros
    #save = IntVar()
    #Csave = Checkbutton(w2, text="Guardar parametros", variable=save).grid(row=5,column=3)
    bOK = Button(w2, text='Aceptar',command=lambda: aceptaConn(w2,
                                                            dbServer.get(),
                                                            dbName.get(),
                                                            dbUser.get(),
                                                            dbPW.get())).grid(row=6,column=2)


def aceptaConn(window,Server,Name,User,PW):
    GlobalValues['connString'] = 'PG: host=%s dbname=%s user=%s password=%s' %(Server,Name,User,PW)
    GlobalValues['host'] = Server
    GlobalValues['dbname'] = Name
    GlobalValues['user'] = User
    GlobalValues['password'] = PW
    window.destroy()

def EdoConexion(estado):
    w3=Toplevel()
    w3lab12 = Label(w3, text="").grid(row=1,column=2)
    w3lab21 = Label(w3, text="  ").grid(row=2,column=1)
    w3lab22 = Label(w3, text=estado).grid(row=2,column=2)
    w3lab23 = Label(w3, text="  ").grid(row=2,column=1)
    w3lab32 = Label(w3, text="").grid(row=3,column=2)
    w3bOK = Button(w3, text='Aceptar',command=w3.destroy).grid(row=4,column=2)
    w3lab52 = Label(w3, text="").grid(row=5,column=2)

def testing():
    #print str(GlobalValues['connString'])
    logwin = LogWindow()
    sys.stdout.write = logwin.redirector
    newtext = "hola mundo\n"
    logwin.insert(END, newtext)
    print "testing\n"
#   Fin funcion

def LogWindow():
    logg = Toplevel()
    logg.title("Log")
    S = Scrollbar(logg)
    T = Text(logg, height=20, width=70)
    S.pack(side=RIGHT, fill=Y)
    T.pack(side=LEFT, fill=Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)
    quote = """HAMLET: To be, or not to be--that is the question:
    Whether 'tis nobler in the mind to suffer
    The slings and arrows of outrageous fortune
    Or to take arms against a sea of troubles
    And by opposing end them. To die, to sleep--
    No more--and by a sleep to say we end
    The heartache, and the thousand natural shocks
    That flesh is heir to. 'Tis a consummation
    Devoutly to be wished."""+"\n"
    T.insert(END, quote)
    return T
#   Fin de la funcion

def redirector(self,nputStr):
    self.insert(INSERT, inputStr)






# Inicializar Interfaz Grafica para carga masiva

# Ventana principal
w1 = Tk()
w1.title('Cargador masivo de archivos de perfiles')
# Titulo de la ventana
l = Label(w1, text="")
l.grid(row=1,column=2)
# 2da fila
b2 = Button(w1, text='Detalles conexion',command=paramConeccion).grid(row=2,column=3)
# 3era fila
l3 = Label(w1, text='Ruta:')
l3.grid(row=3,column=1)
rutaP = StringVar()
#TODO: Setear valor de rutaP olo para testing, eliminar despues
rutaP.set("C:\Users\Arnol\Desktop\TestPerfiles")
e3 = Entry(w1, textvariable=rutaP).grid(row=3,column=2) # Extrae ruta
b3 = Button(w1, text='Seleccionar carpeta',command=rutaDir).grid(row=3,column=3)
# 4ta fila en blanco
checkvar = IntVar()
c4 = Checkbutton(w1, text="Reprocesar", variable=checkvar).grid(row=4,column=2)

# 5ta fila
b5 = Button(w1, text='Cargar archivos',command=subeArchivos).grid(row=5,column=2)
exitB = Button(w1, text='Salir', command=salir).grid(row=5,column=3)
w1.mainloop()

