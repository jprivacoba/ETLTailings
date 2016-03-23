__author__ = 'Arnol'


#from __future__ import division
import string
import os
import metodosPerfiles as met

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

met.DatosPerfil(dir3)
