"""Data tests"""

__license__ = "Cecill-C"
__revision__ = " $Id: test_data.py 2242 2010-02-08 17:03:26Z cokelaer $ "

from openalea.core.pkgmanager import PackageManager


def test_data():
    """test data"""
    pm = PackageManager()
    pm.init()

    assert pm['pkg_test']['file1.txt']
    assert pm['pkg_test']['file2.txt']
