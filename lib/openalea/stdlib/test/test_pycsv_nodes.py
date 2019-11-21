"""pybase node Tests"""

__license__ = "Cecill-C"
__revision__ = " $Id: test_pycsv_nodes.py 2245 2010-02-08 17:11:34Z cokelaer $"

from openalea.core.alea import run
from openalea.core.pkgmanager import PackageManager


""" A unique PackageManager is created for all test of dataflow """
pm = PackageManager()
pm.init(verbose=True)


def test_read_csv_from_file():
    """ Test of node read_csv"""

    res = run(('openalea.csv', 'read csv'),\
        inputs={'text': '1 1 2 3', 'separator': ' '}, pm=pm)


test_read_csv_from_file()
