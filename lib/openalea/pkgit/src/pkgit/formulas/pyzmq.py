# -*- coding: utf-8 -*- 
# -*- python -*-
#
#       Formula file for pkgit
# 
#       pkgit: tool for dependencies packaging
#
#       Copyright 2014 INRIA - CIRAD - INRA
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
__revision__ = "$$Id: $$"

from pkgit.formula import Formula

class Pyzmq(Formula):
    version         = "14.1.0"  	 # Version of the dependency (not of the formula)
    description     = "Python bindings for 0MQ."     # Description of the dependency (not of the formula)
    homepage        = "http://github.com/zeromq/pyzmq"     # Url of home-page of the dependency (not of the formula)
    license         = "LGPL+BSD"     # License of the dependency (not of the formula)
    authors         = "Brian E. Granger, Min Ragan-Kelley"     # Authors of the dependency (not of the formula)
    dependencies    = []     # List of dependencies of the formula
    download_name   = "pyzmq-" + version + "-py2.7-win32.egg"     # Name of the local archive
    download_url    = "https://pypi.python.org/packages/2.7/p/pyzmq/pyzmq-" + version + "-py2.7-win32.egg"   	 # Url where to download sources (feel only if "DOWNLOAD = True")
    DOWNLOAD = COPY_INSTALLER = True