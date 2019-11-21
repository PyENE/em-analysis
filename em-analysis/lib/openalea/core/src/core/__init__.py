"""
See online documentation at 
http://openalea.gforge.inria.fr/doc/sphinx/core/html/contents.html 


"""
__license__ = "Cecill-C"
__revision__ = "$Id: __init__.py 2242 2010-02-08 17:03:26Z cokelaer $"

from openalea.core.external import *
from script_library import ScriptLibrary

def global_module(module):
    """ Declare a module accessible everywhere"""
    import __builtin__
    __builtin__.__dict__[module.__name__] = module

