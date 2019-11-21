# -*- python -*-
#
#       OpenAlea.StdLib
#
#       Copyright 2006 - 2008 INRIA - CIRAD - INRA  
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################


__doc__ = """ OpenAlea dictionary data structure"""
__license__ = "Cecill-C"
__revision__ =" $Id: __wralea__.py 2743 2010-08-12 11:16:50Z moscardi $ "


from openalea.core import *
from openalea.core.pkgdict import protected


__name__ = "openalea.data structure.tuple"
__alias__ = []

__version__ = '0.0.1'
__license__ = "Cecill-C"
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'Nodes for standard data structure creation, edition and visualisation.'
__url__ = 'http://openalea.gforge.inria.fr'

               

__all__ = []

pair = Factory( name="pair",
              description="Python 2-uples",
              category="datatype",
              nodemodule="tuples",
              nodeclass="Pair",
              inputs=(dict(name="IN0", interface=None,),
                      dict(name="IN1", interface=None,),),
              outputs=(dict(name="OUT", interface = ISequence),),
              )

__all__.append('pair')

tuple3 = Factory( name="tuple3",
              description="Python 3-uples",
              category="datatype",
              nodemodule="tuples",
              nodeclass="Tuple3",
              inputs=(dict(name="IN0", interface=None,),
                      dict(name="IN1", interface=None,),
                      dict(name="IN1", interface=None,),
                      ),
              outputs=(dict(name="OUT", interface = ISequence),),
              )

__all__.append('tuple3')

tuple_ = Factory( name="tuple",
              description="Python tuple",
              category="datatype",
              nodemodule="tuples",
              nodeclass="Tuple",
              inputs=(dict(name="tuple", interface=ITuple),),
              outputs=(dict(name="tuple", interface = ITuple),),
              )

__all__.append('tuple_')

