# -*-python-*-
#-------------------------------------------------------------------------------
#
#   OpenAlea.SConsX: SCons extension package for building platform
#                    independant packages.
#
#   Copyright 2006-2009 INRIA - CIRAD - INRA  
#
#   File author(s): Christophe Pradal <christophe.prada@cirad.fr>
#
#   Distributed under the Cecill-C License.
#   See accompanying file LICENSE.txt or copy at
#       http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#   OpenAlea WebSite : http://openalea.gforge.inria.fr
#
#-------------------------------------------------------------------------------
""" QT4 configure environment. """

__license__ = "Cecill-C"
__revision__ = "$Id: qt4.py 4078 2014-02-04 16:05:11Z gbaty $"

import os, sys
from openalea.sconsx.config import *
from os.path import join as pj

exists = os.path.exists

class QT:
    def __init__(self, config):
        self.name = 'qt'
        self.config = config
        self._default = {}


    def default(self):

        qt_dir = os.getenv("QTDIR")
        qt_lib = '$QTDIR/lib'
        qt_bin = '$QTDIR/bin'
        qt_inc = '$QTDIR/include'

        if isinstance(platform, Linux):
            # Use LSB spec
            qt_dir = '/usr'
            qt_bin = '/usr/bin'
            qt_inc = '/usr/include/qt4'
            qt_lib = '/usr/lib'
        elif not qt_dir:
            try: 
                if isinstance(platform, Win32) or isinstance(platform, Darwin):
                    # Try to use openalea egg
                    from openalea.deploy import get_base_dir
                    qt_dir = get_base_dir("qt4-dev")
            except:
                if isinstance(platform, Win32):
                    try:                 
                        from openalea.deploy import get_base_dir
                        qt_dir = get_base_dir("qt4")
                    except:                                             
                        # Try to locate bin/moc in PATH
                        qt_dir = find_executable_path_from_env("moc.exe", strip_bin=True)
                
                elif isinstance(platform, Posix):
                    qt_dir = pj('/usr', 'lib', 'qt4')
                    if not exists(pj(qt_dir, 'bin')):
                        # Use LSB spec
                        qt_dir = '/usr'
                        qt_bin = '/usr/bin'
                        qt_inc = '/usr/include/qt4'
                        qt_lib = '/usr/lib'

        self._default["QTDIR"] = qt_dir
        self._default["QT4_BINPATH"] = qt_bin
        self._default["QT4_CPPPATH"] = qt_inc
        self._default["QT4_LIBPATH"] = qt_lib


    def option( self, opts):

        self.default()

        opts.Add(('QTDIR', 'QT directory', 
                    self._default['QTDIR']))
        opts.Add(('QT4_BINPATH', 'QT binaries path.', 
                    self._default['QT4_BINPATH']))
        opts.Add(('QT4_CPPPATH', 'QT4 includes path.', 
                    self._default['QT4_CPPPATH']))
        opts.Add(('QT4_LIBPATH', 'QT4 lib path.', 
                    self._default['QT4_LIBPATH']))


    def update(self, env):
        """ Update the environment with specific flags """

        t = Tool('qt4', toolpath=[getLocalPath()])
        t(env)
        env.Replace(QT4_UICDECLPREFIX='')
        
        libpath=str(env.subst(env['QT4_LIBPATH']))

        if isinstance(platform, Win32):
            env.AppendUnique(CPPDEFINES=['QT_DLL'])

    def configure(self, config):
        pass

def create(config):
    " Create qt tool "
    qt = QT(config)

    return qt

