# -*- coding: utf-8 -*-


#setup(console=['InterfazPerfiles.py'])

# Ejecutar en consola como "python setup.py py2exe"




import sys
from distutils.core import setup


kwargs = {}
if 'py2exe' in sys.argv:
    import py2exe
    kwargs = {
        # Usar 'windows' en vez de 'console' para evitar que aparezca la ventana del cmd al ejecutar el .exe
        'windows' : [{
            'script'         : 'InterfazPerfiles.py'
            ,'description'    : 'Interfaz para la carga de perfiles.'
            ,'icon_resources' : [(0, './logo/logo_hgi.ico')]
            }],
        'zipfile' : None,
        'options' : { 'py2exe' : {
            'dll_excludes'   : ['MSVCP90.dll','w9xpopen.exe','mswsock.dll','powrprof.dll'],
            'packages'       : ['win32api'],
            #'bundle_files'   : 1,
            'compressed'     : True,
            'optimize'       : 2
            }},
         }

setup(
    name='ETLTailings',
    author='Arnol Garcia',
    author_email='agarcia@gesecology.com',
    **kwargs)