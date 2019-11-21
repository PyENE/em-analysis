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
from pkgit.formulas.mingw import Mingw as mingw
from openalea.core.path import path
import os

class Bisonflex(Formula):
    dependencies = ["mingw"]
    version      = "2.4.1"
    BDIST_EGG = True
    
    def setup(self):
        mingw_path = mingw().get_path()
        bison_path = path(mingw_path)/"msys"/"1.0"

        bindirs = {"bin": str(path(bison_path)/"bin")}
        incdirs = {"include": str(path(bison_path)/"include")}
        libdirs = {"lib": str(path(bison_path)/"lib")}

        # GET DATA FILES (share directory and subdirs)
        OLDDIR = os.getcwd()
        BISFLEXDIR = (path(bison_path)/"share").abspath()
        BISFLEXDIR = str(BISFLEXDIR).replace("\\", "/")
        os.chdir(BISFLEXDIR)
        raw_files = os.walk(BISFLEXDIR)
        data_files = []
        for i,j,k in raw_files:
            for f in k:
                # we want to reproduce the same hierarchy inside the egg.
                # as inside the BISFLEXDIR.
                rel_direc = path(i).relpath(BISFLEXDIR).replace("\\","/")
                file_ = unix_style_join( rel_direc, f)        
                data_files.append( ("share" if rel_direc == "." else str(path("share")/rel_direc),[str(path(file_).abspath())]) )
        os.chdir(OLDDIR)
        
        return dict( 
                    VERSION  = self.version,
                    BIN_DIRS = bindirs,
                    INC_DIRS = incdirs,
                    LIB_DIRS = libdirs,
                    DATA_FILES = data_files
                    )
                    
def unix_style_join(*args):
    l = len(args)
    if l == 1 : return args[0]
    
    ret = args[0]
    for i in range(1,l-1):
        ret += ("/" if args[i]!="" else "")+ args[i]
    
    if args[l-1] != "":
        ret += ("/" if args[l-2]!="" else "") + args[l-1]
        
    return ret