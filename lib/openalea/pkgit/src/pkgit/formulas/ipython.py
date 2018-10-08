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
from pkgit.utils import sh, in_dir, try_except

class Ipython(Formula):
    version         = "1.2.1"  	 # Version of the dependency (not of the formula)
    description     = "IPython: a System for Interactive Scientific Computing"     # Description of the dependency (not of the formula)
    homepage        = "http://ipython.org"     # Url of home-page of the dependency (not of the formula)
    license         = "BSD license"     # License of the dependency (not of the formula)
    authors         = "P\'erez, Fernando and Granger, Brian E."     # Authors of the dependency (not of the formula)
    dependencies    = ["python","setuptools", "pygments", "pyzmq"]     # List of dependencies of the formula
    download_name   = "ipython.zip"     # Name of the local archive
    download_url    = "https://pypi.python.org/packages/source/i/ipython/ipython-"+version+".zip"   	 # Url where to download sources (feel only if "DOWNLOAD = True")
    DOWNLOAD = UNPACK = BDIST_EGG = True 
    
    # The good way is : easy_install ipython[all]
    
    @in_dir("sourcedir")
    @try_except
    def _bdist_egg(self):
        return sh("python setup.py bdist_egg -d %s"%(self.dist_dir,)) == 0
    
    
