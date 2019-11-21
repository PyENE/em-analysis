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

class Numpy(Formula):
    # Here we can download, install and eggify the package for install it after like an egg
    # with DOWNLOAD = INSTALL = BDIST_EGG = True
    # But we can use DOWNLOAD = COPY_INSTALLER = True
    # So, we download the installer and copy it.
    license         = "Numpy License"
    authors         = "(c) Numpy Developers"
    description     = "NumPy is the fundamental package for scientific computing with Python."    
    version         = "1.8.0"
    homepage        = "http://www.numpy.org/"
    download_url    = "http://freefr.dl.sourceforge.net/project/numpy/NumPy/" + version + "/numpy-" + version + "-win32-superpack-python2.7.exe"
    download_name   = "numpy.exe"
    DOWNLOAD = COPY_INSTALLER = True
