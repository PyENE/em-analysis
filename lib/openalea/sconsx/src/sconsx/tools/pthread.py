# -*-python-*-
#--------------------------------------------------------------------------------
#
#       OpenAlea.SConsX: SCons extension package for building platform
#                        independant packages.
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA  
#
#       File author(s): Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
#--------------------------------------------------------------------------------
""" Pthread configure environment. """

__license__ = "Cecill-C"
__revision__ = "$Id: pthread.py 2247 2010-02-08 17:14:26Z cokelaer $"


import os, sys
from openalea.sconsx.config import *


class Pthread:
   def __init__(self, config):
      self.name = 'pthread'
      self.config = config
      self._default = {}


   def default(self):

      self._default['include'] = '/usr/include'
      self._default['lib'] = '/usr/lib'



   def option( self, opts):

      self.default()

      opts.AddVariables(
         PathVariable('pthread_includes', 'pthread include files', 
                     self._default['include']),
         PathVariable('pthread_lib', 'pthread libraries path', 
                     self._default['lib']) 
     )



   def update(self, env):
      """ Update the environment with specific flags """

      env.AppendUnique(CPPPATH=[env['pthread_includes']])
      env.AppendUnique(LIBPATH=[env['pthread_lib']])
      env.AppendUnique(LIBS=['pthread'])



   def configure(self, config):
      if not config.conf.CheckCHeader('pthread.h'):
         print """Error: pthread.h not found !!!
         Please install pthread and start again."""
         sys.exit(-1)


def create(config):
   " Create pthread tool "
   pthread = Pthread(config)

   return pthread

