# -*- coding: utf-8 -*-
"""setup file for pandas package"""
__revision__ = "$Id: setup.py 3815 2013-07-01 13:32:53Z camillechambon $"

import os
from setuptools import setup, find_packages

__license__ = 'Cecill-C' 
__revision__ = "$Id: setup.py 3815 2013-07-01 13:32:53Z camillechambon $"

pj = os.path.join

from openalea.deploy.metainfo import read_metainfo
metadata = read_metainfo('metainfo.ini', verbose=True)
for key,value in metadata.iteritems():
    exec("%s = '%s'" % (key, value))

pkgs = [ pkg for pkg in find_packages('src') if namespace not in pkg] 
top_pkgs = [pkg for pkg in pkgs if  len(pkg.split('.')) < 2]
packages = [ namespace + "." + pkg for pkg in pkgs]
package_dir = dict( [('','src')] + [(namespace + "." + pkg,  "src/" + pkg) for pkg in top_pkgs] )

setup(
    name=name,
    version=version,
    description=description, 
    long_description = '',
    author = authors,
    author_email = authors_email,
    url = url,
    license = license,

    namespace_packages = ['openalea'],
    create_namespaces=True,
    zip_safe=False,

    packages=packages,

    package_dir=package_dir,

    # Add package platform libraries if any
    include_package_data=True,
    package_data = {'' : ['*.csv'],},

    # Dependencies
    setup_requires = ['openalea.deploy'],
    install_requires = ['openalea.core', 'pandas'],
    dependency_links = ['http://openalea.gforge.inria.fr/pi'],

    # entry_points
    entry_points = {
        "wralea": ['openalea.pandas = openalea.pandas_wralea'],
        },

    )
