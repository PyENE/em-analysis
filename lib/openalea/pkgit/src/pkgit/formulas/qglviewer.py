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
from pkgit.utils import recursive_copy, sh, Pattern
from openalea.core.path import path

class Qglviewer(Formula):
    download_url = "https://gforge.inria.fr/frs/download.php/30907/libQGLViewer-2.3.17-py.tgz"
    download_name  = "qglviewer.tgz"
    DOWNLOAD = UNPACK = CONFIGURE = MAKE = MAKE_INSTALL = True

    def __init__(self, *args, **kwargs):
        super(Qglviewer, self).__init__(*args, **kwargs)
        self.install_inc_dir = path(self.installdir)/"include"/"QGLViewer"
        self.install_dll_dir = path(self.installdir)/"dll"
        self.install_lib_dir = path(self.installdir)/"lib"
        
    def unpack(self):
        ret = super(Qglviewer, self).unpack()
        self.sourcedir = path(self.sourcedir)/"QGLViewer"
        return ret

    def configure(self):
        return sh("qmake QGLViewer.pro") == 0

    def make(self):
        # by default, and since we do not use self.options yet, we build in release mode
        return sh("mingw32-make release") == 0

    def make_install(self):
        # The install procedure will install qscintilla in qt's directories
        recursive_copy( self.sourcedir               , self.install_inc_dir, Pattern.include)
        recursive_copy( path(self.sourcedir)/"release", self.install_lib_dir, Pattern.qtstalib)
        recursive_copy( path(self.sourcedir)/"release", self.install_dll_dir, Pattern.dynlib)
        return True

    def extra_paths(self):
        return self.install_dll_dir