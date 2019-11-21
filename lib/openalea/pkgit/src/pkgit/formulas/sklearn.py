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

class Sklearn(Formula):
    version         = "0.14.1"  	 # Version of the dependency (not of the formula)
    description     = "Machine Learning in Python"     # Description of the dependency (not of the formula)
    homepage        = "http://scikit-learn.org"     # Url of home-page of the dependency (not of the formula)
    license         = "BSD license"     # License of the dependency (not of the formula)
    authors         = "Fabian Pedregosa, Gael Varoquaux, Alexandre Gramfort and Vincent Michel and others..."     # Authors of the dependency (not of the formula)
    dependencies    = []     # List of dependencies of the formula
    download_name   = "sklearn.exe"     # Name of the local archive
    download_url    = "http://sourceforge.net/projects/scikit-learn/files/scikit-learn-" + version + ".win32-py2.7.exe/download"   	 # Url where to download sources (feel only if "DOWNLOAD = True")
    DOWNLOAD = COPY_INSTALLER = True