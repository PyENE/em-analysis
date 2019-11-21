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
__revision__ = " $Id: plantgl_ext.py 3207 2011-03-24 16:47:05Z dbarbeau $ "

from openalea.secondnature.api import *

import urlparse
import plantgl_icons

class DT_Curve(DataFactory):
    __name__             = "Curve2D"
    __created_mimetype__ = "application/plantgl-curve"
    __icon_rc__          = ":icons/curve2D.png"

    def new(self):
        from vplants.plantgl.gui import curve2deditor

        # -- let the user choose the curve type he wants --
        constraint = curve2deditor.Curve2DConstraint
        data = constraint.defaultCurve()
        iname = self.__name__
        return self.wrap_data(iname, data, constraintType=constraint)


class DT_Function(DataFactory):
    __name__             = "Function2D"
    __created_mimetype__ = "application/plantgl-function"
    __icon_rc__          = ":icons/function.png"

    def new(self):
        from vplants.plantgl.gui import curve2deditor

        # -- let the user choose the curve type he wants --
        constraint = curve2deditor.FuncConstraint
        data = constraint.defaultCurve()
        iname = self.__name__
        return self.wrap_data(iname, data, constraintType=constraint)


class DT_NurbsPatch(DataFactory):
    __name__             = "NurbsPatch"
    __created_mimetype__ =  "application/plantgl-nurbspatch"
    __icon_rc__          = ":icons/nurbspatch.png"

    def new(self):
        from vplants.plantgl.gui import nurbspatcheditor

        data = nurbspatcheditor.NurbsPatchEditor.newDefaultNurbsPatch()
        iname = self.__name__
        return self.wrap_data(iname, data)

class DT_InterpolatedProfile(DataFactory):
    __name__             = "InterpolatedProfile"
    __created_mimetype__ = "application/plantgl-interpolatedcurve"
    __icon_rc__          = ":icons/interpolatedprofile.png"

    def new(self):
        from vplants.plantgl.scenegraph.interpolated_profile import CrossSection
        from vplants.plantgl.scenegraph.interpolated_profile import InterpolatedProfile
        from vplants.plantgl.scenegraph.interpolated_profile import CSplineMethod

        crsSect1 = CrossSection((0., 0.), (0.5, 0.), (0.6, 0.1), (1., 0.))
        crsSect2 = CrossSection((0., 2.), (0.5, 1.), (0.8, 0.3), (1., 0.))
        crsSect3 = CrossSection((0., 0.), (0.5, 0.), (0.7, 0.8), (1., 0.))
        tc = InterpolatedProfile(interpolator=CSplineMethod)

        tc.set_param_range(-180.0, 180.0)
        tc.add_cross_sections(-180, crsSect1,
                              0, crsSect2,
                              180, crsSect3)

        iname = self.__name__

        return self.wrap_data(iname, tc)



class PlantGLFactory(AbstractApplet):
    __name__          = "PlantGL"
    __datafactories__ = [DT_Curve, DT_Function,
                         DT_NurbsPatch, DT_InterpolatedProfile]

    def start(self):
        self.__pglEscSwallower = EscEventSwallower()
        return True

    def create_space_content(self, data):
        if data.mimetype == DT_Curve.__created_mimetype__:
            from vplants.plantgl.gui import curve2deditor
            curve = data.obj
            constraint = data.get_inner_property("constraintType")
            editor = curve2deditor.Curve2DEditor(None, constraints=constraint())
            editor.setCurve(curve)
        elif data.mimetype == DT_Function.__created_mimetype__:
            from vplants.plantgl.gui import curve2deditor
            curve = data.obj
            constraint = data.get_inner_property("constraintType")
            editor = curve2deditor.Curve2DEditor(None, constraints=constraint())
            editor.setCurve(curve)
        elif data.mimetype == DT_NurbsPatch.__created_mimetype__:
            from vplants.plantgl.gui import nurbspatcheditor
            patch = data.obj
            editor = nurbspatcheditor.NurbsPatchEditor(None)
            editor.setNurbsPatch(patch)
        elif data.mimetype == DT_InterpolatedProfile.__created_mimetype__:
            from vplants.plantgl.gui import interpolated_profile_gui
            profile = data.obj
            editor = interpolated_profile_gui.ProfileEditor(editingCentral=False)
            editor.set_profile(profile)
        editor.installEventFilter(self.__pglEscSwallower)
        return SpaceContent(editor)

