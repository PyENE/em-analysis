
# Redirect path
import os

cdir = os.path.dirname(__file__)
pdir = os.path.join(cdir, "../../scheduler_wralea")
pdir = os.path.abspath(pdir)

__path__ = [pdir] + __path__[:]

from openalea.scheduler_wralea.__init__ import *
