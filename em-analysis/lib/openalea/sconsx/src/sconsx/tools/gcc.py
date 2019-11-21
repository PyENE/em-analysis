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
""" Gcc configure environment. """

__license__ = "Cecill-C"
__revision__ = "$Id: gcc.py 3121 2011-02-07 18:06:25Z pradal $"

import os, sys
from openalea.sconsx.config import *


class Gcc:

   def __init__(self, config):
      self.name = 'gcc'
      self.config = config


   def option( self, opts):
      pass

   def update(self, env):
      """ Update the environment with specific flags """

      t = Tool('gcc')
      t(env)

      CCFLAGS = []
      CXXFLAGS = []
      if env["warnings"]:
         CCFLAGS += ['-W', '-Wall']
         CXXFLAGS += ['-W', '-Wall']

      if env["debug"]:
         CCFLAGS.extend(['-g'])
         CXXFLAGS.extend(['-g'])
      else:
         CCFLAGS.extend(['-DNDEBUG', '-O2'])
         CXXFLAGS.extend(['-DNDEBUG', '-O2'])

      env.AppendUnique(CCFLAGS=CCFLAGS)
      env.AppendUnique(CXXFLAGS=CXXFLAGS)


   def configure(self, config):
      pass

def create(config):
   " Create gcc tool "
   gcc = Gcc(config)

   return gcc

