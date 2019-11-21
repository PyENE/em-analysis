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

class Pygments(Formula):
    version         = "1.6"  	 # Version of the dependency (not of the formula)
    description     = "Python syntax highlighter"     # Description of the dependency (not of the formula)
    homepage        = "http://pygments.org"     # Url of home-page of the dependency (not of the formula)
    license         = "BSD license"     # License of the dependency (not of the formula)
    authors         = "Georg Brandl and Pygments contributors"     # Authors of the dependency (not of the formula)
    dependencies    = []     # List of dependencies of the formula
    download_name   = "Pygments-" + version + "-py2.7.egg"     # Name of the local archive
    download_url    = "https://pypi.python.org/packages/2.7/P/Pygments/Pygments-" + version + "-py2.7.egg"   	 # Url where to download sources (feel only if "DOWNLOAD = True")

    DOWNLOAD = COPY_INSTALLER = True 