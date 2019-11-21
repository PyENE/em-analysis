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

import sys
from openalea.core.path import path
from pkgit.formula import Formula
from pkgit.utils import recursive_copy, sh, recursive_glob_as_dict, \
merge_list_dict, Pattern
from pkgit.formulas.qglviewer import Qglviewer as qglviewer
from pkgit.formulas.qt4 import Qt4 as qt4
#from pkgit.formulas.pyqt4 import pyqt4

class Pyqglviewer(Formula):
    license = "General Public License"
    authors = "libQGLViewer developers for libQGLViewer, PyQGLViewer (INRIA) developers for PyQGLViewer"
    description = "Win-GCC version of PyQGLViewer"
    version = "0.11"
    download_url = "https://gforge.inria.fr/frs/download.php/30908/PyQGLViewer-"+version+".zip"
    download_name  = "pyqglviewer.zip"
    dependencies = ["qglviewer"]
    DOWNLOAD = UNPACK = CONFIGURE = MAKE = MAKE_INSTALL = BDIST_EGG = True

    def __init__(self, *args, **kwargs):
        super(Pyqglviewer, self).__init__(*args, **kwargs)
        qglbuilder = qglviewer()
        self.qglbuilderbase = qglbuilder.sourcedir,
        self.install_sip_dir  = path(qglbuilder.installdir)/"sip"
        self.install_site_dir = qglbuilder.installdir
        self.install_exa_dir  = path(qglbuilder.installdir)/"examples"

    def configure(self):
        # The -S flag is needed or else configure.py
        # sees any existing sip installation and can fail.
        cmd = sys.executable + " -S configure.py -Q %s"%(self.qglbuilderbase)
        # pyqt = pyqt4()
        # cmd = sys.executable + " -S configure.py -Q %s --sip-include-dirs=%s"%(self.qglbuilderbase,pyqt.install_sip_dir)
        print
        print cmd
        print
        return sh(cmd) == 0

    def make_install(self):
        """ pyqglviewer installs itself into the same directory as qglviewer """
        recursive_copy( path(self.sourcedir)/"build", self.install_site_dir, Pattern.pyext, levels=1)
        recursive_copy( path(self.sourcedir)/"src"/"sip", self.install_sip_dir, Pattern.sipfiles, levels=1)
        recursive_copy( path(self.sourcedir)/"examples", self.install_exa_dir, Pattern.any)
        return True

    def extra_python_paths(self):
        qglbuilder = qglviewer()
        return qglbuilder.installdir
        
    def setup(self):
        qt4_   = qt4()
        qglv_   = qglviewer()
        
        pyqgl_mods = recursive_glob_as_dict(self.install_site_dir, Pattern.pyall, strip_keys=True, levels=1).items()
        # includes are recursive subdirectories of qglviewer           
        incs = recursive_glob_as_dict( qglv_.install_inc_dir, Pattern.include, strip_keys=True, prefix_key="include", dirs=True).items()
        inc_dirs = merge_list_dict( incs )
        # libs are recursive subdirectories of qt libs          
        libs = recursive_glob_as_dict(qglv_.install_lib_dir, Pattern.qtstalib, strip_keys=True, prefix_key="lib").items()
        # sip files are recursive subdirectories of pyqglviewer sip installation directory
        sips = recursive_glob_as_dict(self.install_sip_dir, Pattern.sipfiles, strip_keys=True, prefix_key="sip").items()
        # examples are recursive subdirectories of pyqglviewer examples installation directory contains various types of files
        exas = recursive_glob_as_dict(self.install_exa_dir, Pattern.any, strip_keys=True, prefix_key="examples").items()        
        lib_dirs    = {"" : qglv_.install_dll_dir}
        data_files  = exas+sips+libs+pyqgl_mods
        
        # Need an other shell ???
        try:
            import PyQGLViewer
        except ImportError:
            print "================================="
            print "!!!!Can't import PyQGLViewer!!!!!"
            print "Close current shell and try again"
            print "================================="
            raise
        
        return dict( 
                    VERSION      = PyQGLViewer.QGLViewerVersionString(),                                  
                    PACKAGE_DATA = {'' : [Pattern.pyext]},
                    #PACKAGE_DIRS = package_dir,                    
                    LIB_DIRS     = lib_dirs,
                    INC_DIRS     = inc_dirs,
                    
                    DATA_FILES   = data_files,
                    INSTALL_REQUIRES = [qt4_.egg_name()]
                    )  