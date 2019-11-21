# -*- python -*-
#
#       OpenAlea.StdLib
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA  
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################
""" Model nodes """

__license__ = "Cecill-C"
__revision__ = " $Id: models.py 2245 2010-02-08 17:11:34Z cokelaer $ "


#from openalea.core import global_module


def linearmodel(x=0., a=0., b=0.):
    """ return a*x + b  """
    
    return a*x + b