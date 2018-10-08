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
""" Python configure environment. """

__license__ = "Cecill-C"
__revision__ = "$Id: python.py 4080 2014-02-05 12:37:40Z jcoste $"


import os, sys
from openalea.sconsx.config import *
from distutils.sysconfig import *
pj = os.path.join

class Python:
   def __init__(self, config):
      self.name = 'python'
      self.config = config
      self._default = {}


   def default(self):

      self._default['include'] = get_python_inc(plat_specific=1)
      if isinstance(platform, Win32):
          lib_dir = pj(PREFIX,"libs")
          if not os.path.exists(lib_dir):
              # case with virtual env...
              lib_dir = pj(os.path.dirname(get_config_var('LIBDEST')),'libs')
          self._default['libpath'] = lib_dir
      elif isinstance(platform, Darwin):
         lib_dir = get_config_var('LIBPL')
         self._default['libpath'] = lib_dir
      else:
         self._default['libpath'] = '/usr/lib'


   def option( self, opts):

      self.default()

      opts.AddVariables(
         PathVariable('python_includes', 'Python include files', 
          self._default['include']),

         PathVariable('python_libpath', 'Python library path', 
         self._default['libpath'])
        )


   def update(self, env):
      """ Update the environment with specific flags """

      env.AppendUnique(CPPPATH=[env['python_includes']])
      
      if isinstance(platform, Win32):
          version = "%d%d" % (sys.version_info.major,sys.version_info.minor)
          pylib = 'python' + version          
          env.AppendUnique(LIBS=[pylib])
          env.AppendUnique(LIBPATH=[env['python_libpath']])
      
      elif isinstance(platform, Darwin):
          # hack to not use python system
          version = "%d.%d" % (sys.version_info.major,sys.version_info.minor)
          pylib = 'python' + version
          pylib = os.path.join(env['python_libpath'],'lib'+pylib+'.dylib')
          env.AppendUnique(LINKFLAGS=[pylib])
      else:
          pylib = 'python' + get_config_var('VERSION')
          env.AppendUnique(LIBS=[pylib])
          env.AppendUnique(LIBPATH=[env['python_libpath']])


   def configure(self, config):
      if not config.conf.CheckCXXHeader('Python.h'):
         print "Error: Python.h not found, probably failure in automatic python detection"
         sys.exit(-1)


def create(config):
   " Create python tool "
   python = Python(config)

   return python

