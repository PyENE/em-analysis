"""NoCaseDict tests"""

__license__ = "Cecill-C"
__revision__ = " $Id: test_nocasedict.py 2242 2010-02-08 17:03:26Z cokelaer $ "

from openalea.core.pkgdict import PackageDict


def test_dict():
    """Test packageDict"""
    d = PackageDict()
    d['AbC'] = 3
    assert d['aBc'] == 3
    print d


if __name__=="__main__":
    test_dict()
