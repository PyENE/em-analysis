# -*- coding: utf-8 -*-

"""setup file for core package"""
__revision__ = "$Id: setup.py 2242 2010-02-08 17:03:26Z cokelaer $"

import os
from setuptools import setup
pj = os.path.join


# to get the version
# execfile("src/core/version.py")

from openalea.deploy.metainfo import read_metainfo
metadata = read_metainfo('metainfo.ini', verbose=True)
for key,value in metadata.iteritems():
    exec("%s = '%s'" % (key, value))


setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    author=authors,
    author_email=authors_email,
    url=url,
    license=license,

    namespace_packages = ['openalea'],
    create_namespaces = True,
    zip_safe = False,
    include_package_data = True,

    packages = [ 'openalea.core', 'openalea.core.graph', 'openalea.core.algo', 'openalea.core.system',
                'openalea.core.graph.interface' ],
    
    package_dir = { 'openalea.core' : pj('src','core'),
                    'openalea.core.system' : pj('src','core', 'system'),
                    'openalea.core.algo' : pj('src','core', 'algo'),
                    'openalea.core.graph' : pj('src','core', 'graph'),
                    'openalea.core.graph.interface' : pj('src', 'core', 'graph','interface'),
                    '':'src',
                  },

    # Dependencies
    setup_requires = ['openalea.deploy'],
    install_requires = [],
    dependency_links = ['http://openalea.gforge.inria.fr/pi'],

    # entry_points
    entry_points = {
              "wralea": ["openalea.flow control = openalea.core.system",],
              "console_scripts": ["alea = openalea.core.alea:main"],
              },


    )


