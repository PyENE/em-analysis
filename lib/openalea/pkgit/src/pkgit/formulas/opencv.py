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

class Opencv(Formula):
    version         = "2.4.8"  	 # Version of the dependency (not of the formula)
    description     = "open source computer vision"     # Description of the dependency (not of the formula)
    homepage        = "http://opencv.org/"     # Url of home-page of the dependency (not of the formula)
    license         = "BSD"     # License of the dependency (not of the formula)
    authors         = "OpenCV Developers Team"     # Authors of the dependency (not of the formula)
    dependencies    = []     # List of dependencies of the formula
    download_name   = "opencv.exe"     # Name of the local archive
    download_url    = "https://sourceforge.net/projects/opencvlibrary/files/opencv-win/" + version + "/opencv-" + version + ".exe"   	 # Url where to download sources (feel only if "DOWNLOAD = True")
    DOWNLOAD = COPY_INSTALLER = True
    