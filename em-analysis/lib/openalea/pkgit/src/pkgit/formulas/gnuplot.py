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

class Gnuplot(Formula):
    version         = "4.6.3"
    download_url    = "http://downloads.sourceforge.net/project/gnuplot/gnuplot/4.6.3/gp463-win32-setup.exe"
    download_name   = "gnuplot.exe"
    homepage        = "http://www.gnuplot.info/"
    description     = "Gnuplot is a portable command-line driven graphing utility"
    license         = "Gnuplot's copyright"
    authors         = "Thomas Williams, Colin Kelley"
    DOWNLOAD = COPY_INSTALLER = True 