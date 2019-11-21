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

class Pyparsing(Formula):
    version = "1.5.7"
    download_url   = "https://pypi.python.org/packages/2.7/p/pyparsing/pyparsing-"+version+".win32-py2.7.exe"
    download_name =	"pyparsing.exe"
    DOWNLOAD = COPY_INSTALLER = True