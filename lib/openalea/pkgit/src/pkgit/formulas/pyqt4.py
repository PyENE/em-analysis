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
from pkgit.utils import option_to_python_path, option_to_sys_path, sh
from pkgit.formulas.qt4 import Qt4 as qt4
from pkgit.formulas.sip import Sip as sip_
import sys, os
from openalea.core.path import path, shutil

class Pyqt4(Formula):
    homepage        = "http://www.riverbankcomputing.com/software/pyqt/intro"
    description     = "PyQt is a set of Python v2 and v3 bindings for Digia's Qt application framework."
    authors         = "PyQt authors"
    license         = "GNU General Public License v3"
    download_url    = "http://downloads.sourceforge.net/project/pyqt/PyQt4/PyQt-4.10.3/PyQt-win-gpl-4.10.3.zip"
    download_name   = "pyqt4.zip"
    version         = "4.10.3"
    dependencies    = ["qt4", "sip"]
    DOWNLOAD = UNPACK = CONFIGURE = MAKE = MAKE_INSTALL = True
     
    def __init__(self, *args, **kwargs):
        super(Pyqt4, self).__init__(*args, **kwargs)
        # we install pyqt4 binaries in the qt bin installation directory to easily recover it
        # for the egg. The eggs are built in the historical layout used by openalea packagers.
        # This doesn't mean it's good. It doesn't mean it's bad though it does look a bit messy.
        qt4_    = qt4()
        sip     = sip_()
        self.install_bin_dir  = qt4_.install_bin_dir
        self.install_site_dir = path(self.installdir)/"site"
        self.install_sip_dir  = path(self.installdir)/"sip"
        self.inst_paths       = self.install_bin_dir, self.install_site_dir, self.install_sip_dir  
        self.sipsite          = sip.install_site_dir
        self.siphome          = sip.install_sip_dir
        
    @option_to_python_path("sipsite")
    @option_to_sys_path("siphome")
    def configure(self):
        cmd = sys.executable + " -S configure.py --confirm-license --no-designer-plugin -w -b %s -d %s -v %s "%self.inst_paths
        print
        print cmd
        print
        ret = sh(cmd) == 0
        self.patch_pyqt_config()
        return ret
        
    def extra_paths(self):
        return self.install_bin_dir

    def extra_python_paths(self):
        return self.install_site_dir

    def patch_pyqt_config(self):
        # 1) Patching pyqtconfig.py like we patch sipconfig 
        # (cf sip formula).
        # 2) We have problems in trying to build QtDesigner.
        # So, we try to work without QtDesigner but
        # option --no-designer-plugin in configure.py semms to not work.
        # We path QtDesigner/Makefile and qpy/Makefile .
        '''
        print
        print "Patch pyqtconfig"
        print
        
        header = """
import sipconfig
from sipconfig import pj as pj
from sipconfig import qtdev as qtdev
from sipconfig import qt as qt"""
        txt = ""
        with open("pyqtconfig.py") as f:
            txt = f.read()
        txt = txt.replace("import sipconfig", header)
        txt = re.sub(r"(\s*'pyqt_bin_dir':\s*)'[A-Z]:(\\\\|/).*'", r"\1pj(qtdev,'bin')", txt)
        txt = re.sub(r"(\s*'pyqt_mod_dir':\s*)'[A-Z]:(\\\\|/).*'", r"\1pj(qt,'PyQt4')", txt)
        txt = re.sub(r"(\s*'pyqt_sip_dir':\s*)'[A-Z]:(\\\\|/).*'", r"\1pj(qtdev,'sip')", txt)
        txt = re.sub(r"(\s*'qt_data_dir':\s*)'[A-Z]:(\\\\|/).*'",  r"\1qtdev.replace('\\\','/')", txt)
        txt = re.sub(r"(\s*'qt_dir':\s*)'[A-Z]:(\\\\|/).*'",       r"\1qt", txt)
        txt = re.sub(r"(\s*'qt_inc_dir':\s*)'[A-Z]:(\\\\|/).*'",   r"\1pj(qtdev, 'include')", txt)
        txt = re.sub(r"(\s*'qt_lib_dir':\s*)'[A-Z]:(\\\\|/).*'",   r"\1pj(qtdev, 'lib')", txt)
        txt = re.sub(r"(\s*'INCDIR_QT':\s*)'[A-Z]:(\\\\|/).*'",    r"\1pj(qtdev, 'include')", txt)
        txt = re.sub(r"(\s*'LIBDIR_QT':\s*)'[A-Z]:(\\\\|/).*'",    r"\1pj(qtdev, 'lib')", txt)
        txt = re.sub(r"(\s*'MOC':\s*)'[A-Z]:(\\\\|/).*'",          r"\1pj(qtdev, 'bin', 'moc.exe')", txt)
        txt = txt.replace("phonon QtDesigner QAxContainer", "phonon QAxContainer") # Try to remove QtDesigner
        shutil.copyfile( "pyqtconfig.py", "pyqtconfig.py.old" )
        with open("pyqtconfig.py", "w") as f:
            f.write(txt)
        '''
        print
        print "Patch Makefile"
        print
        shutil.copyfile("Makefile", "Makefile.old")
        txt = ""
        with open("Makefile") as f:
            txt = f.read()
        txt = txt.replace("	@$(MAKE) -C QtDesigner install", "")
        txt = txt.replace("	@$(MAKE) -C QtDesigner clean", "")
        txt = txt.replace("	@$(MAKE) -C QtDesigner", "")
        with open("Makefile", "w") as f:
            f.write(txt)        
        
        print
        print "Patch qpy/Makefile"
        print
        os.chdir("qpy")
        shutil.copyfile("Makefile", "Makefile.old")
        txt = ""
        with open("Makefile") as f:
            txt = f.read()
        txt = txt.replace("	@$(MAKE) -C QtDesigner install", "")
        txt = txt.replace("	@$(MAKE) -C QtDesigner clean", "")
        txt = txt.replace("	@$(MAKE) -C QtDesigner", "")
        with open("Makefile", "w") as f:
            f.write(txt)
        os.chdir("..")