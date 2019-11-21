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

class Pillow(Formula):
    # Here we can download, install and eggify the package for install it after like an egg
    # with DOWNLOAD = INSTALL = BDIST_EGG = True
    # But we can use DOWNLOAD = COPY_INSTALLER = True
    # So, we download the installer and copy it.
    license         = "Pillow License."
    authors         = "Copyright (c) 1997-2011 by Secret Labs AB, Copyright (c) 1995-2011 by Fredrik Lundh."
    description     = "Pillow is the 'friendly' PIL fork by Alex Clark and Contributors. PIL is the Python Imaging Library by Fredrik Lundh and Contributors."  
    __modulename__  = "Image"
    __packagename__ = "PIL"
    version         = "2.1.0"       
    download_url    = "https://pypi.python.org/packages/2.7/P/Pillow/Pillow-"+version+".win32-py2.7.exe"
    homepage        = "https://pypi.python.org/pypi/Pillow"
    download_name   = "pillow.exe"
    DOWNLOAD = COPY_INSTALLER = True
