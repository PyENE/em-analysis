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
from openalea.core.path import path

class Qhull(Formula):
    version         = "2011.2"
    download_url    = "http://www.qhull.org/download/qhull-" + version + ".zip"
    download_name   = "qhull.zip"
    description     = "Qhull computes the convex hull, Delaunay triangulation, Voronoi diagram, halfspace intersection about a point, furthest-site Delaunay triangulation, and furthest-site Voronoi diagram"
    homepage        = "http://www.qhull.org/"
    authors         = "Barber, C.B., Dobkin, D.P., and Huhdanpaa, H.T."
    DOWNLOAD = UNPACK = BDIST_EGG = True
    
    def setup(self):
        return dict(
                    LIB_DIRS         = {'lib' : str(path(self.sourcedir)/'build') },
                    INC_DIRS         = {'include' : str(path(self.sourcedir)/'eg') },
                    BIN_DIRS         = {'bin' : str(path(self.sourcedir)/'bin') },
                    )


class Qhull2012(Formula):
    version         = "2012.1"
    download_url    = "http://www.qhull.org/download/qhull-2012.1.zip"
    download_name   = "qhull.zip"
    description     = "Qhull computes the convex hull, Delaunay triangulation, Voronoi diagram, halfspace intersection about a point, furthest-site Delaunay triangulation, and furthest-site Voronoi diagram"
    homepage        = "http://www.qhull.org/"
    authors         = "Barber, C.B., Dobkin, D.P., and Huhdanpaa, H.T."
    DOWNLOAD = UNPACK = BDIST_EGG = True
    
    def setup(self):
        return dict(
                    LIB_DIRS         = {'lib' : str(path(self.sourcedir)/'build') },
                    INC_DIRS         = {'include' : str(path(self.sourcedir)/'eg') },
                    BIN_DIRS         = {'bin' : str(path(self.sourcedir)/'bin') },
                    )