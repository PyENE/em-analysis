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
__revision__ = "$Id: $"

import sys, os
import datetime
from openalea.core.path import path, glob, shutil
from .utils import unpack as utils_unpack
from .utils import install as util_install
from .utils import in_dir, try_except, TemplateStr, sh, sj, makedirs
from .utils import Pattern, recursive_glob_as_dict, get_logger, url

logger = get_logger()   

############################################
# Formula                                  #
############################################
class Formula(object):
    """
    This class is the abstract class of all formulas.
    
    To create a formula, simply derive from this one, put it in directory 'formulas'
    and overload necessary parameters and methods.
    
    Attributes:
        
        * version:         Version of the dependency (not of the formula)
        * description:     Description of the dependency (not of the formula)
        * homepage:        Url of home-page of the dependency (not of the formula)
        * license:         License of the dependency (not of the formula)
        * authors:         Authors of the dependency (not of the formula)
        * dependencies:    List of dependencies of the formula
        * download_name:   Name of the local archive
        * download_url:    Url where to download sources (feel only if "DOWNLOAD = True")
        
    Flags to set to True if necessary:
    
        * DOWNLOAD 
        * UNPACK 
        * INSTALL 
        * CONFIGURE 
        * MAKE 
        * MAKE_INSTALL 
        * BDIST_EGG 
        * COPY_INSTALLER 
        * POST_INSTALL
        
    Special attribute:
    
        * __packagename__: Only usefull for package like Pillow which use another name for import (<<import Pil>> and not <<import Pillow>>)
    
    :warning: __init__ method create directories in disk.
    """
    
    version         = "1.0"  # Version of the dependency (not of the formula)
    description     = ""     # Description of the dependency (not of the formula)
    homepage        = ""     # Url of home-page of the dependency (not of the formula)
    license         = ""     # License of the dependency (not of the formula)
    authors         = ""     # Authors of the dependency (not of the formula)
    dependencies    = []     # List of dependencies of the formula
    download_name   = ""     # Name of the local archive
    download_url    = None   # Url where to download sources (feel only if "DOWNLOAD = True")
    __packagename__ = None   # Only for package like Pillow which use another name for import (<<import Pil>> and not <<import Pillow>>)
    _working_path  = os.getcwd()

    DOWNLOAD = UNPACK = INSTALL = CONFIGURE = MAKE = MAKE_INSTALL = BDIST_EGG = COPY_INSTALLER = POST_INSTALL = False
    
    def __init__(self,**kwargs):
        logger.debug("__init__ %s" %self.__class__)
        self.options = {} 
        
        self.dldir          = path(self._get_dl_path())
        self.archname       = path(self._get_dl_path())/self.download_name
        self.sourcedir      = path(self._get_src_path())/self.download_name
        self.sourcedir      = self.sourcedir.splitext()[0]
        self.installdir     = path( self._get_install_path())/self.download_name
        self.installdir     = self.installdir.splitext()[0]
        self.install_inc_dir = path(self.installdir)/"include"
        self.install_lib_dir = path(self.installdir)/"lib"    
        self.dist_dir       = path(self._get_dist_path())/"thirdpart"
        self.eggdir         = path(self._get_egg_path())/self.egg_name()
        self.setup_in_name  = path(__file__).abspath().dirname()/"setup.py.in"
        self.setup_out_name = path(self.eggdir)/"setup.py"
        self.use_cfg_login  = False #unused for the moment
        self.force          = False #Set to True t force re-download, re-build, re-package
        
        self._make_default_dirs()
        
        if (self.packaged()[0] is True) and (not self.force):
            DOWNLOAD = UNPACK = INSTALL = CONFIGURE = MAKE = MAKE_INSTALL = BDIST_EGG = COPY_INSTALLER = False

    def _default_substitutions_setup_py(self):
        """
        Default dict fill setup.py to create egg.
        
        :return: default dict to fill "setup.py" files
        """
        # if package is python and yet installed
        try:
            packages, package_dirs = self.find_packages_and_directories()
            install_dir = str(path(self.package.__file__).abspath().dirname())
            # py_modules = recursive_glob(self.install_dir, Pattern.pymod)
            data_files = recursive_glob_as_dict(install_dir,
                        ",".join(["*.example","*.txt",Pattern.pyext,"*.c",".1"])).items()
        # evreything else
        except:
            packages, package_dirs, data_files = None, None, None
                        
        d = dict ( NAME                 = self.egg_name(),
                   VERSION              = self.version,
                   THIS_YEAR            = datetime.date.today().year,
                   SETUP_AUTHORS        = "Openalea Team",
                   CODE_AUTHOR          = self.authors,
                   DESCRIPTION          = self.description,
                   HOMEPAGE             = self.homepage,
                   URL                  = self.download_url,
                   LICENSE              = self.license,
                   ZIP_SAFE             = False,
                   PYTHON_MODS          = None,
                   PACKAGE_DATA         = {},
                   INSTALL_REQUIRES     = None,
                   PACKAGES             = packages,
                   PACKAGE_DIRS         = package_dirs,
                   DATA_FILES           = data_files,
                   LIB_DIRS             = None,
                   INC_DIRS             = None,
                   BIN_DIRS             = None,
                  )
            
        lib = str(path(self.sourcedir)/'lib')
        inc = str(path(self.sourcedir)/'include')
        bin = str(path(self.sourcedir)/'bin')
        if path(lib).exists(): d['LIB_DIRS'] = {'lib' : lib }
        if path(inc).exists(): d['INC_DIRS'] = {'include' : inc }
        if path(bin).exists(): d['BIN_DIRS'] = {'bin' : bin }
        
        return d

    def get_dependencies(self):
        """
        :return: list of dependencies of the formula. If doesn't have, return "".
        """
        if self.dependencies is None:
            self.dependencies = ""
        return list(self.dependencies)
           
    def _download(self):
        if self.DOWNLOAD:
            logger.debug("==DOWNLOAD==") 
            # a formula with a none url implicitely means
            # the sources are already here because some
            # other formula installed it.
            # If not downloadable : do nothing
            if self.download_url is None:
                return True    
            dir=self._get_dl_path()
            # If already downloaded : do nothing
            if (self.download_name in os.listdir(dir)) and (not self.force):
                message = "%s already downloaded!" %self.download_name
                logger.debug(message) 
                return True
            # Else: download
            else:
                ret = url(self.download_url, dir=self._get_dl_path(), dl_name=self.download_name)
                logger.debug("Download %s" %ret)
                return bool(ret)
        return True
    
    def _unpack(self):
        if self.UNPACK:
            logger.debug("==UNPACK==") 
            # a formula with a none url implicitely means
            # the sources are already here because some
            # other formula installed it.
            # If not downloadable : do nothing
            if self.download_url is None:
                logger.debug("No url")
                ret = True
            if path(self.sourcedir).exists():
                # If already unpacked and size > 0 : do nothing
                if (path(self.sourcedir).getsize() > 0) and (not self.force):
                    message =  'already unpacked in %s' %repr(self.sourcedir)
                    logger.debug(message)
                    ret = True
                # If already unpacked but size = 0 : unpack
                else:
                    ret = self.unpack()
            # Else: unpack
            else:
                ret = self.unpack()
            logger.debug("Unpack %s" %ret)
            return ret 
        return True
            
    def _extend_sys_path(self):
        # TODO : check if it works...
        exp = self.extra_paths()
        if exp is not None:
            if isinstance(exp, tuple):
                exp = sj(exp)
                
            path_splited = os.environ["PATH"].split(";")
            # Check if not already set
            if not exp in path_splited:
                #os.environ["PATH"] = sj([exp,os.environ["PATH"]])
                old_path = os.environ["PATH"]
                
                os.environ["PATH"] += os.pathsep + exp

                # cmd = " PATH "
                # for e in exp.split(";"):
                    # cmd = cmd + "\"" + e + "\";"
                # cmd = cmd + "%PATH%"
                cmd = ""
                for e in exp.split(";"):
                    cmd = cmd + e + ";"
                cmd = cmd + old_path + "\""            
                
                # set temp PATH
                cmd1 = "SET PATH=\"" + cmd
                logger.debug( cmd1 )
                sh(cmd1)
                
                # set permanent PATH
                cmd2 = "SETX PATH \"" + cmd
                logger.debug( cmd2 )
                sh(cmd2)
            
        return True

    def _extend_python_path(self):
        # Use PYTHONPATH instead PYTHON_PATH

        exp = self.extra_python_paths()
        if exp is not None:
            if isinstance(exp, tuple):
                for e in exp:
                    e = path(e).normpath()
                    sys.path.extend(e)
                exp = sj(exp)
            elif isinstance(exp, str):
                exp = path(exp).normpath()
                sys.path.extend(exp.split(os.pathsep))

            path_splited = os.environ.get("PYTHONPATH","").split(";")
            # Check if not already set
            if not exp in path_splited:
                os.environ["PYTHONPATH"] = sj([exp,os.environ.get("PYTHONPATH","")])
                
                cmd = " PYTHONPATH "
                for e in exp.split(";"):
                    cmd = cmd + "\"" + e + "\";"
                cmd = cmd + "%PYTHONPATH%"
                
                # set temp PYTHON_PATH
                cmd1 = "SET" + cmd
                logger.debug( cmd1 )
                sh(cmd1)
                
                # set permanent PYTHONPATH
                cmd2 = "SETX" + cmd
                logger.debug( cmd2 )
                sh(cmd2)

        return True

    # -- Top level process, they delegate to abstract methods, try not to override --
    @in_dir("sourcedir")
    @try_except
    def _configure(self):
        if self.CONFIGURE:
            logger.debug("==CONFIGURE==") 
            self._extend_sys_path()
            self._extend_python_path()
            ret = self.configure()
            logger.debug("Configure %s" %ret)
            return ret
        return True
        
    @in_dir("sourcedir")
    @try_except
    def _make(self):
        if self.MAKE:
            logger.debug("==MAKE==") 
            ret = self.make()
            logger.debug("Make %s" %ret)
            return ret
        return True
        
    @in_dir("sourcedir")
    @try_except
    def _make_install(self):
        if self.MAKE_INSTALL:
            logger.debug("==MAKE__INSTALL==") 
            ret = self.make_install()
            logger.debug("Make_install %s" %ret)
            return ret 
        return True
        
    @in_dir("dldir") 
    @try_except
    def _install(self):
        if self.INSTALL:
            logger.debug("==INSTALL==") 
            ret = self.install()
            logger.debug("Install %s" %ret)
            return ret
        return True
        
    @try_except
    def _configure_script(self):
        with open( self.setup_in_name, "r") as input, \
             open( self.setup_out_name, "w") as output:
             
            conf = self._default_substitutions_setup_py()
            conf.update(self.setup())
            conf = dict( (k,repr(v)) for k,v in conf.iteritems() )
            template = TemplateStr(input.read())
            output.write(template.substitute(conf))
        return True

    @in_dir("eggdir")
    @try_except
    def _bdist_egg(self):
        if self.BDIST_EGG:
            logger.debug("==BDIST_EGG==") 
            ret = self._configure_script()     
            ret = ret & self.bdist_egg()
            
            if not ret:
                # If bdist_egg create an empty egg, remove empty egg
                egg = self._glob_egg()
                if egg is not None:
                    path(egg).removedirs()
                    logger.warnings("Can't eggify. Remove %s"%egg) 

            logger.debug("Bdist_egg %s" %ret)
            return ret
        return True
           
    @in_dir("dldir") 
    @try_except    
    def _copy_installer(self):
        if self.COPY_INSTALLER:
            logger.debug("==COPY_INSTALLER==") 
            ret = self.copy_installer()
            logger.debug("Copy_installer %s" %ret)
            return ret
        return True
        
    @in_dir("dist_dir") 
    @try_except  
    def _post_install(self):
        if self.POST_INSTALL:
            logger.debug("==POST INSTALL==") 
            ret = self.post_install()
            logger.debug("Post Install %s" %ret)
            return ret
        return True

    def unpack(self):
        """
        Unpack previously download sources from "download" repository into "source" repository.
        
        Works with ZIP, TGZ and TAR formats.
        
        Can be overloaded.
        
        :return:  True if success, else False
        """
        return utils_unpack(self.archname, self.sourcedir)
            
    def setup(self):
        """
        Return a dict to complete setup.py to create egg.
        
        Can be (and MUST be in many cases) overloaded.
        
        :return:  dict()
        """
        return(dict())

    # -- The ones you can override are these ones --
    def copy_installer(self):
        """
        Copy a previously downloaded installer file in dist repository.
        
        Can be overloaded.
        
        :return:  True
        """
        shutil.copy(self.download_name, path(self.dist_dir)/self.download_name)
        return True
    
    def extra_paths(self):
        """
        List paths to add to Windows PATH.
        
        Can be overloaded.
        
        :return: None
        """
        return None
        
    def extra_python_paths(self):
        """
        List paths to add to Windows PYTHONPATH.
        
        Can be overloaded.
        
        :return: None
        """
        return None 
        
    def install(self):
        """
        Install a previously downloaded file. Works only with file ".exe" and ".msi".
        
        Can be overloaded.
        
        :return:  True if success, else False
        """
        return util_install(self.download_name)

    def configure(self):
        """
        Use it to launch command "configure" in the building logic "configure", "make", "make install".
        
        Actually do nothing!
        
        Can be (and MUST be in many cases) overloaded.
        
        :return: True
        """
        return True
        
    def make(self):
        """
        Launch command "make" in the building logic "configure", "make", "make install".
        
        Use command mingw32-make
        
        Can be (and MUST be in many cases) overloaded.
        
        :return: True if success, else False
        """
        try:
            opt = str(self.options["jobs"])
        except:
            opt = None
            
        n = os.environ.get("NUMBER_OF_PROCESSORS")
        if opt:
            cmd = "mingw32-make -j " + str(self.options["jobs"])
        elif n > 1 :
            cmd = "mingw32-make -j " + str(n)
        else:
            cmd = "mingw32-make"
        print
        print cmd
        print
        logger.debug(cmd)  
        return sh( cmd ) == 0

    def make_install(self):
        """
        Launch command "make install" in the building logic "configure", "make", "make install".
        
        Use command mingw32-make install
        
        Can be (and MUST be in many cases) overloaded.
        
        :return: True if success, else False
        """
        return sh("mingw32-make install") == 0

    def _glob_egg(self):
        """
        Search egg
        """
        eggs = glob.glob( path(self.dist_dir)/(self.egg_name()+"*.egg") )
        return None if not eggs else eggs[0]    
        
    def bdist_egg(self):
        """
        Build egg.
        
        Use command python setup.py bdist_egg
        
        Can be overloaded.
        
        :return: True if success, else False
        """
        return sh(sys.executable + " setup.py bdist_egg -d %s"%(self.dist_dir,)) == 0
        
    def post_install(self):
        """
        Try to install egg, exe or msi after packaging.
        
        Search an egg, then an exe, then a msi.
        
        If it is an egg, use command alea_install -H None -f . mypackage.egg
        
        Can be overloaded.
        
        :return: True if success, else False
        """
        
        egg_search = self.egg_name() + "*"
        egg = glob.glob( path(".")/egg_search )
        if egg:
            egg = egg[0]
            cmd = "alea_install -H None -f . %s" %egg
            return sh(cmd) == 0
        else: 
            #
            name_search = "*" + self.name + "*.exe"
            name = glob.glob( path(".")/name_search )
            if not name:
                name_search = "*" + self.name + "*.msi"
                name = glob.glob( path(".")/name_search )
            
            if name:
                name = name[0]
                return util_install(name)
                
        return False
    
    def packaged(self):
        """
        :return: True if not yet packaged in dist repo. Else False
        """
        name_search = "*" + self.name + "*"
        name = glob.glob( path(self.dist_dir)/name_search )
        if name:
            return True, name
        return False, ""

    # @in_dir("eggdir")
    # @try_except
    # def _upload_egg(self):
        # if not self.options["login"] or not self.options["passwd"]:
            # self.use_cfg_login = True
            # ret = self.upload_egg()
            # if not ret:
                # warnings.warn("No login or passwd provided, skipping egg upload")
                # logger.warn( "No login or passwd provided, skipping egg upload" )
                # return Later
            # return ret
        # return self.upload_egg()
        
    # def upload_egg(self):
        # if not self.use_cfg_login:
            # opts = self.options["login"], self.options["passwd"], \
                    # self.egg_name(), "\"ThirdPartyLibraries\"", "vplants" if not self.options["release"] else "openalea"
            # return sh(sys.executable + " setup.py egg_upload --yes-to-all --login %s --password %s --release %s --package %s --project %s"%opts) == 0
        # else:
            # opts = self.egg_name(), "\"ThirdPartyLibraries\"", "vplants" if not self.options["release"] else "openalea"
            # return sh(sys.executable + " setup.py egg_upload --yes-to-all --release %s --package %s --project %s"%opts) == 0
            
    def conf_dict(self):
        """
        Use it to configure inno_setup during "pkgit --wininst".
        
        Cf. openalea.deploy.makeWinInstaller
        
        Can be overloaded if you want to wininst.
        
        :return: dict of configuration to generate windows installer with inno setup
        """
        return dict()
        
    def _make_default_dirs(self):
        """
        Create default directories:
        * source
        * install
        * download
        * egg
        * ...
        """
        dirs = [self._get_src_path(), self._get_install_path(), self.sourcedir, self._get_dl_path(),\
                self.dist_dir, self.eggdir, self.installdir]
        for dir in dirs:
            makedirs(dir)
        
        logger.debug("makedirs %s" %str(dirs))
    
    @property
    def package(self):
        """
        Import corresponding package.
        
        :return: imported package
        """
        return __import__(self.packagename)

    @property
    def packagename(self):
        """
        :return: self.__packagename__ or egg_name (str)
        """
        return self.__packagename__ or self.egg_name()
        
    @property
    def name(self):
        """
        Name of the package to work with.
        
        :return: name (str)
        """
        return self.__class__.__name__
    
    @classmethod
    def egg_name(cls):
        """
        Name of the corresponding egg.
        
        :return: name (str)
        """
        return cls.__name__.split("egg_")[-1]

    def _filter_packages(self, pkgs):
        parpkg = self.packagename + "."
        return [ p for p in pkgs if (p == self.packagename or p.startswith(parpkg))]

    def _find_packages(self):
        from setuptools import find_packages
        install_dir = path(self.package.__file__).abspath().dirname()
        pkgs   = find_packages( path(install_dir)/os.pardir )
        pkgs = self._filter_packages(pkgs)
        return pkgs

    def find_packages_and_directories(self):
        """
        Find packages thanks to setuptools and then fix corresponding directories names.
        
        :return: list(packages, dict(packages:directories))
        """
        pkgs = self._find_packages()
        dirs = {}
        install_dir = path(self.package.__file__).abspath().dirname()
        base = (path(install_dir)/os.pardir).abspath()
        for pk in pkgs:
            dirs[pk] =  path(base)/pk.replace(".", os.sep)
        return pkgs, dirs          
            
    #################################
    ## Get PATHs
    #################################
    def _get_working_path(self):
        return self._working_path
        
    def _get_dl_path(self):
        return path(self._get_working_path())/"download"
    
    def _get_src_path(self):
        return path(self._get_working_path())/"src"
    
    def _get_install_path(self):
        return path(self._get_working_path())/"install"
        
    def _get_egg_path(self):
        return path(self._get_working_path())/"egg"
        
    def _get_dist_path(self):
        return path(self._get_working_path())/"dist"