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

class Pywin(Formula):
    license         = "Python Software Foundation License"
    authors         = "Mark Hammond"
    description     = "Python for Windows Extensions"
    version         = "218"       
    download_url    = "http://freefr.dl.sourceforge.net/project/pywin32/pywin32/Build%20218/pywin32-218.win32-py2.7.exe"
    homepage        = "http://pywin32.sourceforge.net/"
    download_name   = "pywin.exe"
    DOWNLOAD = INSTALL = COPY_INSTALLER = True   