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
from pkgit.utils import with_original_sys_path, sh

class Pylsm(Formula):
    license = "PYLSM License."
    authors = "Freesbi.ch"
    description = "Patched version of PyLSM"
    download_url   = "http://launchpad.net/pylsm/trunk/0.1/+download/pylsm-0.1-r34.orig.tar.gz"
    download_name  = "pylsm.tgz"
    version = "0.1-r34"
    DOWNLOAD = UNPACK = MAKE_INSTALL = BDIST_EGG = True
    
    def make_install(self):
        cmd = "python setup.py install"
        print cmd
        return sh(cmd) == 0
    
    @property 
    @with_original_sys_path
    def package(self):
        return __import__("pylsm")
    
    def setup(self):
        pth = self.package.__path__[0]
        for p in pth.split("\\"):
            if ".egg" in p:
                self.version = p.split("-")[1]+"_1" # we have a patched version
        return dict( LIB_DIRS = {"pylsm" : str(pth)},
                      VERSION  = self.version, )
                    