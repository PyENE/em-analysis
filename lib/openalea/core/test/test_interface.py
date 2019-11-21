""" Core interface test"""

__license__ = "Cecill-C"
__revision__ = " $Id: test_interface.py 2242 2010-02-08 17:03:26Z cokelaer $ "

from openalea.core.interface import *
from types import *



class IMyInterface(IInterface):
    """Test declation of a new interface"""

    __pytype__ = InstanceType


def test_mapper():

    map = TypeInterfaceMap()

    assert map[FloatType] == IFloat
    assert map[IntType] == IInt
    assert map[BooleanType] == IBool
    assert map[StringType] == IStr
    assert map[ListType] == ISequence
    assert map[DictType] == IDict

    assert map[InstanceType] == IMyInterface
