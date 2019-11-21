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
from pkgit.formulas.qscintilla import Qscintilla as qscintilla
from pkgit.formulas.pyqt4 import Pyqt4 as pyqt4
import sys
from openalea.core.path import path

class Pyqscintilla(Formula):
    download_url = None 
    download_name  = "qscintilla.zip" # shares the same repos as qscintilla
    dependencies = ["qscintilla"]  
    CONFIGURE = MAKE = MAKE_INSTALL = True
    
    def __init__(self, *args, **kwargs):
        super(Pyqscintilla, self).__init__(*args, **kwargs)
        self.sourcedir = path(self.sourcedir)/"Python"
        # define installation paths
        qsci = qscintilla()
        qt4_ = qt4()
        pyqt = pyqt4()
        self.install_paths = path(qt4_.installdir)/"qsci", path(qsci.sourcedir)/"Qt4Qt5"/"release", \
                             path(qsci.sourcedir)/"Qt4Qt5", path(pyqt.sourcedir)/"sip", \
                             path(pyqt.install_site_dir)/"PyQt4"
        self.qsci_dir = self.install_paths[0]        
  
    def configure(self):
        # we want pyqscintilla to install itself where pyqt4 installed itself.
        # -- The -S flag is needed or else configure.py
        # sees any existing sip installation and can fail. --
        """
        cmd = sys.executable + " -S configure.py"\
                " -a %s -o %s -n %s --sipdir=%s --destdir=%s"%self.install_paths
        # " -a C:/temp_working_dir/install/qt4/qsci"\
        # " -o C:/temp_working_dir/src/qscintilla/Qt4Qt5/release"\
        # " -n C:/temp_working_dir/src/qscintilla/Qt4Qt5"\
        # " -v C:/temp_working_dir/src/pyqt4/sip"\
        # " --destdir=C:/temp_working_dir/install/pyqt4/site/PyQt4" .replace("\\", "/")"""
        cmd = sys.executable + " -S configure.py"\
            " -a C:/temp_working_dir/install/qt4/qsci"\
            " -o C:/temp_working_dir/src/qscintilla/Qt4Qt5/release"\
            " -n C:/temp_working_dir/src/qscintilla/Qt4Qt5"\
            " -v C:/temp_working_dir/install/pyqt4/sip"\
            " --destdir=C:/temp_working_dir/install/pyqt4/site/PyQt4"
            
        """pyqt.inst_paths = pyqt.install_bin_dir, pyqt.install_site_dir, pyqt.install_inc_dir, \
                      pyqt.install_sip_dir

        cmd = sys.executable + " -S configure.py --platform win32-g++ -b %s -d %s -e %s -v %s"%pyqt.inst_paths"""
        print
        print cmd
        print
        return sh(cmd) == 0