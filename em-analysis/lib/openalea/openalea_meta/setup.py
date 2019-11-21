# -*- coding: utf-8 -*-
__revision__ = "$Id: setup.py 4155 2014-03-19 15:42:23Z camillechambon $"

import os, sys
pj = os.path.join

from setuptools import setup, find_packages

from openalea.deploy.metainfo import read_metainfo
metadata = read_metainfo('metainfo.ini', verbose=True)
for key,value in metadata.iteritems():
    exec("%s = '%s'" % (key, value))


platform = sys.platform
if platform.startswith('win'):
    external_dependencies = ['matplotlib>=0.99.1',
                             'scipy>=0.7.1',
                             'numpy>=1.4.0',
                             'pandas>=0.10.0']
else:
    external_dependencies = ['matplotlib',
                             'scipy',
                             'numpy',
                             'pandas']

#if platform != 'darwin':
#    external_dependencies.append('PIL<=1.1.6')

alea_dependencies = [
'openalea.core >= 1.0.0',
'openalea.deploy >= 1.0.0',
'openalea.deploygui >= 1.0.0',
'openalea.grapheditor >= 1.0.0',
'openalea.misc >= 1.0.0',
'openalea.visualea >= 1.0.0',
'openalea.stdlib >= 1.0.0',
'openalea.sconsx >= 1.0.0',
'openalea.scheduler >= 1.0.0',
'openalea.numpy >= 1.0.0',
'openalea.pylab >= 1.0.0',
'openalea.image >= 1.0.0',
'openalea.pkgbuilder >= 1.0.0',
#'openalea.container >=2.0.1.dev', part of vplants 
#'openalea.mtg >=0.7.0.dev', part of vplants
'openalea.pandas >= 1.0.0',
]

install_requires = alea_dependencies

# Add dependencies on Windows and Mac OS X platforms
if 'win' in platform:
    install_requires += external_dependencies 

build_prefix = "build-scons"

setup(
    name = name,
    version = version,
    description = description,
    long_description = long_description,
    author = authors,
    author_email = authors_email,
    url = url,
    license = license,

    namespace_packages = ['openalea'],
    create_namespaces=False,
    zip_safe=False,

    packages=find_packages('src'),

    package_dir={"":"src" },

    #scons_scripts=['SConstruct'],

    # Add package platform libraries if any
    include_package_data=True,
    package_data = {'' : ['*.png']},
    # Dependencies
    setup_requires = ['openalea.deploy'],
    install_requires = install_requires,
    dependency_links = ['http://openalea.gforge.inria.fr/pi'],

    # entry_points
    entry_points = {"wralea": ['openalea = openalea']},
    )


