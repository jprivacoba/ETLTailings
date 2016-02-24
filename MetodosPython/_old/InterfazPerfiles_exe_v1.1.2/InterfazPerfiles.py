# Autor : Arnol Garcia
# Version : 1.1.2
# Fecha : 24/02/2016


import os
from osgeo import ogr,osr
from Tkinter import *
from tkFileDialog import *
import metodosPerfiles as metPer
import sys
import time
import datetime as dt


#TODO: dejar los parametros de conexion en un archivo config.txt
#TODO: borrar valores iniciales de configuarcion
GlobalValues = {}
GlobalValues['host'] = "" + "54.94.215.131"# "152.231.85.226"
GlobalValues['dbname'] = "" + "HGI_test" #"Testing_ETL"
GlobalValues['user'] = "" + "postgres"
GlobalValues['password'] = "" + "Admin321" #"admin"

"""
GlobalValues['host'] = "" + "152.231.85.226"
GlobalValues['dbname'] = "" + "Testing_ETL"
GlobalValues['user'] = "" + "postgres"
GlobalValues['password'] = ""
"""

GlobalValues['connString'] = 'PG: host=%s dbname=%s user=%s password=%s' %(GlobalValues['host'],
                                                                           GlobalValues['dbname'],
                                                                           GlobalValues['user'],
                                                                           GlobalValues['password'])


# Interfaz grafica
def subeArchivos():
    err = 0
    try:
        connStr = GlobalValues['connString']
        rep = str(checkvar.get())
        err = testConnString(connStr,esTest=0)
    except Exception,e:
        err = 1
    if err == 0:
        logwin,mainWin = LogWindow()
        stdout_old = sys.stdout
        sys.stdout = Std_redirector(logwin)
        time_ini = dt.datetime.now()
        try:
            path = str(rutaP.get())
        except Exception,e:
            print "ERROR con la ruta especificada: " + str(e)
            err=1
        if err==0:
            print "Carga de archivos iniciada: " + time_ini.strftime("%d-%m-%Y %H:%M:%S")
            logwin.update()
            try:
                metPer.LoadPerfilMulti(path,connStr,rep)
                time_fin = dt.datetime.now()
                print "Carga de archivos finalizada: " + time_fin.strftime("%d-%m-%Y %H:%M:%S")
                print "Tiempo de ejecucion: " + str(time_fin-time_ini)
            except Exception,e:
                print "Error de ejecucion:\n" + str(e)
        sys.stdout = stdout_old
        mainWin.title("Log: Finalizado")
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
    if esTest==0 and esError==1:
        EdoConexion(texto)
    return esError

def paramConeccion():
    # Ventana de coneccion a BD
    w2 = Toplevel()
    w2.title("HGI Tailings: parametros de conexion")
    dbServer = StringVar()
    dbServer.set(GlobalValues['host'])
    Lserver = Label(w2, width=15,text='DB Server').grid(row=1,column=1)
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
    Epass = Entry(w2,show="*",width = 20,textvariable=dbPW).grid(row=4,column=2)
    bTest = Button(w2, width=8, text='Test',command=lambda: testConn(dbServer.get(),
                                                            dbName.get(),
                                                            dbUser.get(),
                                                            dbPW.get())).grid(row=5,column=2)
    #TODO: revisar si dejar el check o que el usuario siempre tenga que ingresar los parametros
    #save = IntVar()
    #Csave = Checkbutton(w2, text="Guardar parametros", variable=save).grid(row=5,column=3)
    bOK = Button(w2, width=8,text='Aceptar',command=lambda: aceptaConn(w2,
                                                            dbServer.get(),
                                                            dbName.get(),
                                                            dbUser.get(),
                                                            dbPW.get())).grid(row=5,column=4)
    w2L53 = Label(w2, text=" ").grid(row=5,column=3)
    w2L55 = Label(w2, text=" ").grid(row=5,column=5)
    w2.iconbitmap('.\logo\logo_hgi.ico')


def aceptaConn(window,Server,Name,User,PW):
    GlobalValues['connString'] = 'PG: host=%s dbname=%s user=%s password=%s' %(Server,Name,User,PW)
    GlobalValues['host'] = Server
    GlobalValues['dbname'] = Name
    GlobalValues['user'] = User
    GlobalValues['password'] = PW
    window.destroy()

def EdoConexion(estado):
    w3=Toplevel()
    w3.title("HGI Tailings: parametros de conexion")
    Label(w3, text="").grid(row=1,column=1)
    Label(w3, width=20,text=estado).grid(row=2,column=1)
    Label(w3, text="").grid(row=3,column=1)
    Button(w3, text='Aceptar',command=w3.destroy).grid(row=4,column=1)
    Label(w3, text="").grid(row=5,column=1)
    w3.iconbitmap('.\logo\logo_hgi.ico')

def LogWindow():
    logg = Toplevel()
    time.sleep(3)
    logg.title("Log: Ejecutandose...")
    S = Scrollbar(logg)
    T = Text(logg, height=20, width=70)
    S.pack(side=RIGHT, fill=Y)
    T.pack(side=LEFT, fill=Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)
    exitB = Button(logg,width=10,text="Salir",command=salir).pack(side=BOTTOM)
    aceptaB = Button(logg,width=10,text="Aceptar",command=logg.destroy).pack(side=BOTTOM)
    cancelaB = Button(logg,width=10,text="Cancelar",command=logg.destroy).pack(side=BOTTOM)
    logg.iconbitmap('.\logo\logo_hgi.ico')
    return T,logg
#   Fin de la funcion

class Std_redirector(object):
    def __init__(self,widget):
        self.widget = widget

    def write(self,string):
        self.widget.insert(END,string)
        self.widget.see(END)
        self.widget.update()

def cancelaCarga(self):
    self.destroy()
    #print "ERROR: Carga de archivos cancelada"






# Inicializar Interfaz Grafica para carga masiva

# Ventana principal
w1 = Tk()
w1.title('HGI Tailings: Carga de perfiles')

# 1ra fila (en blanco
l = Label(w1, text="").grid(row=1,column=2)

# 2da fila (boton conexion)
b2 = Button(w1, width=15,
            text='Detalles conexion',
            command=paramConeccion).grid(row=2,column=4)

# 3era fila (Ingresar directorio)
l3 = Label(w1, width=10,text='Ruta:')
l3.grid(row=3,column=1)
rutaP = StringVar()
#TODO: Setear valor de rutaP olo para testing, eliminar despues
#rutaP.set("C:\Users\Arnol\Desktop\TestPerfiles")
e3 = Entry(w1, width=40,textvariable=rutaP).grid(row=3,column=2) # Extrae ruta
b3 = Button(w1, width=15,text='Seleccionar carpeta',command=rutaDir).grid(row=3,column=4)
l33 = Label(w1,width=1,text='').grid(row=3,column=3)
l35 = Label(w1,width=1,text='').grid(row=3,column=5)

# 4ta fila (checkvar)
checkvar = IntVar()
c4 = Checkbutton(w1, text="Reprocesar", variable=checkvar).grid(row=4,column=2)

# 5ta fila "Elegir minera"



# 5ta fila (botones "carga" y "exit")
b5 = Button(w1, text='Cargar archivos',command=subeArchivos).grid(row=5,column=2)
exitB = Button(w1, text='Salir', command=salir).grid(row=5,column=4)

# 6ta fila (en blanco)
l62 = Label(w1, text=" ").grid(row=6,column=2)

# Crear ventana con la informacion de l aversion
def info_version():
    versionwin = Toplevel(w1)
    Label(versionwin, text="Version 1.1.2").grid(row=2,column=2)
    # Labels en blanco en la primera y tercera fila/columna
    Label(versionwin, width=20,text='').grid(row=1,column=1)
    Label(versionwin, width=20,text='').grid(row=3,column=3)
    versionwin.iconbitmap('.\logo\logo_hgi.ico')

# Crear menu
menubar = Menu(w1)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Exit", command=w1.quit)
menubar.add_cascade(label="File", menu=filemenu)
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About...", command=info_version)
menubar.add_cascade(label="Help", menu=helpmenu)
w1.config(menu=menubar)


# Iniciar ventana
w1.iconbitmap('.\logo\logo_hgi.ico')
w1.mainloop()
