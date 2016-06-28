"""
#__author__ = 'Arnol'
# Metodos para ejecutar la macro ConsolidaPerfil
#
"""

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

import win32com.client


def executeMacroPerfil(macroDir, directorioIn, directorioOut):
    logging.info('Parametros executeMacroPerfil: (%s, %s, %s)', macroDir, directorioIn, directorioOut)

    # Iniciar Excel
    xl = win32com.client.DispatchEx("Excel.Application")

    # Abrir libro con la macro
    nameWb = "EjecutarMacroPerfiles.xls"
    pathToWb = macroDir + "/" + nameWb
    wb = xl.workbooks.open(pathToWb)

    # Ejecutar Macro 'BorrarLog'
    try:
        xl.run("BorrarLog")
        logging.info('Macro BorrarLog ejecutada correctamente')
    except Exception, e:
        strInfo = 'Error al ejecutar la Macro BorrarLog'
        logging.error('Error al ejecutar la Macro BorrarLog: %s', e)
        return strInfo

    # Ejecutar Macro 'FunctionConsolidaProyectos'
    try:
        nroErrores = xl.run("FunctionConsolidaProyectos", directorioIn, directorioOut)
        logging.debug(nroErrores)
        if nroErrores > 0:
            strInfo = 'Macro ConsolidaProyectos ejecutada con errores. por favor revisa el log'
            logging.info(strInfo)
        else:
            strInfo = 'Macro ConsolidaProyectos ejecutada correctamente'
            logging.info(strInfo)
    except Exception, e:
        logging.error('Error al ejecutar la Macro ConsolidaProyecto: %s', e)
        strInfo = 'Error al ejecutar la Macro ConsolidaProyecto'
        return strInfo

    # Mostrar el libro y retornar salida
    xl.Visible = True
    return strInfo
# Fin de la funcion
#
