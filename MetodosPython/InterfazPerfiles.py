"""
#__author__ = 'Arnol'
# Metodos para la interfaz grafica para subir archivos de perfiles
#
"""
Version = "2.0.0 (2016-06-20)"

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info('Iniciando ejecucion.')


import Tkinter
import ttk
from tkFileDialog import *
import ogr
import os, sys
import datetime as dt
import threading
from PIL import ImageTk, Image

import Parametros as par
import metodosPerfiles as metPer
import ExecuteMacro as macro
import LoggingFrame as logframe


# -----------------------------------------------------
# Variables
# -----------------------------------------------------

test_path = 'C:\Users\Arnol\GitHub\ETLTailings\MacroVB\data_formateada'


# -----------------------------------------------------
# Clase Aplicacion
# -----------------------------------------------------

class Aplicacion(Tkinter.Frame):
    def __init__(self, master=None):
        Tkinter.Frame.__init__(self, master)
        self.master.title("HGI Tailings")
        self.master.iconbitmap('.\logo\logo_hgi.ico')

        # Inicializar pestannas
        self.notebook = ttk.Notebook(master)
        self.frame1 = ttk.Frame(self.notebook)
        self.frame2 = ttk.Frame(self.notebook)
        self.frame3 = ttk.Frame(self.notebook)

        # Crear Menu
        self.CreateMenu()

        # Crear primera pestanna para formatear y cargar datos a BD
        self.notebook.add(self.frame1, text='Cargar proyecto')
        self.StrVarRutaInFormat = Tkinter.StringVar()
        self.StrVarRutaOutFormat = Tkinter.StringVar()
        self.StrVarDescFormat = Tkinter.StringVar()
        self.StrVarRutaCarga = Tkinter.StringVar()
        self.CheckVarRep = Tkinter.IntVar()
        self.StrVarDescCarga = Tkinter.StringVar()
        self.FrameUpload()

        # Crear pestanna Configuracion de conexion
        self.notebook.add(self.frame2, text='Configuracion')
        self.dbServer = Tkinter.StringVar()
        self.dbPort = Tkinter.StringVar()
        self.dbName = Tkinter.StringVar()
        self.dbUser = Tkinter.StringVar()
        self.dbPW = Tkinter.StringVar()
        self.dbConnString = ""
        self.FrameConfig(self.frame2)

        # Crear pestanna de Logger
        self.notebook.add(self.frame3, text='Log de ejecucion')
        self.FrameLogger(self.frame3)

        # pack
        #master.geometry('700x400')
        self.notebook.pack(fill='both', expand='yes')
    # Fin del __init__
    #

    def CreateMenu(self):
        menubar = Tkinter.Menu(self.master)

        filebar = Tkinter.Menu(menubar, tearoff=0)
        filebar.add_command(label="Exit", command=self.master.quit)
        menubar.add_cascade(label="File", menu=filebar)

        helpmenu = Tkinter.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=lambda: self.info_version())
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.master.config(menu=menubar)
    # Fin de la funcion self.CreateMenu
    #

    def info_version(self):
        versionwin = Tkinter.Toplevel(self)
        versionwin.title("Version")
        img = ImageTk.PhotoImage(Image.open('.\logo\logo_hgi.ico'))

        panel = Tkinter.Label(versionwin, image = img)
        panel.image = img
        panel.pack(fill="both", expand="yes")
        Tkinter.Label(versionwin, text="Version del aplicativo %s"%(Version)).pack()

        versionwin.iconbitmap('.\logo\logo_hgi.ico')
    # Fin de la funcion self.info_version
    #

    def FrameUpload(self):
        # Inicializar frame de trabajo y primera fila
        r = 0

        # Top frame con las funciones para formatear los proyectos
        TopFrame = ttk.Labelframe(self.frame1, text='Formatear proyecto')
        TopFrame.pack(side="top", fill="both", expand=True)

        # TopFrame Row: en blanco
        Tkinter.Label(TopFrame, text=" ").grid()
        r += 1

        # TopFrame Row: directorio de entrada
        self.StrVarRutaInFormat.set(DirectorioInicial('formato'))
        Tkinter.Label(TopFrame, text='Ingrese directorio de entrada:').grid(row=r, column=1, sticky='WE')
        Tkinter.Entry(TopFrame, width=55, textvariable=self.StrVarRutaInFormat).grid(row=r, column=2, sticky='WE')
        Tkinter.Label(TopFrame, text=" ").grid(row=r, column=3, sticky='WE')
        Tkinter.Button(TopFrame, text='Seleccionar carpeta',
                       command=lambda: rutaDir(self.StrVarRutaInFormat)).grid(row=r, column=4, sticky='WE')
        r += 1

        # TopFrame Row: en blanco
        Tkinter.Label(TopFrame, text=" ").grid()
        r += 1

        # TopFrame Row: directorio de salida
        self.StrVarRutaOutFormat.set(DirectorioInicial('outputmacro'))
        Tkinter.Label(TopFrame, text='Ingrese directorio de salida:').grid(row=r, column=1, sticky='WE')
        Tkinter.Entry(TopFrame, width=55, textvariable=self.StrVarRutaOutFormat).grid(row=r, column=2, sticky='WE')
        Tkinter.Label(TopFrame, text=" ").grid(row=r, column=3, sticky='WE')
        Tkinter.Button(TopFrame, text='Seleccionar carpeta',
                       command=lambda: rutaDir(self.StrVarRutaOutFormat)).grid(row=r, column=4, sticky='WE')
        r += 1

        # TopFrame Row: en blanco
        Tkinter.Label(TopFrame, text=" ").grid()
        r += 1

        # TopFrame Row: descriptor formato y boton para procesar
        self.StrVarDescFormat.set("Por favor selecciona la carpeta con los proyectos a procesar")
        Tkinter.Label(TopFrame, text=" ").grid()
        Tkinter.Label(TopFrame, textvariable=self.StrVarDescFormat).grid(row=r, column=1, columnspan=2, sticky='W')
        Tkinter.Label(TopFrame, text=" ").grid(row=r, column=3)
        Tkinter.Button(TopFrame, text='Procesar',
                       command=lambda: self.clickFormatea()).grid(row=r, column=4, sticky='WE')
        r += 1

        #

        # Bottom frame con las funciones para subir los proyectos a la BD
        BottomFrame = ttk.Labelframe(self.frame1, text='Cargar proyecto a BD')
        BottomFrame.pack(side="top", fill="both", expand=True)
        r = 0

        # BottomFrame Row: en blanco
        Tkinter.Label(BottomFrame, text=" ").grid()
        r += 1

        # BottomFrame Row: Directorio de Carga
        self.StrVarRutaCarga.set(DirectorioInicial('carga'))
        Tkinter.Label(BottomFrame, text='Ingrese directorio:').grid(row=r, column=1, sticky='WE')
        Tkinter.Entry(BottomFrame, width=55, textvariable=self.StrVarRutaCarga).grid(row=r, column=2, sticky='WE')
        Tkinter.Label(BottomFrame, text=" ").grid(row=r, column=3, sticky='WE')
        Tkinter.Button(BottomFrame, text='Seleccionar carpeta',
                       command=lambda: rutaDir(self.StrVarRutaCarga)).grid(row=r, column=4, sticky='WE')
        r += 1

        # BottomFrame Row: checkvar para reprocesar
        self.CheckVarRep.set(1)
        Tkinter.Checkbutton(BottomFrame, text="Reprocesar", variable=self.CheckVarRep).grid(row=r, column=1)
        r += 1

        # BottomFrame Row: en blanco
        Tkinter.Label(BottomFrame, text=" ").grid()
        r += 1

        # BottomFrame Row: descriptor carga
        self.StrVarDescCarga.set("Por favor selecciona la carpeta con los proyectos a procesar")
        Tkinter.Label(BottomFrame, text=" ").grid()
        Tkinter.Label(BottomFrame, textvariable=self.StrVarDescCarga).grid(row=r, column=1, columnspan=2, sticky='W')
        Tkinter.Label(BottomFrame, text=" ").grid(row=r, column=3)
        Tkinter.Button(BottomFrame, text='Cargar',
                       command=lambda: self.clickCarga()).grid(row=r, column=4, sticky='WE')
    # Fin de la funcion self.FrameUpload()
    #

    def FrameConfig(self, wkFrame):
        # Top Frame
        topFrame = Tkinter.Frame(wkFrame)
        topFrame.pack(side="top", fill="x", expand=False)

        Tkinter.Label(topFrame, text=" ").grid(row=0, column=1)

        self.dbServer.set(par.GlobalValues['host'])
        Tkinter.Label(topFrame, width=25, text='DB Server').grid(row=1, sticky='WE')
        Tkinter.Entry(topFrame, width=25, textvariable=self.dbServer).grid(row=1, column=2, sticky='WE')

        self.dbPort.set(par.GlobalValues['port'])
        Tkinter.Label(topFrame, text='DB Port').grid(row=2, sticky='WE')
        Tkinter.Entry(topFrame, textvariable=self.dbPort).grid(row=2, column=2, sticky='WE')

        self.dbName.set(par.GlobalValues['dbname'])
        Tkinter.Label(topFrame, text='DB Name').grid(row=3, sticky='WE')
        Tkinter.Entry(topFrame, textvariable=self.dbName).grid(row=3, column=2, sticky='WE')

        self.dbUser.set(par.GlobalValues['user'])
        Tkinter.Label(topFrame, text='User').grid(row=4, sticky='WE')
        Tkinter.Entry(topFrame, textvariable=self.dbUser).grid(row=4, column=2, sticky='WE')

        self.dbPW.set(par.GlobalValues['password'])
        Tkinter.Label(topFrame, text='Password').grid(row=5, sticky='WE')
        Tkinter.Entry(topFrame, show="*", width=20, textvariable=self.dbPW).grid(row=5, column=2, sticky='WE')

        self.dbConnString = "PG: host='%s' port='%s' dbname='%s' user='%s' password='%s'" % \
                            (self.dbServer.get(), self.dbPort.get(), self.dbName.get(), self.dbUser.get(), self.dbPW.get())

        #

        # Bottom Frame
        bottomFrame = Tkinter.Frame(wkFrame)
        bottomFrame.pack(side="bottom", fill="both", expand=True)

        # Bottom-Left
        bottomLeft = Tkinter.Frame(bottomFrame)
        bottomLeft.pack(side="left", fill="x", expand=True)
        Tkinter.Button(bottomLeft, width=10, text='Limpiar', command=lambda: self.LimpiaConn()).pack()

        # Bottom-Center
        bottomCenter = Tkinter.Frame(bottomFrame)
        bottomCenter.pack(side="right", fill="x", expand=True)
        Tkinter.Button(bottomCenter, width=15, text='Testear Conexion', command=lambda: self.testConn()).pack()

        # Bottom-Right
        bottomRight = Tkinter.Frame(bottomFrame)
        bottomRight.pack(side="right", fill="x", expand=True)
        Tkinter.Button(bottomRight, width=10, text='Guardar', state='disabled', command=lambda: self.SaveConn()).pack()
    # Fin de la funcion self.FrameConfig()
    #

    def FrameLogger(self, wkFrame):
        # frame 1
        frame1 = Tkinter.Frame(wkFrame)
        T = Tkinter.Text(frame1, height=10, width=10)
        T.pack(side='left', fill='both', expand=1)
        S = Tkinter.Scrollbar(frame1)
        S.pack(side='right', fill='y')
        S.config(command=T.yview)
        T.config(yscrollcommand=S.set)

        # frame 2
        frame2 = Tkinter.Frame(wkFrame)
        P = ttk.Progressbar(frame2, orient='horizontal', mode='indeterminate')
        P.pack(fill='x', expand=1)

        frame1.pack(side='top', fill='both', expand=1)
        frame2.pack(side='bottom', fill='x')

        # Definir TextWidget y Progressbar
        self.textWidget = T
        self.progressBar = P

        # Agregar LogHandler
        # Create textLogger
        text_handler = logframe.TextHandler(T)

        # Add the handler to logger
        logger = logging.getLogger()
        logger.addHandler(text_handler)
    # Fin de la funcion self.FrameLogger()
    #

    def clickFormatea(self):
        # TODO: chequear que carpetas existan
        rutaIn = self.StrVarRutaInFormat.get().replace("/", "\\")
        rutaOut = self.StrVarRutaOutFormat.get().replace("/", "\\")

        # TODO: modificar funcion para que haga lo que corresponde
        self.StrVarDescFormat.set('Ejecutando macro, por favor espere...')
        #self.notebook.select(2)

        # Ejecutar macro
        mDir = "C:\\Users\\Casandra\\PycharmProjects\\ETLTailings\\" \
               "" \
               "MacroVB"
        strFormateo = macro.executeMacroPerfil(mDir, rutaIn, rutaOut)
        self.StrVarDescFormat.set(strFormateo)

        # Asignar carpeta de subida igual a la salida del formato
        self.StrVarRutaCarga.set(rutaOut)
    # Fin de la funcion self.clickFormatea()
    #

    def clickCarga(self):
        # TODO: Modificar para que funcione la barra de progreso
        logging.info("",)
        logging.info("Inciando carga de datos")
        self.updateDescriptor('carga')
        self.progressBar.start()
        self.dbConnString = "PG: host='%s' port='%s' dbname='%s' user='%s' password='%s'" % \
                            (self.dbServer.get(), self.dbPort.get(), self.dbName.get(), self.dbUser.get(), self.dbPW.get())
        subeArchivos(self.CheckVarRep, self.StrVarRutaCarga, self.textWidget, self.dbConnString)
        self.progressBar.stop()
    # Fin de la funcion
    #

    def updateDescriptor(self, tipoDescriptor):
        # TODO: Modificar, eliminar si no es necesario
        if(tipoDescriptor=='format'):
            self.StrVarDescFormat.set('Presionaste el boton Formatear')
        if(tipoDescriptor=='carga'):
            self.StrVarDescCarga.set('Presionaste el boton Cargar')
        self.notebook.select(2)
    # Fin de la funcion self.updateDescriptor()
    #

    def LimpiaConn(self):
        self.dbServer.set("")
        self.dbPort.set("")
        self.dbName.set("")
        self.dbUser.set("")
        self.dbPW.set("")
        self.dbConnString = ""
    # Fin funcion self.LimpiaConn()
    #

    def testConn(self):
        logging.info("testeando conexion: PG: host='%s' port='%s' dbname='%s' user='%s'" %
                     (self.dbServer.get(), self.dbPort.get(), self.dbName.get(), self.dbUser.get()))
        self.dbConnString = "PG: host='%s' port='%s' dbname='%s' user='%s' password='%s'" % \
                            (self.dbServer.get(), self.dbPort.get(), self.dbName.get(), self.dbUser.get(), self.dbPW.get())

        testConnString(self.dbConnString)
    # Fin funcion self.testConn()
    #

    def SaveConn(self):
        Server = self.dbServer.get()
        Port = self.dbPort.get()
        Name = self.dbName.get()
        User = self.dbUser.get()
        PW = self.dbPW.get()
        # TODO: De momento no hace nada, despues hay que guardarlo en un archivo config.json o similar
        #par.GlobalValues['connString'] = "PG: host='%s' port='%s' dbname='%s' user='%s' password='%s'" %(Server,Port,Name,User,PW)
    # Fin funcion self.SaveConn()
    #
# Fin de la clase
#
#


# -----------------------------------------------------
# Clase Std_redirector
# -----------------------------------------------------

class Std_redirector(object):
    def __init__(self, widget):
        self.widget = widget
    # Fin del __init__

    def write(self,string):
        self.widget.insert('end', string)
        self.widget.see('end')
        self.widget.update()
    # Fin de la funcion
# Fin de la clase
#
#


# -----------------------------------------------------
# Funciones
# -----------------------------------------------------

def testConnString(connStr, esTest=1):
    ogr.UseExceptions()
    esError = 0
    try:
        conn = ogr.Open(connStr)
        texto = "Conexion exitosa"
        logging.info("Conexion exitosa")
        conn.Destroy()
    except Exception, e:
        texto = "Error de conexion"
        logging.info("Error de conexion")
        esError = 1
    if esTest == 1:
        EdoConexion(texto)
    if esTest == 0 and esError == 1:
        EdoConexion(texto)
    return esError
# Fin de la funcion


def EdoConexion(estado):
    w3=Tkinter.Toplevel()
    w3.title("HGI Tailings: parametros de conexion")

    whiteL = Tkinter.Label(w3, text="  ")
    whiteL.pack()

    Tkinter.Label(w3, width=20, text=estado).pack()
    Tkinter.Button(w3, text='Aceptar', command=w3.destroy).pack()

    w3.geometry('150x100')
    w3.iconbitmap('.\logo\logo_hgi.ico')
# Fin de la funcion


def rutaDir(StrVarRuta):
    rutadeldirectorio=askdirectory()
    StrVarRuta.set(rutadeldirectorio)
# Fin funcion


def subeArchivos(CheckVar, StrVarRuta, logwin, connStr):
    path = ""
    rep = str(CheckVar.get())

    try:
        conn = ogr.Open(connStr)
        conn.Destroy()
        err = 0
        #err = testConnString(connStr, esTest=0)
    except Exception, e:
        err = 1
        logging.error("Error de conexion al tratar de conectarse a: %s", connStr)
    if err == 0:
        # logwin,mainWin = LogWindow()
        #stdout_old = sys.stdout
        #sys.stdout = Std_redirector(logwin)
        time_ini = dt.datetime.now()
        try:
            path = str(StrVarRuta.get())
        except Exception,e:
            print "ERROR con la ruta especificada: " + str(e)
            err=1
        if err==0:
            print "Carga de archivos iniciada: " + time_ini.strftime("%d-%m-%Y %H:%M:%S")
            print "Parametros de conexion: %s" % connStr
            logwin.update()
            try:
                new_thread = threading.Thread(target=metPer.LoadPerfilMulti(path, connStr, rep))
                new_thread.daemon = True
                new_thread.start()
                time_fin = dt.datetime.now()
                logging.info("Carga de archivos finalizada")
                logging.info("Tiempo de ejecucion: " + str(time_fin-time_ini))
            except Exception,e:
                print "Error de ejecucion:\n" + str(e)
        #sys.stdout = stdout_old
# Fin funcion


def salir():
    os._exit(0)
# Fin funcion


def Test(window):
    1+1
    #window.destroy()
# Fin funcion


def DirectorioInicial(tipoDir):
    if(tipoDir =='formato'):
        return 'C:\Users\Arnol\GitHub\ETLTailings\MacroVB\data_proyectos'
    if(tipoDir =='outputmacro'):
        return 'C:\Users\Arnol\GitHub\ETLTailings\MacroVB\data_formateada'
    if(tipoDir =='carga'):
        return 'C:\Users\Arnol\GitHub\ETLTailings\MacroVB\data_formateada'
# Fin de la funcion DirectorioInicial()




# -----------------------------------------------------
# Inicializar interfaz
# -----------------------------------------------------



root = Tkinter.Tk()
app = Aplicacion(master=root)
app.mainloop()
