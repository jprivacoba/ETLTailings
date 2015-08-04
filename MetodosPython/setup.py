# -*- coding: utf-8 -*-

#from distutils.core import setup
#import py2exe

#setup(console=['InterfazPerfiles.py'])


import sys
from distutils.core import setup

kwargs = {}
if 'py2exe' in sys.argv:
    import py2exe
    kwargs = {
        'console' : [{
            'script'         : 'InterfazPerfiles.py',
            'description'    : 'Interfaz para la carga de perfiles.',
            #'icon_resources' : [(0, 'icono.ico')]
            }],
        'zipfile' : None,
        'options' : { 'py2exe' : {
            'dll_excludes'   : ['MSVCP90.dll','w9xpopen.exe','mswsock.dll','powrprof.dll'],
            'packages'       : ['win32api'],
            #'bundle_files'   : 2,
            'compressed'     : True,
            'optimize'       : 2
            }},
         }

setup(
    name='ETLTailings',
    author='Arnol Garcia',
    author_email='agarcia@gesecology.com',
    **kwargs)