
# Redirect path
import os

cdir = os.path.dirname(__file__)
pdir = os.path.join(cdir, "../../image")
pdir = os.path.abspath(pdir)

__path__ = [pdir] + __path__[:]

from openalea.image.__init__ import *
