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

class R(Formula):
    license         = "GNU General Public License"
    authors         = "(c) 1998-2013 by Kurt Hornik"
    description     = "The R Project for Statistical Computing"
    version         = "2.15.3"       
    download_url    = "http://mirror.ibcp.fr/pub/CRAN/bin/windows/base/old/2.15.3/R-2.15.3-win.exe"
    homepage        = "http://www.r-project.org/"
    download_name   = "r.exe"
    DOWNLOAD = INSTALL = COPY_INSTALLER = True