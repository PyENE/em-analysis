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

class Svn(Formula):
    license         = "Apache License Version 2.0"
    authors         = "Apache Software Foundation"
    description     = "Enterprise-class centralized version control for the masses"
    version         = "1.8.5"       
    download_url    = "http://sourceforge.net/projects/win32svn/files/"+version+"/apache22/Setup-Subversion-"+version+".msi"
    homepage        = "http://subversion.apache.org/"
    download_name   = "svn.msi"
    DOWNLOAD = INSTALL = COPY_INSTALLER = True 