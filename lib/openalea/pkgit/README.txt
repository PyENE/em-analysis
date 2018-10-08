Description
-------------

The PkgIt package is a package to help packaging dependencies and so to create releases. 

Quick Start
-----------

To package matplotlib:

>>> pkgit --package matplotlib

To see available formulas and corresponding versions:

>>> pkgit --versions

To see dependencies of a package:

>>> pkgit --deps qt4

To create a new formula:

>>> pkgit --create mynewdependency

To create a windows installer (after packaging):

>>> pkgit --wininst openalea

Download
----------

>>> svn co https://scm.gforge.inria.fr/svn/openalea/trunk/pkgit pkgit

Installation
------------

>>> python setup.py install

Requirements
------------

* Setuptools
* SVN
* python-requests
* path.py
* Scons >= 0.96.93
* SconsX
* OpenAlea.Deploy

Documentation
-------------
http://openalea.gforge.inria.fr/doc/openalea/pkgit/doc/_build/html/contents.html

