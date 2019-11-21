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
from pkgit.utils import sh, option_to_sys_path, apply_patch_from_string
from pkgit.formulas.qt4 import Qt4 as qt4
import sys, os
from openalea.core.path import path, shutil

class Sip(Formula):
    download_url = "http://downloads.sourceforge.net/project/pyqt/sip/sip-4.15.2/sip-4.15.2.zip"
    download_name  = "sip.zip"
    version = "4.15.2"
    dependencies = ['bisonflex'] 
    DOWNLOAD = UNPACK = CONFIGURE = MAKE = MAKE_INSTALL = True

    def __init__(self, *args, **kwargs):
        super(Sip, self).__init__(*args, **kwargs)
        # we install pyqt4 binaries in the qt bin installation directory to easily recover it
        # for the egg. The eggs are built in the historical layout used by openalea packagers.
        # This doesn't mean it's good. It doesn't mean it's bad though it does look a bit messy.
        qt4_ = qt4()
        self.install_bin_dir  = qt4_.install_bin_dir
        self.install_site_dir = path(self.installdir)/"site"
        self.install_inc_dir  = path(self.installdir)/"include"
        self.install_sip_dir  = path(self.installdir)/"sip"

        self.inst_paths = self.install_bin_dir, self.install_site_dir, self.install_inc_dir, \
                          self.install_sip_dir

    @option_to_sys_path("bisonflex_path")
    def configure(self):
        if (path(self.sourcedir)/"configure.py").exists():
            # The -S flag is needed or else configure.py
            # sees any existing sip installation and can fail.
            cmd = sys.executable + " -S configure.py --platform win32-g++ -b %s -d %s -e %s -v %s"%self.inst_paths
            print
            print cmd
            print
            ret = sh(cmd) == 0
        else:
            #if configure.py doesn't exist then we might
            #be using a zipball retreived directly from
            #sip's mercurial repository. This type of source
            #needs a step before actually calling configure.py
            if path("build.py").exists():
                print "Will try to build sip from mercurial source zipball"
                try:
                    #We need bison and flex
                    sh("bison.exe")
                except:
                    print "Could not find bison flex, use --bisonflex"
                    return False
                apply_patch_from_string( PATCH )
                sh(sys.executable + " -S build.py prepare")
                ret = self.configure()
            else:
                #we don't have a clue of what type of source we're in
                #so dying cleanly can seem like a good option:
                return False
        self.patch_sip_config()
        return ret
                
    def setup(self):
        return dict( 
                    INSTALL_REQUIRES = ["bisonflex"],
                    ) 
                    
    def patch_sip_config(self):
        # Patching sipconfig.py so that its
        # paths point to the qt4 egg path we are building.
        # Feel free to do better
        
        '''
        qt4_ = qt4()
        
        header = """
import re
from openalea.core.path import path

# HACK paths
qtdev = os.environ.get('QTDIR') if 'QTDIR' in os.environ else r'%s'
sip_bin     = '%s'
sip_include = '%s'
qt          = '%s'

try:
    from pkg_resources import Environment
    env = Environment()
    if 'qt4' in env:
        qt = env['qt4'][0].location # Warning: 0 is the active one
    if 'qt4-dev' in env:
        qtdev       = env['qt4-dev'][0].location # Warning: 0 is the active one
        sip_bin     = path(qtdev)/'bin'/'sip.exe'
        sip_include = path(qtdev)/'include'
except:
    pass"""%(qt4_.sourcedir.replace("\\", "/"), path(qt4_.install_bin_dir)/"sip".replace("\\", "/"), self.install_inc_dir.replace("\\", "/"), qt4_.sourcedir.replace("\\", "/"))

        txt = ""
        print "sip patching", os.getcwd()
        with open(path(self.sourcedir)/"sipconfig.py") as f:
            txt = f.read()

        # inject our new header
        txt = txt.replace("import re", header)

        prefix = sys.prefix.replace("\\", r"\\\\")
        # Evil massive regexp substitutions. RegExp are self-explanatory! Just kidding...
        txt = re.sub(r"(\s*'default_bin_dir':\s*)'%s'"%prefix,    r"\1sys.prefix", txt)
        txt = re.sub(r"(\s*'default_mod_dir':\s*)'%s.*'"%prefix,  r"\1path(sys.prefix)/'Lib'/'site-packages'", txt)
        txt = re.sub(r"(\s*'default_sip_dir':\s*)'[A-Z]:\\\\.*'", r"\1path(qtdev)/'sip'", txt)
        txt = re.sub(r"(\s*'py_conf_inc_dir':\s*)'%s.*'"%prefix,  r"\1path(sys.prefix)/'include'", txt)
        txt = re.sub(r"(\s*'py_inc_dir':\s*)'%s.*'"%prefix,       r"\1path(sys.prefix)/'include'", txt)
        txt = re.sub(r"(\s*'py_lib_dir':\s*)'%s.*'"%prefix,       r"\1path(sys.prefix)/'libs'", txt)
        txt = re.sub(r"(\s*'sip_bin':\s*)'[A-Z]:\\\\.*'",         r"\1sip_bin", txt)
        txt = re.sub(r"(\s*'sip_inc_dir':\s*)'[A-Z]:\\\\.*'",     r"\1sip_include", txt)
        txt = re.sub(r"(\s*'sip_mod_dir':\s*)'[A-Z]:\\\\.*'",     r"\1qt", txt)

        shutil.copyfile( path(self.sourcedir)/"sipconfig.py", path(self.sourcedir)/"sipconfig.py.old" )
        
        with open( path(self.sourcedir)/"sipconfig.py", "w") as f:
            f.write(txt)
        '''
        try:
            os.makedirs(self.install_site_dir)
        except:
            pass
        shutil.copyfile( path(self.sourcedir)/"sipconfig.py", path(self.install_site_dir)/"sipconfig.py" )
                
    def extra_paths(self):
        return self.sourcedir, path(self.sourcedir)/"sipgen"

    def extra_python_paths(self):
        return self.sourcedir, path(self.sourcedir)/"siplib"

PATCH = """
--- ./build.py	Mon Oct 24 10:03:02 2011
+++ ./build.py	Thu Apr 05 21:42:06 2012
@@ -188,13 +188,31 @@
         release_suffix = "-unknown"
         version = None
 
-        parts = name.split('-')
-        if len(parts) > 1:
-            name = parts[-1]
+        hg_archival = os.path.join(_RootDir, ".hg_archival.txt")
+        if os.path.exists(hg_archival):            
+            # we might be able to get the tag
+            # from the hg_archival file!
+            print "Using hg_archival"
+            f = open(hg_archival)
+            lines = f.readlines()
+            f.close()
+            hg_values = dict( tuple(item.strip() for item in line.split(":")) for line in lines )
+            version   = hg_values.get("tag")
+            if version is not None:
+                version = version.split(".")
+                if len(version) == 2:
+                    version += 0,
+                version = tuple( int(i) for i in version )
+            release_suffix = ""
+        
+        if version is None:
+            parts = name.split('-')
+            if len(parts) > 1:
+                name = parts[-1]
 
-            if len(name) == 12:
-                # This is the best we can do without access to the repository.
-                release_suffix = '-' + name
+                if len(name) == 12:
+                    # This is the best we can do without access to the repository.
+                    release_suffix = '-' + name
 
     # Format the results.
     if version is None:
"""