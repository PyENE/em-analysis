import os.path
from os.path import join as pj

cdir = os.path.dirname(__file__)
pdir = pj(cdir, "..", "..", "ema")
pdir = os.path.abspath(pdir)
import openalea.ema
from openalea.ema import __path__
__path__ = [pdir] + __path__[:]

from openalea.ema.__init__ import *


