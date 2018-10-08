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

from pkgit.formula import Formula
from pkgit.utils import sh, ascii_file_replace, recursive_glob_as_dict, merge_list_dict, Pattern
from pkgit.formulas.mingw_rt import Mingw_rt as mingw_rt
from openalea.core.path import path
import sys
from re import compile as re_compile
import re

class Boost(Formula):
    ## 1.54.0 make an error during "make_install()" and seems to not work (ex : cgal)...
    ## So use 1.48.0
    #version = "1.54.0"
    #download_url = "http://switch.dl.sourceforge.net/project/boost/boost/1.54.0/boost_1_54_0.zip"
    version = "1.48.0"
    download_url = "http://switch.dl.sourceforge.net/project/boost/boost/1.48.0/boost_1_48_0.zip"
    
    download_name  = "boost.zip"
    license = "Boost Software License 1.0"
    authors = "Boost contributors"
    description = "Windows gcc libs and includes of Boost"
    homepage = "http://www.boost.org/"
    DOWNLOAD = UNPACK = MAKE_INSTALL = BDIST_EGG = POST_INSTALL = True

    def __init__(self, **kwargs):
        super(Boost, self).__init__(**kwargs)
        self.install_inc_dir = path(self.installdir)/"include"
        self.install_lib_dir = path(self.installdir)/"lib"  
           
    #bjam configures, builds and installs so nothing to do here
    def make_install(self):
        print "Make install"
    
        # it is possible to bootstrap boost if no bjam.exe is found:
        if not (path(self.sourcedir)/"bjam.exe").exists() :
            print "Call bootstrap.bat"
            #mingw_path = r"c:/Python27/Lib/site-packages/mingw-5.2-py2.7-win32.egg/" 
            #mingw_path = r"c:/MinGW/" 
            #if sh("bootstrap.bat mingw --toolset-root=%s"%(mingw_path)) != 0:
            if sh("bootstrap.bat mingw") != 0:
                return False
            else:
                # The Bootstrapper top-level script ignores that gcc
                # was used and by default says it's msvc, even though
                # the lower level scripts used gcc.
                ascii_file_replace( "project-config.jam",
                                    "using msvc",
                                    "using gcc")
        # try to fix a bug in python discovery which prevents
        # bjam from finding python on Windows NT and old versions.
        pyjam_pth = path("tools")/"build"/"v2"/"tools"/"python.jam"
        ascii_file_replace(pyjam_pth,
                           "[ version.check-jam-version 3 1 17 ] || ( [ os.name ] != NT )",
                           "[ version.check-jam-version 3 1 17 ] && ( [ os.name ] != NT )")

        paths = str(self.installdir), str(path(sys.prefix)/"include"), str(path(sys.prefix)/"libs")
        cmd = "bjam --prefix=%s --without-test --layout=system"
        cmd += " variant=release link=shared threading=multi runtime-link=shared toolset=gcc"
        cmd += " include=%s library-path=%s install"
        cmd %= paths
        print
        print cmd
        print
        return sh(cmd) == 0
        
    def setup(self):
        version_re  = re_compile("^.*BOOST_VERSION\s:\s([\d\.]{4,8}).*$", re.MULTILINE|re.DOTALL)
        incs = recursive_glob_as_dict( str(self.install_inc_dir), Pattern.qtinc, strip_keys=True, prefix_key="include", dirs=True).items()
        inc_dirs = merge_list_dict( incs )
        # get the version from Jamroot file
        version = "UNKNOWN"        
        with open( path(self.sourcedir)/"Jamroot" ) as f:
            txt = f.read()
            se = version_re.search(txt)
            if se:
                version = se.groups()[0]
        lib_dirs    = {"lib": str(self.install_lib_dir)}
        return dict( 
                    VERSION          = version,                 
                    LIB_DIRS         = lib_dirs,
                    INC_DIRS         = inc_dirs,
                    BIN_DIRS         = None,                
                    INSTALL_REQUIRES = [mingw_rt.egg_name()]
                    )  