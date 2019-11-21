# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2014 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
"""
Working with Project class
--------------------------

You can work directly on project:

    >>> from openalea.vpltk.project import Project
    >>> # Get the correct path
    >>> from openalea.deploy.shared_data import shared_data
    >>> from openalea import oalab
    >>> path_of_my_proj = shared_data(oalab)
    >>> # Real work on project:
    >>> project1 = Project(name="mynewproj", projectdir=path_of_my_proj)
    >>> project1.rename("project", "mynewproj", "hello_project")
    >>> project1.start()

Change metadata:

    >>> project1.authors = "OpenAlea Consortium and John Doe"
    >>> project1.description = "Test project concept with numpy"
    >>> project1.long_description = 'This project import numpy. Then, it create and display a numpy eye. We use it to test concept of Project.'

... project file, models, ... :

    >>> success = project1.add(category="model", name="hello.py", value="print('Hello World')")
    >>> project1.description = "This project is used to said hello to everyone"
    >>> success = project1.add("startup", "begin_numpy", "import numpy as np")
    >>> success = project1.add("model", "eye.py", "print np.eye(2)")
    >>> project1.rename("model", "eye", "eye_numpy")


Creation and Manipulation with Project Manager
----------------------------------------------

Or, you can create or load a *project* thanks to the *project manager*.
    >>> from openalea.vpltk.project import ProjectManager
    >>> project_manager = ProjectManager()

Discover available projects
    >>> project_manager.discover()
    >>> list_of_projects = project_manager.projects

Create project in default directory or in specific one
    >>> p1 = project_manager.create('project1')
    >>> p2 = project_manager.create(name='project2', projectdir=".")

Load project from default directory
    >>> p3 = project_manager.load('sum')

Load project from a specific directory
    >>> oalab_dir = shared_data(oalab)
    >>> p4 = project_manager.load('sum', oalab_dir)

Load
    >>> project2 = project_manager.load("sum")

Run startup
    >>> project2.start()

Get model
    >>> model = project2.model("sum_int")

Search other projects
---------------------

To search projects that are not located inside default directories:
    >>> project_manager.find_links.append('/path/to/search/projects')
    >>> project_manager.discover()
    >>> list_of_projects = project_manager.projects

"""
from openalea.vpltk.project.project import Project
from openalea.vpltk.project.manager import ProjectManager
