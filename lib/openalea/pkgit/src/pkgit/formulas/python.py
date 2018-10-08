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

class Python(Formula):
    license = "GPL-compatible"
    authors = "Python Software Foundation"
    description = "Python Language"    
    version = "2.7.6"
    download_url = "http://www.python.org/ftp/python/"+version+"/python-"+version+".msi"
    download_name  = "python-"+version+".msi"
    DOWNLOAD = COPY_INSTALLER = True 
