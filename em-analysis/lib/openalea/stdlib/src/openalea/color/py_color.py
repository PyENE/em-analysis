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
###############################################################################
"""Colormap Nodes"""

__license__ = "Cecill-C"
__revision__ = " $Id: py_color.py 4115 2014-02-25 13:29:28Z dasilva $ "


import random as rd
from openalea.core import *
from openalea.core.observer import lock_notify
import colormap
from colorsys import hsv_to_rgb,rgb_to_hsv

color_list=[(0,0,0),
            (255,0,0),
            (0,255,0),
            (0,0,255),
            (255,255,0),
            (0,255,255),
            (255,0,255),
            (128,255,0),
            (0,128,255),
            (255,0,128),
            (0,255,128),
            (128,0,255),
            (255,128,0),
            (128,128,255),
            (255,128,128),
            (128,255,128),
            (255,255,255)
            ]

class ColorNode (Node) :
    """Small color node
    """
    def __init__ (self, inputs, outputs) :
        Node.__init__(self, inputs, outputs)
        self.set_caption(" ")
        self.get_ad_hoc_dict().set_metadata("useUserColor",True)
    
    def __call__ (self, inputs) :
        color = list(inputs[0])
        if len(color) in (3,4) :
            self.get_ad_hoc_dict().set_metadata("useUserColor",True)
            self.get_ad_hoc_dict().set_metadata("userColor",color)
        
        return color,

class FixedColorNode (Node) :
    """Small color node
    """
    _color = None
    def __init__ (self, inputs, outputs) :
        Node.__init__(self, inputs, outputs)
        self.set_caption(" ")
        self.get_ad_hoc_dict().set_metadata("useUserColor",True)
        self.get_ad_hoc_dict().set_metadata("userColor",self._color)
    
    def __call__ (self, inputs) :
        return self._color,

class BlackNode (FixedColorNode) :
    _color = [0,0,0]

class WhiteNode (FixedColorNode) :
    _color = [255,255,255]

class RedNode (FixedColorNode) :
    _color = [255,0,0]

class GreenNode (FixedColorNode) :
    _color = [0,255,0]

class BlueNode (FixedColorNode) :
    _color = [0,0,255]

def col_item (ind, color_list=color_list) :
    if ind is None:
        return lambda x: color_list[x % len(color_list)]
    elif callable(ind):
        return lambda x: color_list[ind(x) % len(color_list)]
    else:
        return color_list[ind % len(color_list)],

def random (alpha) :
    col = tuple(rd.random() * 255 for i in range(3) )
    if alpha is not None :
        col += (alpha,)
    
    return col,

def rgb (H,S,V, alpha) :
    rgb_col = tuple(int(v * 255) for v in hsv_to_rgb(H / 360.,S / 255.,V / 255.) )
    
    if alpha is not None :
        rgb_col += (alpha,)
    
    return rgb_col,

def hsv (rgb_col) :
    r,g,b = (v / 255. for v in rgb_col[:3])
    h,s,v = rgb_to_hsv(r,g,b)
    H,S,V = (int(h * 360),int(s * 255),int(v * 255))
    
    if len(rgb_col) == 3 :
        return H,S,V,None
    else :
        return H,S,V,rgb_col[3]

def color_map(val, minval=0, maxval=1, coul1=80, coul2=20):
    """todo"""
    cmap = colormap.ColorMap(minval=minval, maxval=maxval)

    if val is None:
        return lambda x: cmap(x, minval, maxval, coul1, coul2)
    elif callable(val):
        return lambda x: cmap(val(x), minval, maxval, coul1, coul2)
    else:
        return cmap(val, minval, maxval, coul1, coul2),


def rgb_color_map(value, minval=0, maxval=1, hue1=0,
        hue2=100, sat=220, val=220):
    """todo"""
    if value < minval:
	value = minval
    if value > maxval:
	value = maxval
	
    newHue = ((value - minval)/(maxval - minval))*(hue2 - hue1) + hue1
    r, g, b = hsv_to_rgb(newHue/400., sat/255., val/255.)
    
    return (int(r*255), int(g*255), int(b*255)),
