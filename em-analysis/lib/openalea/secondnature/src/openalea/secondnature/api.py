#
#       OpenAlea.SecondNature
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
__revision__ = " $Id: api.py 3776 2013-04-05 22:04:58Z jcoste $ "



# APPLET API
from openalea.secondnature.applets import AbstractApplet

# LAYOUT API
from openalea.secondnature.layouts import Layout
from openalea.secondnature.layouts import SpaceContent

# PROJECT API
from openalea.secondnature.project import ProjectManager

# DATA API
from openalea.secondnature.data import DataReader
from openalea.secondnature.data import SingletonFactory
from openalea.secondnature.data import DataFactory
from openalea.secondnature.data import GlobalDataManager
from openalea.secondnature.data import DataFactoryManager
from openalea.secondnature.data import SiblingList

# QT UTILS
from openalea.secondnature.qtutils import EscEventSwallower

# URL UTILS
from openalea.secondnature.urltools import file_url_to_path

# MENU API
def get_datafactory_menu():
    from openalea.vpltk.qt import QtCore
    return QtCore.QCoreApplication.instance().win.get_datafactory_menu()


# WIDGETS
from openalea.secondnature.project_view import ProjectView
