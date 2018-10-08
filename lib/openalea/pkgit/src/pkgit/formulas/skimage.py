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

class Skimage(Formula):
    version         = "0.9.3"  	 # Version of the dependency (not of the formula)
    description     = "Image processing routines for SciPy"     # Description of the dependency (not of the formula)
    homepage        = "http://scikit-image.org/"     # Url of home-page of the dependency (not of the formula)
    license         = 'Modified BSD'     # License of the dependency (not of the formula)
    authors         = "Stefan van der Walt"     # Authors of the dependency (not of the formula)
    dependencies    = ["scipy"]     # List of dependencies of the formula
    download_name   = "skimage.exe"     # Name of the local archive
    download_url    = "http://www.lfd.uci.edu/~gohlke/pythonlibs/v92jt8xn/scikit-image-" + version + ".win32-py2.7.exe"	 # Url where to download sources (feel only if "DOWNLOAD = True")
    DOWNLOAD = COPY_INSTALLER = True
    
"""
class SkImageWin64(Skimage):
    def create_win32():
        pass
    
    sysinfo = dict(
    archi = 'win64'
    distrib = 'windows'
    os = ""
    )
    
class SkImageLinux(Skimage):
    sysinfo = dict(
    os = "linux"
    )
    cmd1 = "pip install -U scikit-image"
    cmd2 = "easy_install -U scikit-image"
    cmd0 = "alea_install -U scikit-image"
    
def create(archi='64', python='2.7'):
    if archi == "64":
        return SkImageWin64
    else:
        return default_factory(**kwargs)"""