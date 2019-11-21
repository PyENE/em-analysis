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

from openalea.core.path import path
from pkgit.formula import Formula
from pkgit.utils import recursive_copy, Pattern
from pkgit.formulas.mingw import Mingw as mingw

class Mingw_rt(Formula):
    """
    You need to install MinGW first.
    """
    license = "PublicDomain for MingW runtime. GLP or LGPL for some libraries."
    authors = "The Mingw Project"
    description = "Mingw Development (compiler, linker, libs, includes)"
    version        = mingw.version
    download_url = None
    download_name  = "mingw_rt"
    
    dependencies = ["mingw"]
    INSTALL = BDIST_EGG = True
    
    def __init__(self, **kwargs):
        super(Mingw_rt, self).__init__(**kwargs)
        self.sourcedir = mingw().get_path()
        self.install_dll_dir = path(self.installdir)/"dll"
        
    def install(self):
        recursive_copy( path(self.sourcedir)/"bin", self.install_dll_dir, Pattern.dynlib, levels=1)
        return True
        
    def setup(self):
        return dict( 
                    VERSION  = self.version,
                    LIB_DIRS = {"lib":str(self.install_dll_dir)},
                    INC_DIRS = None,
                    BIN_DIRS = None,
                    )             
