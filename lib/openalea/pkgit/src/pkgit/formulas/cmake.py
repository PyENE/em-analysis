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
from openalea.core.path import path

class Cmake(Formula):
    version        = '2.8.11.2'
    homepage       = "http://www.cmake.org/"
    download_url   = "http://www.cmake.org/files/v2.8/cmake-"+version+"-win32-x86.zip"
    download_name  = "cmake.zip"
    license        = "Copyright 2000-2009 Kitware, Inc., Insight Software Consortium"
    authors        = "Bill Hoffman, Ken Martin, Brad King, Dave Cole, Alexander Neundorf, Clinton Stimpson..."
    DOWNLOAD = UNPACK = BDIST_EGG = POST_INSTALL = True
    
    def setup(self):
        return dict(BIN_DIRS = {'bin' : str(path(self.sourcedir)/'bin') },
                    LIB_DIRS = None,
                    INC_DIRS = {'share' : str(path(self.sourcedir)/'share') },
                    )
    def extra_paths(self):
        return path(self.sourcedir)
