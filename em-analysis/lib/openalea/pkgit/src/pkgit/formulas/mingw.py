# -*- coding: utf-8 -*- 
# -*- python -*-
#
#       Formula file for pkgit
# 
#       pkgit: tool for dependencies packaging
#
#       Copyright 2013 INRIA - CIRAD - INRA
#
#       File author(s):
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
from __future__ import absolute_import
__revision__ = "$Id: $"

"""
HOW TO CREATE MINGW EGG
=======================

1. Download mingw-get-setup.exe at https://sourceforge.net/projects/mingw/files/latest/download

2. Install this packages thanks to the GUI:
    a. mingw32-gcc-fortran (bin)
    b. mingw32-gcc-g++ (bin)
    
    c. mingw32-gmp (dev)
    d. mingw32-mpfr (dev)
    e. mingw32-libz (dev)
    
    f. msys-bison (bin)
    g. msys-flex (bin)
    
OR with the CLI:
    a. mingw-get install gcc-fortran
    b. mingw-get install gcc-g++
    c. mingw-get install gmp
    d. mingw-get install mpfr
    e. mingw-get install libz
    f. mingw-get install msys-bison
    g. mingw-get install msys-flex
    
Here, we install Bison-Flex too.
"""

from pkgit.formula import Formula
from pkgit.utils import recursive_glob_as_dict, memoize, sh, makedirs, safe_rmdir
import os, sys
from re import compile as re_compile
from openalea.core.path import path
import subprocess
import time
  
class Mingw(Formula):
    download_url = "http://downloads.sourceforge.net/project/mingw/Installer/mingw-get-setup.exe?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fmingw%2F%3Fsource%3Ddirectory&ts=1380884282&use_mirror=freefr"
    download_name = "mingw-get-setup.exe"
    license = "PublicDomain for MingW runtime. GLP or LGPL for some libraries."
    authors = "The Mingw Project"
    description = "Mingw Runtime"
    version        = "5.1.4_4c"
    DOWNLOAD = INSTALL = CONFIGURE = BDIST_EGG = True
    
    def configure(self):
        """
        Will install mingw with gcc and other dependencies.
        More informations:
        http://www.mingw.org/wiki/InstallationHOWTOforMinGW
        
        :warning: will install much more than needed! And will be really heavy!
        Try to remove what is not necessary.
        For example, when installing gcc, it installs binutils. A big part of binutils is useless.
        """
        
        cmd_prefix = "mingw-get install "
        libs = ["gcc-fortran", "gcc-g++", "gmp", "mpfr", "zlib", "libz", "msys-bison", "msys-flex", "gcc", "mingw32-make"]
        libs += ["binutils", "mingw-runtime", "pthreads", "iconv", "gcc-core", "libiconv"]
        for lib in libs:
            cmd = cmd_prefix + lib
            sh(cmd)
            print(cmd)
        
        '''
        # Remove useless packages:
        cmd_prefix = "mingw-get remove "
        libs = ["binutils"]
        for lib in libs:
            cmd = cmd_prefix + lib
            sh(cmd)
            
        # mingw-get install --reinstall g++ 
        # avoid error?
        # gcc: fatal error: -fuse-linker-plugin, but liblto_plugin-0.dll not found
        '''
        
        return True 

    def extra_paths(self):
        """
        .. todo:: Replace "path set by hand" by "automatic path"
        """
        
        bin_path = "C:\\MinGW\\bin"
        return str(bin_path)
        
    def setup(self):
        mingwbase = self.get_path()
        if not path(mingwbase).exists():
            makedirs(path(mingwbase))
        subd  = os.listdir( mingwbase )
        safe_rmdir("EGG-INFO", subd)
        safe_rmdir("bin", subd)
        safe_rmdir("include", subd)
        data = []
        for dir in subd:
            dat = recursive_glob_as_dict(path(mingwbase)/dir, "*", strip_keys=True, prefix_key=dir).items()         
            data += [ (str(d), [str(f) for f in t if not f.endswith(".dll")]) for d,t in dat]
        bindirs = {"bin": str(self.get_bin_path())}
        incdirs = {"include": str(path(mingwbase)/"include")}   
        #libdirs = {"lib": str(path(mingwbase/"lib")}  
        return dict( 
                    VERSION  = self.version,
                    BIN_DIRS = bindirs,
                    INC_DIRS = incdirs,
                    LIB_DIRS = None,
                    DATA_FILES   = data,
                    )

    def get_bin_path(self):
        # works well ?
        if "win32" not in sys.platform:
            return "/usr/bin"
        if self.options.get("compiler"):
            v =  self.options["compiler"]
            if path(v).exists():
                return v
        else:
            return self.get_path()/"bin"  
            
    def get_path(self):
        from pkg_resources import get_distribution
        location = "c:\\MinGW"
        try:
            result = get_distribution('mingw')
            location = result.location
        except:
            location = "c:\\MinGW"
        
        return path(location)
    
    def is_installed(self):
        compiler = path(self.get_bin_path())/"gcc.exe"
        try:
            sh(compiler+" --version")
            return True
        except OSError:
            return False  
          
    def version_gt(self, version):
        return self.get_version() >= version
        
    @memoize("version")
    def get_version(self):
        pop = subprocess.Popen( path(self.get_bin_path())/"gcc --version",
                                           stdout=subprocess.PIPE)
        time.sleep(1)
        output = pop.stdout.read()
        reg = re_compile(r"(\d\.\d.\d)")
        return reg.search(output).group(1)