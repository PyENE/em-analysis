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

class Dateutil(Formula):
    version         = "2.2"  	 # Version of the dependency (not of the formula)
    description     = "The dateutil module provides powerful extensions to the standard datetime module, available in Python 2.3+. "     # Description of the dependency (not of the formula)
    homepage        = "http://labix.org/python-dateutil"     # Url of home-page of the dependency (not of the formula)
    license         = "BSD"     # License of the dependency (not of the formula)
    authors         = "Gustavo Niemeyer"     # Authors of the dependency (not of the formula)
    dependencies    = []     # List of dependencies of the formula
    download_name   = "dateutil.tgz"     # Name of the local archive
    download_url    = "https://pypi.python.org/packages/source/p/python-dateutil/python-dateutil-"+version+".tar.gz"   	 # Url where to download sources (feel only if "DOWNLOAD = True")
    DOWNLOAD = UNPACK = BDIST_EGG = True 
    
    # easy_install python-dateutil

    @in_dir("sourcedir")
    @try_except
    def _bdist_egg(self):
        return sh("python setup.py bdist_egg -d %s"%(self.dist_dir,)) == 0