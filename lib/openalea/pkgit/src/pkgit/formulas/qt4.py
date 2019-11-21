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
##############################
######### INSTALL QT #########
##############################
See more informations: http://qt-project.org/wiki/Building_Qt_Desktop_for_Windows_with_MinGW

Patch thanks to: http://qt-project.org/forums/viewthread/24950
(answer : April 17, 2013 Chris Kawa Chris Kawa)

######### CONFIGURE #########
Thanks to jom, we save half time during compilation.
jom link: http://download.qt-project.org/official_releases/jom/jom_1_0_13.zip
>>> Download jom
>>> Unpack jom.exe in ./src/qt4
>>> modify ./src/qt4/config.cache (cf. self.configure())
>>> ./src/qt4/configure.exe -redo

######### MAKE #########
>>> ./src/qt4/jom /W /S -j4

######### MAKE INSTALL #########
>>> make_install()
copy mingw32/bin/mingwm10.dll ./src/qt4/bin
copy mingw32/bin/libgcc_s_dw2-1.dll ./src/qt4/bin

######### MAKE QT CONF #########
>>> make_qt_conf() create file ./src/qt4/bin/qt.conf

#########################################################################
######### INSTALL OTHERS (SIP, PYQT4, QSCINTILLA, PYQSCINTILLA) #########
#########################################################################
>>> install_deps()

################################################
######### BDIST_EGG PYQT, QSCINTILLA, SIP #########
################################################
>>> setup()

#################################
######### BDIST_EGG QT4DEV #########
#################################
>>> cf formula qt4_dev
"""
from pkgit.formula import Formula
from pkgit.formulas.mingw import Mingw as mingw
from pkgit.formulas.mingw_rt import Mingw_rt as mingw_rt
from pkgit.utils import uj, recursive_glob_as_dict, \
recursive_copy, makedirs, Pattern, sh, eggify_formula
from openalea.core.path import path, shutil
import subprocess
import ConfigParser
import time
import os
from setuptools import find_packages
        
class Qt4(Formula):
    version = "4.8.5"
    ## with exe
    # download_url = "http://download.qt-project.org/official_releases/qt/4.8/4.8.5/qt-win-opensource-4.8.5-mingw.exe"
    # download_name  = "qt4.exe"
    #DOWNLOAD = INSTALL = CONFIGURE = BDIST_EGG = True
    ## with zip
    download_url = "http://download.qt-project.org/official_releases/qt/4.8/4.8.5/qt-everywhere-opensource-src-4.8.5.zip"
    download_name  = "qt4.zip"
    license = "General Public License V3"
    authors = "Riverbank Computing (Sip+PyQt4+QSCintilla) & Nokia (Qt4)"
    description = "Sip+PyQt4+QScintilla Runtime packaged as an egg for windows-gcc"
    dependencies = ["mingw", "mingw_rt"]
    DOWNLOAD = UNPACK = CONFIGURE = MAKE = MAKE_INSTALL = BDIST_EGG = True

    def __init__(self, *args, **kwargs):
        super(Qt4, self).__init__(*args, **kwargs)
        self.old_dir = os.getcwd()
        
        # define installation paths
        self.install_bin_dir = path(self.installdir)/"bin"
        self.install_dll_dir = path(self.installdir)/"dll"
        self.install_lib_dir = path(self.installdir)/"lib"
        self.install_src_dir = path(self.installdir)/"src"
        self.install_inc_dir = path(self.installdir)/"include"
        self.install_plu_dir = path(self.installdir)/"dll"
        self.install_plu_lib_dir = path(self.installdir)/"plugins_lib"
        self.install_mks_dir = path(self.installdir)/"mkspecs"
        self.install_tra_dir = path(self.installdir)/"translations"
        self.inst_paths      = [getattr(self, attr) for attr in dir(self) if attr.startswith("install_") and attr.endswith("_dir")]

    def configure(self):
        # new_env_vars
        cmd = "setx QMAKESPEC win32-g++"
        print cmd
        sh(cmd)
        cmd = "set QMAKESPEC=win32-g++"
        print cmd
        sh(cmd)
        cmd = "setx QTDIR %s" %self.installdir
        print cmd
        sh(cmd)
        cmd = "set QTDIR=%s" %self.installdir
        print cmd
        sh(cmd)

        config_txt="""
-platform
win32-g++
-release
-opensource
-shared
-nomake
demos
-nomake
examples
-fast
-sse2 
-3dnow
-declarative
-webkit
-no-vcproj
-no-cetest
-no-s60"""
        f = open("configure.cache", "w")
        f.write(config_txt)
        f.close()
        
        cmd = "configure.exe -redo"
        print
        print cmd
        print
        
        # PIPE is required or else pop.communicate won't do anything!
        pop = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        # give enough time for executable to load before it asks for license agreement.
        time.sleep(2)
        # accepts license agreement, also waits for configure to finish
        pop.communicate("y\r")
        return pop.returncode == 0    

    def make_install(self):
        for pth in self.inst_paths:
            makedirs(pth)
            
        # Copy mingw dll
        # More informations here: http://qt-project.org/wiki/Building_Qt_Desktop_for_Windows_with_MinGW
        mingw_bin_path = mingw().get_bin_path()
        shutil.copy(path(mingw_bin_path)/"mingwm10.dll", path(self.sourcedir)/"bin")    
        shutil.copy(path(mingw_bin_path)/"libgcc_s_dw2-1.dll", path(self.sourcedir)/"bin")    

        print "copy files for qt4"
        # copy installed binaries in temporary installdir
        recursive_copy( path(self.sourcedir)/"bin", self.install_bin_dir, Pattern.exe )
        # add a qt.conf file that tells qmake to look into
        # directories that are relative to the executable.
        with open( path(self.install_bin_dir)/"qt.conf", "w") as qtconf:
            qtconf.write("[Paths]")
        # copy dlls
        recursive_copy( path(self.sourcedir)/"bin", self.install_dll_dir, Pattern.dynlib )
        # copy libs
        recursive_copy( path(self.sourcedir)/"lib", self.install_lib_dir, Pattern.qtstalib )
        # copy src -- actually only header files in src --
        recursive_copy( path(self.sourcedir)/"src", self.install_src_dir, Pattern.qtsrc )
        # copy include
        recursive_copy( path(self.sourcedir)/"include", self.install_inc_dir, Pattern.qtinc )
        # copy plugins
        recursive_copy( path(self.sourcedir)/"plugins", self.install_plu_dir, Pattern.dynlib, flat=True )
        # copy plugins
        recursive_copy( path(self.sourcedir)/"plugins", self.install_plu_lib_dir, Pattern.qtstalib )
        # copy plugins
        recursive_copy( path(self.sourcedir)/"mkspecs", self.install_mks_dir, Pattern.qtmkspec )
        # copy translations
        recursive_copy( path(self.sourcedir)/"translations", self.install_tra_dir, Pattern.qttransl )
    
        self.make_qt_conf()
        self.install_deps()
        return True
 
    def extra_paths(self):
        return path(self.sourcedir)/"bin"
 
    def make_qt_conf(self, where=None):
        """ Patch qt *.exes and *.dlls so that they do not contain hard coded paths anymore. """
        print "Make qt conf"
        config = ConfigParser.RawConfigParser()
        sec = "Paths"
        config.add_section(sec)
        if where == None:
            config.set(sec, "Headers",	 "../include")
            config.set(sec, "Libraries", "../lib")
            config.set(sec, "Binaries",  "../bin")
            config.set(sec, "Plugins",   "../dll")
            #config.set(sec, "Imports"	"no idea")
            config.set(sec, "Data",      "..")
            config.set(sec, "Translations", "../translations")
        else:
            unix_installdir = self.installdir.replace("\\", "/")
            config.set(sec, "Headers",	 uj(unix_installdir, "include"))
            config.set(sec, "Libraries", uj(unix_installdir, "lib"))
            config.set(sec, "Binaries",  uj(unix_installdir, "bin"))
            config.set(sec, "Plugins",   uj(unix_installdir, "dll"))
            #config.set(sec, "Imports"	"no idea")
            config.set(sec, "Data",      unix_installdir )
            config.set(sec, "Translations", uj(unix_installdir, "translations")  )      
        # Writing our configuration file
        if where is None:
            where = self.install_bin_dir
        with open(path(where)/'qt.conf', 'w') as configfile:
            config.write(configfile)
        return True
 
    def install_deps(self):
        # Install dependencies before to create egg   
        temp_dir = os.getcwd()
        os.chdir(self.old_dir)

        eggify_formula("sip")
        eggify_formula("pyqt4")
        eggify_formula("qscintilla")
        eggify_formula("pyqscintilla")
        
        os.chdir(temp_dir)
 
    def setup(self):  
        from pkgit.formulas.pyqt4 import Pyqt4 as pyqt4
        from pkgit.formulas.pyqscintilla import Pyqscintilla as pyqscintilla
        from pkgit.formulas.sip import Sip as sip  

        pyqt4_ = pyqt4()
        pysci_ = pyqscintilla()
        sip_   = sip()
        # dlls are the union of qt dlls and plugins directories (which is actually the same!)
        # qscis apis are recursive from qt4 (need to list all files)        
        qscis    = recursive_glob_as_dict(pysci_.qsci_dir, Pattern.sciapi, strip_keys=True, prefix_key="qsci").items()
        extra_pyqt4_mods = recursive_glob_as_dict(path(pyqt4_.install_site_dir)/"PyQt4", Pattern.pyall, strip_keys=True, prefix_key="PyQt4").items()
        # print extra_pyqt4_mods
        sip_mods = recursive_glob_as_dict(sip_.install_site_dir, Pattern.pyall, strip_keys=True, levels=1).items()

        lib_dirs    = {"PyQt4": self.install_dll_dir}
        package_dir = {"PyQt4": path(pyqt4_.install_site_dir)/"PyQt4"}
        
        d  = dict( 
                    VERSION  = self.version,
                    PACKAGES = find_packages(pyqt4_.install_site_dir, "PyQt4"),
                    PACKAGE_DIRS = package_dir,
                    PACKAGE_DATA = {'' : [Pattern.pyext]},
                    
                    LIB_DIRS         = lib_dirs,
                    INC_DIRS         = None,
                    BIN_DIRS         = None,
                    DATA_FILES       = qscis+sip_mods+extra_pyqt4_mods,
                    INSTALL_REQUIRES = [mingw_rt().egg_name()]
                    )   
        return d