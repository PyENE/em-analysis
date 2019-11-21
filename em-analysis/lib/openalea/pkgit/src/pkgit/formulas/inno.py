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

class Inno(Formula):
    license         = "Free of charge but not public domain : http://www.jrsoftware.org/files/is/license.txt"
    authors         = "(C) 1997-2013 Jordan Russell"
    description     = "Inno Setup is a free installer for Windows programs"  
    version         = "5.5.3"       
    download_url    = "http://mlaan2.home.xs4all.nl/ispack/isetup-5.5.3.exe"
    homepage        = "http://www.jrsoftware.org/"
    download_name   = "innosetup.exe"
    DOWNLOAD = INSTALL = True 