""" todo 

>>> egg = 'PlantGL-2.2.0.dev_r4822-py2.5-win32.egg'
>>> cmd = 'C:\\Python25\\Scripts\\alea_install.exe -f . %s'
>>> os.system(cmd%egg)
>>> l.remove(egg)
"""

__license__ = "Cecill-C"
__revision__ = " $Id: install_distrib.py 2252 2010-02-08 17:43:10Z cokelaer $"

import os, sys
import glob

l = glob.glob('*.egg')

cmd = sys.prefix + "\\Scripts\\alea_install.exe -H None -f . %s"

for egg in l:
    os.system(cmd % egg)

#os.system('PyQGLViewer-0.2.0-2.2.6-3-Py2.5-Qt4.3.2.exe')
raw_input("finish")
