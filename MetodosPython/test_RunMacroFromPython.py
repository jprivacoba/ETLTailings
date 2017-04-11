__author__ = 'Arnol'


import ExecuteMacro as macro


# Parametros de la macro
mDir = "C:\\Users\\Arnol\\GitHub\\ETLTailings\\MacroVB"
# pDir = "C:\\Users\\Arnol\\Desktop\\test tailings"
pDir = "C:\\Users\\Arnol\\GitHub\\ETLTailings\\MacroVB"

pFolderIn = pDir + "\\data_proyectos"
pFolderOut = pDir + "\\data_proyectos_procesados"


aux = macro.executeMacroPerfil(mDir, pFolderIn, pFolderOut)

print aux