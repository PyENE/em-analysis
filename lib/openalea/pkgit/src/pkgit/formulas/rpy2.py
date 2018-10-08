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
from pkgit.utils import sh, apply_patch_from_string, Pattern
from openalea.core.path import path
import sys

class Rpy2(Formula):
    version         = "2.3.6"
    revision        = "RELEASE_2_3_6"
    download_url    = "https://bitbucket.org/lgautier/rpy2/get/"+revision+".zip"
    download_name   = "rpy2.zip"
    homepage        = "http://rpy.sourceforge.net"
    license         = "AGPLv3.0 (except rpy2.rinterface: LGPL)"
    authors         = "Laurent Gautier"
    description     = "Unofficial Windows gcc libs and includes of rpy2"
    dependencies    = ["r"]
    DOWNLOAD = UNPACK = MAKE = MAKE_INSTALL = BDIST_EGG = True

    def setup(self):
        from setuptools import find_packages
        return dict(URL          = self.homepage,
                    PACKAGES     = find_packages(self.installdir,"rpy2"),
                    PACKAGE_DIRS = { "rpy2": str(path(self.installdir)/"rpy2") },
                    VERSION      = self.version+".rev"+self.revision,
                    PACKAGE_DATA = {'' : [Pattern.pyext]},
                    LIB_DIRS     = None,
                    INC_DIRS     = None,
                    BIN_DIRS     = None,
                    )
        
    def make(self):
        # apply_patch_from_string( PATCH )
        
        # sys.path.append("C:\\Program Files\\R\\R-2.15.3")
        # sys.path.append("C:\\Program Files\\R\\R-2.15.3\\bin")
        # sys.path.append("C:\\Program Files\\R\\R-2.15.3\\bin\\i386")
        # sys.path.append("C:\\Program Files\\R\\R-2.15.3\\bin\\i386\\R")
        # sys.path.append("C:\\Program Files\\R\\R-2.15.3\\bin\\i386\\R.exe")
        cmd = "set R_HOME=C:\\Program Files\\R\\R-2.15.3\\bin\\i386\\"
        cmd = "set PATH=R_HOME;%PATH%"
        sh(cmd)
        
        cmd = sys.executable + ' setup.py build_ext --compiler=mingw32'
        print cmd
        return sh(cmd) == 0
        
    def make_install(self):
        sys.path.append("C:\\Program Files\\R\\R-2.15.3")
        cmd = sys.executable + " setup.py install --install-lib=" + self.installdir
        return sh(cmd) == 0
        
PATCH = """
--- ./setup.py	Sat Apr 27 08:23:32 2013
+++ ./setup.py	Wed Jul 12 15:42:22 2013
@@ -287,19 +287,19 @@
                     span = rconfig_m.span()
                     ok = True
                     break
-                elif rconfig_m is None:
-                    if allow_empty:
-                        print('\nreturned an empty string.\n')
-                        rc += RConfig()
-                        ok = True
-                        break
-                    else:
-                        # if the configuration points to an existing library, 
-                        # use it
-                        if os.path.exists(string):
-                            rc += RConfig(libraries = substring)
-                            ok = True
-                            break
+            if rconfig_m is None:
+               if allow_empty:
+                   print('\nreturned an empty string.\n')
+                   rc += RConfig()
+                   ok = True
+                   break
+               else:
+                   # if the configuration points to an existing library, 
+                   # use it
+                   if os.path.exists(string):
+                       rc += RConfig(libraries = substring)
+                       ok = True
+                       break
             if not ok:
                 raise ValueError('Invalid substring\n' + substring 
                                  + '\nin string\n' + string)
@@ -334,15 +334,30 @@
 
 
 def get_rconfig(r_home, about, allow_empty = False):
+    FORCE_OPTIONS = True #if True, use patch, else use original one
     if sys.platform == "win32" and "64 bit" in sys.version:
         r_exec = os.path.join(r_home, 'bin', 'x64', 'R')
+        r_bin = os.path.join(r_home, 'bin', 'x64')
+        r_include = os.path.join(r_home, 'include')
     else:
         r_exec = os.path.join(r_home, 'bin', 'R')
-    cmd = '"'+r_exec+'" CMD config '+about
-    print(cmd)
-    rp = os.popen(cmd)
-    rconfig = rp.readline()
-    #Twist if 'R RHOME' spits out a warning
+        r_bin = os.path.join(r_home, 'bin', 'i386')
+        r_include = os.path.join(r_home, 'include')
+    options = {}
+    options['--ldflags'] = '-L%s -lR'%(r_bin)
+    options['--cppflags'] = '-I%s'%(r_include)
+    options['LAPACK_LIBS'] = '-lRlapack'
+    options['BLAS_LIBS'] = '-lRblas'
+    if not FORCE_OPTIONS:  
+        cmd = '"'+r_exec+'" CMD config '+about
+        print(cmd)
+        rp = os.popen(cmd)
+        rconfig = rp.readline()
+        #Twist if 'R RHOME' spits out a warning
+        rp.close()
+    else:
+        rconfig = options[about]
+        print "RCONFIG ", about, rconfig
     if rconfig.startswith("WARNING"):
         rconfig = rp.readline()
     rconfig = rconfig.strip()  
@@ -351,7 +364,6 @@
     except ValueError as ve:
         print(ve)
         sys.exit("Problem while running `{0}`\n".format(cmd))
-    rp.close()
     return rc
 
 def getRinterface_ext():
"""