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
from pkgit.formulas.qt4 import Qt4 as qt4
from openalea.core.path import path, shutil

class Qscintilla(Formula):
    version = "2.6.2"
    download_url = "http://downloads.sourceforge.net/project/pyqt/QScintilla2/QScintilla-2.6.2/QScintilla-gpl-2.6.2.zip"
    # version = "2.7.2"
    # download_url = "http://sourceforge.net/projects/pyqt/files/QScintilla2/QScintilla-2.7.2/QScintilla-gpl-2.7.2.zip"
    download_name  = "qscintilla.zip"
    dependencies = ["qt4", "mingw"]  
    DOWNLOAD = UNPACK = CONFIGURE = MAKE = MAKE_INSTALL = True
    
    def unpack(self):
        ret = super(Qscintilla, self).unpack()
        self.sourcedir = path(self.sourcedir)/"Qt4Qt5"
        return ret
    
    def configure(self):
        # The install procedure will install qscintilla in qt's installation directories
        qt4_ = qt4()
        paths = qt4_.install_inc_dir, qt4_.install_tra_dir, qt4_.installdir, qt4_.install_dll_dir,
        cmd = ("qmake -after header.path=%s trans.path=%s qsci.path=%s " + \
                                 "target.path=%s -spec win32-g++ qscintilla.pro")%paths
        print
        print cmd
        print
        ret = sh(cmd) == 0
        return ret 
    
    def make_install(self):
        ret = super(Qscintilla, self).make_install()
        qt4_ = qt4()
        try:
            shutil.move( path(qt4_.install_dll_dir)/"libqscintilla2.a", qt4_.install_lib_dir)
        except Exception, e :
            print e
        return ret