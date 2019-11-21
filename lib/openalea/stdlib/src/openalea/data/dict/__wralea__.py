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
__revision__ =" $Id: __wralea__.py 3259 2011-04-14 15:33:05Z pradal $ "


from openalea.core import *
from openalea.core.pkgdict import protected


__name__ = "openalea.data structure.dict"

__version__ = '0.0.1'
__license__ = "Cecill-C"
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'Nodes for standard data structure creation, edition and visualisation.'
__url__ = 'http://openalea.gforge.inria.fr'

               

__all__ = []



dict_ = Factory( name="dict",
              description="Python dictionary",
              category="datatype",
              nodemodule="dicts",
              nodeclass="Dict",
              
              inputs=(dict(name="Dict", interface=IDict),),
              outputs=(dict(name="Dict", interface=IDict),),
              )
__all__.append('dict_')

edict_ = Factory( name="edit dict",
              description="Python dictionary",
              category="datatype",
              nodemodule="dicts",
              nodeclass="EditDict",
              
              inputs=(dict(name="Dict"), dict(name="dict", interface=IDict),),
              outputs=(dict(name="Dict", interface=IDict),),
              )

__all__.append('edict_')



