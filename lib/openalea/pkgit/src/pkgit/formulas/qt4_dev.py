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
from pkgit.utils import recursive_glob_as_dict, merge_list_dict, Pattern
from pkgit.formulas.qt4 import Qt4 as qt4
from pkgit.formulas.pyqt4 import Pyqt4 as pyqt4
from pkgit.formulas.sip import Sip as sip

class Qt4_dev(Formula):
    license = "General Public License V3"
    authors = "Riverbank Computing (Sip+PyQt4+QSCintilla) & Nokia (Qt4)"
    description = "Sip+PyQt4+QScintilla Development packaged as an egg for windows-gcc"
    dependencies = ["qt4"]
    version = qt4.version
    BDIST_EGG = True

    def setup(self):
        qt4_   = qt4()
        pyqt4_ = pyqt4()
        sip_   = sip()
        # binaries are the union of qt, pyqt and sip binaries 
        bin_dirs = {"bin":qt4_.install_bin_dir}
        # includes are recursive subdirectories and the union of qt and sip includes               
        incs = recursive_glob_as_dict( qt4_.install_inc_dir, Pattern.qtinc, strip_keys=True, prefix_key="include", dirs=True).items() + \
               recursive_glob_as_dict( sip_.install_inc_dir, Pattern.qtinc, strip_keys=True, prefix_key="include", dirs=True).items()
        inc_dirs = merge_list_dict( incs )
        # libs are recursive subdirectories of qt libs          
        libs = recursive_glob_as_dict(qt4_.install_lib_dir, Pattern.qtstalib, strip_keys=True, prefix_key="lib").items()
        # sip files are recursive subdirectories and the union of pyqt4 and...
        sips = recursive_glob_as_dict(pyqt4_.install_sip_dir, Pattern.sipfiles, strip_keys=True, prefix_key="sip").items()
        # sources are recursive subdirectories and the union of qt4 and that all (CPP have been removed)...
        srcs = recursive_glob_as_dict(qt4_.install_src_dir, Pattern.qtsrc, strip_keys=True, prefix_key="src").items()
        # tra files are recursive subdirectories in qt4
        tra = recursive_glob_as_dict(qt4_.install_tra_dir, Pattern.qttransl, strip_keys=True, prefix_key="translations").items()
        # mks files are recursive subdirectories in qt4
        mks = recursive_glob_as_dict(qt4_.install_mks_dir, Pattern.qtmkspec, strip_keys=True, prefix_key="mkspecs").items()        
        # plugins files are recursive subdirectories in qt4
        plu = recursive_glob_as_dict(qt4_.install_plu_lib_dir, Pattern.qtstalib, strip_keys=True, prefix_key="plugins").items()

        return dict( 
                    VERSION          = qt4_.version,                   
                    BIN_DIRS         = bin_dirs,
                    INC_DIRS         = inc_dirs,
                    DATA_FILES       = libs+sips+srcs+tra+mks+plu,
                    INSTALL_REQUIRES = [qt4_.egg_name()]
                    )         