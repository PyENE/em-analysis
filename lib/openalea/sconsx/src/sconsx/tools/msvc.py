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
""" Visual Studio C++ configure environment. """

__license__ = "Cecill-C"
__revision__ = "$Id: msvc.py 3280 2011-05-27 12:54:36Z boudon $"


import os, sys
from openalea.sconsx.config import *


class Msvc:

   def __init__(self, config):
      self.name = 'msvc'
      self.config = config

   def option(self, opts):
      pass

   def update(self, env):
      """ Update the environment with specific flags """

      #env['MSVS_VERSION'] = '6.0'
      t = Tool('msvc')
      t(env)

      # /GR: enable C++ RTTI
      CCFLAGS = ['/MD','/GR','/EHsc']
      #CPPPATH = [r'C:\PROGRAM FILES\MICROSOFT VISUAL STUDIO\VC98\INCLUDE\STLPORT']
      CPPDEFINES = ['UNICODE']
      #LIBS = ['advapi32','uuid','stlport_vc6']

      if env["warnings"]:
         # TODO add warnings flags
         CCFLAGS += ['/W3']

      if env["debug"]:
         # Optimization
         # /Od2: disable optimizations
         CCFLAGS.extend(['/Od'])
         # language
         # /Zi enable debugging information
         CCFLAGS.extend(['/Zi'])
         # code generation
         # /GZ: enable runtime debug checks
         # /Gm: enable minimal rebuild
         CCFLAGS.extend(['/GZ','/Gm'])

         CPPDEFINES.append('_DEBUG')
      else:
         # Optimization
         # /O2: maximum speed
         # /ob2: inline expansion (n=2)
         CCFLAGS.extend(['/O2','/Ob2'])
         # code generation
         # /Gy: separate functions for linker
         # /GF: enable read-only string pooling
         # /GA: enable for Windows Application
         # /GR: enable C++ RTTI
         CCFLAGS.extend(['/Gy','/GF','/GA'])
         
         CPPDEFINES.append('NDEBUG')

      #env.AppendUnique(CPPPATH=CPPPATH)
      env.AppendUnique(CCFLAGS=CCFLAGS)
      env.AppendUnique(CPPDEFINES=CPPDEFINES)
      #env.AppendUnique(LIBS=LIBS)
      
      if 8 <= env['MSVS_VERSION'] < 10:
        # Bug fix with scons msvc manifest. Manifest will be included into the dll.
        env['LINKCOM'] = [env['LINKCOM'], 'mt.exe -nologo -manifest ${TARGET}.manifest -outputresource:$TARGET;1']
        env['SHLINKCOM'] = [env['SHLINKCOM'], 'mt.exe -nologo -manifest ${TARGET}.manifest -outputresource:$TARGET;2']


   def configure(self, config):
      pass

def create(config):
   " Create msvc tool "
   msvc = Msvc(config)

   return msvc

