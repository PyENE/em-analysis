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
""" GMP configure environment. """

__license__ = "Cecill-C"
__revision__ = "$Id: gmp.py 3654 2012-10-02 08:59:51Z boudon $"

import os, sys
from openalea.sconsx.config import *
from os.path import join as pj

class GMP:
   def __init__(self, config):
      self.name = 'gmp'
      self.config = config
      self._default = {}


   def depends(self):
      return []


   def default(self):

      if isinstance(platform, Win32):
      
         self._default['flags'] = ''
         self._default['defines'] = ''

         try:
            cgalroot = os.environ['CGALROOT']
            self._default['include'] = pj(cgalroot,'auxiliary','gmp','include')
            self._default['libpath'] = pj(cgalroot,'auxiliary','gmp','lib')
            self._default['libs'] = 'libgmp-10'            
         except:
            try:
               import openalea.config as conf
               self._default['include'] = conf.include_dir
               self._default['libpath'] = conf.lib_dir
            except ImportError, e:
               try:
                  import pkg_resources as pkg
                  egg_env = pkg.Environment()
                  mingw_base = egg_env["mingw"][0].location
                  self._default['include'] = pj(mingw_base, "include")
                  self._default['libpath'] = pj(mingw_base, "lib")
               except Exception, e:
                  self._default['include'] = 'C:' + os.sep
                  self._default['libpath'] = 'C:' + os.sep
               
            self._default['libs'] = 'gmp'

      elif isinstance(platform, Posix):
         self._default['include'] = '/usr/include'
         self._default['libpath'] = '/usr/lib'
         self._default['libs'] = 'gmp'
         self._default['flags'] = ''
         self._default['defines'] = ''


   def option( self, opts):

      self.default()

      opts.AddVariables(PathVariable('gmp_includes', 
                     'GMP include files', 
                     self._default['include']),

         PathVariable('gmp_libpath', 
                     'GMP libraries path', 
                     self._default['libpath']),

         ('gmp_libs', 
           'GMP libraries', 
           self._default['libs']),
           
         ('gmp_flags', 
           'GMP compiler flags', 
           self._default['flags']),

         ('gmp_defines', 
           'GMP defines', 
           self._default['defines']),

         BoolVariable('WITH_GMP', 
           'Specify whether you want to compile your project with GMP', True)
     )


   def update(self, env):
      """ Update the environment with specific flags """
      if env['WITH_GMP'] :
        gmp_inc = env['gmp_includes']
        # if type(gmp_inc) == str:
          # gmp_inc = gmp_inc.split()
        #gmp_inc = gmp_inc[0]
        if not os.path.exists(os.path.join(gmp_inc,'gmp.h')):
          import warnings
          warnings.warn("Error: GMP headers not found. GMP disabled ...")
          env['WITH_GMP'] = False      
      if env['WITH_GMP']:
        env.AppendUnique(CPPPATH=[env['gmp_includes']])
        env.AppendUnique(LIBPATH=[env['gmp_libpath']])
        env.Append(CPPDEFINES='$gmp_defines')
        env.Append(CPPDEFINES='WITH_GMP')
        env.Append(CPPFLAGS='$gmp_flags')

        env.AppendUnique(LIBS=env['gmp_libs'])


   def configure(self, config):
      if not config.conf.CheckCXXHeader('gmp.h'):
        print "Error: GMP headers not found."
        exit()
        
         


def create(config):
   " Create gmp tool "
   gmp = GMP(config)

   deps= gmp.depends()
   for lib in deps:
      config.add_tool(lib)

   return gmp

