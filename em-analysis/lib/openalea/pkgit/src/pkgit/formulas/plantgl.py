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
from pkgit.utils import checkout, sh
from openalea.core.path import path

class Plantgl(Formula):
    version         = "2.16.1"  	 # Version of the dependency (not of the formula)
    description     = "OpenAlea is an open source project primarily aimed at the plant research community."     # Description of the dependency (not of the formula)
    homepage        = "http://openalea.gforge.inria.fr/dokuwiki/doku.php"     # Url of home-page of the dependency (not of the formula)
    license         = "Cecill-C License"     # License of the dependency (not of the formula)
    authors         = "Inria, INRA, CIRAD"     # Authors of the dependency (not of the formula)
    dependencies    = ["openalea", "ann", "bisonflex", "boost", "cgal",
                    "pyopengl", "qt4", "qt4_dev", "qhull", "mingw_rt",
                    "svn", "pyqglviewer"] # List of dependencies of the formula
    download_name   = "plantgl"     # Name of the local archive
    download_url    = "https://scm.gforge.inria.fr/svn/vplants/vplants/trunk/PlantGL"   	 # Url where to download sources (feel only if "DOWNLOAD = True")
    DOWNLOAD = BDIST_EGG = True
    
    def __init__(self,**kwargs):
        super(Plantgl, self).__init__(**kwargs)
        self.dist_dir = path(self._get_dist_path())/"openalea"
        
    def _download(self):
        return checkout(self.download_url, self.eggdir)

    def bdist_egg(self):
        cmd = "python setup.py build bdist_egg -d %s"%(self.dist_dir,)
        print cmd
        return sh(cmd) == 0
        
    def _configure_script(self):
        return True
