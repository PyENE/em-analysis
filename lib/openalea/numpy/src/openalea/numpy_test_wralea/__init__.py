
# Redirect path
import os

cdir = os.path.dirname(__file__)
pdir = os.path.join(cdir, "../../numpy_test_wralea")
pdir = os.path.abspath(pdir)

__path__ = [pdir] + __path__[:]

from openalea.numpy_test_wralea.__init__ import *
