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
from pkgit.utils import sh
from pkgit.formulas.boost import Boost as boost
from pkgit.formulas.mingw import Mingw as mingw
from openalea.core.path import path

class Cgal(Formula):
    license = "GNU Lesser Public License"
    authors = "CGAL, Computational Geometry Algorithms Library"
    description = "Windows gcc libs and includes of CGAL"
    version = "4.2"
    homepage = "http://www.cgal.org/"
    #download_url = "https://gforge.inria.fr/frs/download.php/30390/CGAL-4.0.zip"
    download_url = "https://gforge.inria.fr/frs/download.php/32358/CGAL-"+version+".zip"
    download_name  = "cgal.zip"
    dependencies = ["cmake"]
    DOWNLOAD = UNPACK = CONFIGURE = MAKE = MAKE_INSTALL = BDIST_EGG = True
    

    def configure(self):
        compiler = mingw().get_path()
        boost_ = boost()
        db_quote = lambda x: '"'+x+'"'
        options = " ".join(['-DCMAKE_INSTALL_PREFIX='+db_quote(self.installdir),
                            '-DCMAKE_CXX_COMPILER:FILEPATH='+db_quote(path(compiler)/"bin"/"g++.exe"),
                            '-DBOOST_ROOT='+db_quote(boost_.installdir),
                            '-DGMP_INCLUDE_DIR='+db_quote( path(compiler)/"include" ),
                            '-DMPFR_INCLUDE_DIR='+db_quote( path(compiler)/"include"),
                            '-DZLIB_INCLUDE_DIR='+db_quote(path(compiler)/"include"),
                            '-DZLIB_LIBRARY='+db_quote(path(compiler)/"lib"/"libz.a"),
                            #'-DOPENGL_LIBRARIES='+db_quote(path(compiler)/".."/"lib"/"libglu32.a"),
                            ])
        options=options.replace("\\", "/") #avoid "escape sequence" errors with cmake
        cmd = 'cmake -G"MinGW Makefiles" '+options+' . '
        print cmd
        return sh(cmd) == 0   
    
    def setup(self):
        return dict( 
                    VERSION          = self.version,
                    LIB_DIRS         = {'lib' : str(path(self.sourcedir)/'lib') },
                    INC_DIRS         = {'include' : str(path(self.sourcedir)/'include') },
                    BIN_DIRS         = {'bin' : str(path(self.sourcedir)/'bin') },
                    INSTALL_REQUIRES = ["cmake"],
                    ) 
                    
def create(*args, **kwds):
    "return CgalWin32"
    return Cgal
    
    