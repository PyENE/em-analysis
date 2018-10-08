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

"""
OLD Way to create SCONS egg:

SCONS=scons-1.2.0.d20100117
wget http://sourceforge.net/projects/scons/files/scons/1.2.0.d20100117/${SCONS}.tar.gz/download
tar xvfz ${SCONS}.tar.gz
cp setup_scons.py ${SCONS}/setup.py
cd ${SCONS}
python setup.py build;
python setup.py bdist_egg

"""

import sys, os
from pkgit.utils import sh
from pkgit.formula import Formula
from setuptools import find_packages
from openalea.core.path import path

class Scons(Formula):
    license         = "MIT license"
    authors         = "Steven Knight and The SCons Foundation"
    description     = "SCons is an Open Source software construction tool."    
    version         = "2.3.0"      
    homepage        = "http://scons.org/"
    download_url    = "http://downloads.sourceforge.net/project/scons/scons/2.3.0/scons-2.3.0.zip"
    download_name   = "scons.zip"
    DOWNLOAD = UNPACK = MAKE = BDIST_EGG = True   

    _packages = dict()
    _package_dir = dict()
    _bin_dir = dict()
       
    def make(self):
        ret = sh(sys.executable + " setup.py build") == 0
        os.chdir("engine")
        self._packages=[pkg.replace('.','/') for pkg in find_packages('.')]
        self._package_dir = dict([(pkg, str(path(pkg).abspath())) for pkg in self._packages])
        os.chdir("..")
        self._bin_dir = {'EGG-INFO/scripts': str(path('script').abspath())}
        return ret

    def setup(self):
        print self._package_dir
        print "-----------------"
        print self._packages
        print "================="
        return dict( 
                    PACKAGES = self._packages,
                    PACKAGE_DIRS = self._package_dir,
                    BIN_DIRS = self._bin_dir,
                    ZIP_SAFE = False,
                    setup_requires = ['openalea.deploy'],
                    dependency_links = ['http://openalea.gforge.inria.fr/pi'],
                    ) 