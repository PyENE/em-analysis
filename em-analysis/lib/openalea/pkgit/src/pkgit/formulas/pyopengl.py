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

class Pyopengl(Formula):
    license         = "BSD-style Open-Source license"
    authors         = "Mike C. Fletcher"
    description     = "Standard OpenGL bindings for Python"
    version         = "3.0.2"       
    download_url    = "http://pypi.python.org/packages/any/P/PyOpenGL/PyOpenGL-"+version+".win32.exe"
    homepage        = "http://pyopengl.sourceforge.net/"
    download_name   = "pyopengl.exe"
    DOWNLOAD = COPY_INSTALLER = True 