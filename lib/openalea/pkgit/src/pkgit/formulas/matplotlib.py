# -*- coding: utf-8 -*- 
# -*- python -*-
#
#       Formula file for pkgit
# 
#       pkgit: tool for dependencies packaging
#
#       Copyright 2013 INRIA - CIRAD - INRA
#
#       File author(s):
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
from __future__ import absolute_import
__revision__ = "$Id: $"

from pkgit.formula import Formula

class Matplotlib(Formula):
    # Here we can download, install and eggify the package for install it after like an egg
    # with DOWNLOAD = INSTALL = BDIST_EGG = True
    # But we can use DOWNLOAD = COPY_INSTALLER = True
    # So, we download the installer and copy it.
    license         = "Python Software Foundation License Derivative - BSD Compatible."
    authors         = "Matplotlib developers"
    version         = "1.3.1"
    homepage        = "http://matplotlib.org/"
    download_url    = "https://downloads.sourceforge.net/project/matplotlib/matplotlib/matplotlib-"+version+"/matplotlib-" + version + ".win32-py2.7.exe"
    download_name   = "matplotlib.exe"
    description     = "Matplotlib is a python 2D plotting library."  
    DOWNLOAD = COPY_INSTALLER = True
