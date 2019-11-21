# -*- python -*-
#
#       OpenAlea.Secondnature
#
#       Copyright 2006-2011 INRIA - CIRAD - INRA
#
#       File author(s): Daniel Barbeau <daniel.barbeau@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

__license__ = "CeCILL v2"
__revision__ = " $Id: layouts.py 3216 2011-03-29 15:47:02Z dbarbeau $ "

from openalea.secondnature.api import *

# -- instantiate layouts --
sk = "{0: [1, 2], 1: [5, 6], 2: [3, 4]},"+\
     "{0: None, 1: 0, 2: 0, 3: 2, 4: 2, 5: 1, 6: 1},"+\
     "{0: {'amount': 0.7272727272727273, 'splitDirection': 2}, "+\
     "1: {'amount': 0.16180555555555556, 'splitDirection': 1}, "+\
     "2: {'amount': 0.960352422907489, 'splitDirection': 2},"+\
     "3: {}, 4: {}, 5: {}, 6: {}}"



default = Layout("Default",
                 skeleton = sk,
                 # the widgets we want are those  placed under the
                 # `Visualea` application namespace.
                 # but you could have "PlantGl.viewer" here too.
                 contentmap={3:("Interpreter","g"),
                            4:("Logger","g"),
                            5:("ProjectManager","g")},
                 easy_name="Default Layout")



def get_builtins():
    return [default]
