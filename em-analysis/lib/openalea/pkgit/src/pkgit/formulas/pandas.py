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

class Pandas(Formula):
    version         = "0.13.0"  	 # Version of the dependency (not of the formula)
    description     = "Pandas is a library providing high-performance, easy-to-use data structures and data analysis tools for the Python programming language."     # Description of the dependency (not of the formula)
    homepage        = "http://pandas.pydata.org/"     # Url of home-page of the dependency (not of the formula)
    license         = "BSD"     # License of the dependency (not of the formula)
    authors         = ""     # Authors of the dependency (not of the formula)
    dependencies    = []     # List of dependencies of the formula
    download_url  = "https://pypi.python.org/packages/2.7/p/pandas/pandas-" + version + ".win32-py2.7.exe"     # Name of the local archive
    download_name    = "pandas.exe"   	 # Url where to download sources (feel only if "DOWNLOAD = True")
    DOWNLOAD = COPY_INSTALLER = True 