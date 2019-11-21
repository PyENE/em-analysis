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
__revision__ = "$$Id: $$"

from pkgit.formula import Formula
from pkgit.utils import sh, checkout, StrictTemplate
from openalea.core.path import path

## Name is openalea_formula and not openalea to avoid namespace conflict!
class Openalea(Formula):
    version = '1.0'
    homepage = "http://openalea.gforge.inria.fr/dokuwiki/doku.php"
    # download_url = "https://scm.gforge.inria.fr/svn/openalea/branches/release_1_0"
    download_url = "https://scm.gforge.inria.fr/svn/openalea/trunk"
    license = "Cecill-C License"
    authors = "Inria, INRA, CIRAD"
    description = "OpenAlea is an open source project primarily aimed at the plant research community."
    download_name  = "OpenAlea"
    dependencies = ["python", "ipython", "setuptools", "pywin", "mingw", "mingw_rt", "qt4", "numpy", "scipy", "matplotlib", 
                  "pyqscintilla", "pillow", "pylsm", "svn", "dateutil", "ipython", "inno"]#"pylibtiff", 
    DOWNLOAD = BDIST_EGG = True

    def __init__(self,**kwargs):
        super(Openalea, self).__init__(**kwargs)
        self.dist_dir = path(self._get_dist_path())/"openalea"    
    
    def _download(self):
        return checkout(self.download_url, self.eggdir)

    def bdist_egg(self):
        return sh("python multisetup.py clean build install bdist_egg -d %s"%(self.dist_dir,)) == 0
        
    def conf_dict(self):
        """
        Use it for inno_setup. Cf. openalea.deploy.makeWinInstaller
        
        :return: dict of configuration to generate windows installer with inno setup
        """
        return {"generate_pascal_install_code":generate_pascal_install_code, "generate_pascal_post_install_code":generate_pascal_post_install_code}
"""
class Openaleaformula(Formula):
    version         = "0.9"  	 # Version of the dependency (not of the formula)
    description     = "Blabla"     # Description of the dependency (not of the formula)
    homepage        = ""     # Url of home-page of the dependency (not of the formula)
    license         = 'Cecill-C'     # License of the dependency (not of the formula)
    authors         = "Nous"     # Authors of the dependency (not of the formula)
    dependencies    = ["plein"]     # List of dependencies of the formula
    download_name   = "scikit-image.exe"     # Name of the local archive
    download_url    = "https://gforge.inria.fr/frs/download.php/32478/OpenAlea-1.0-Installer-Py2.7.exe" % version  	 # Url where to download sources (feel only if "DOWNLOAD = True")
    DOWNLOAD = INSTALL = COPY_INSTALLER = True
"""

        
def generate_pascal_install_code(eggmaxid):        
    tmpl = StrictTemplate("""
var i, incr:Integer;
var s:String;
begin
    Result:=False;
    incr := (100 - WizardForm.ProgressGauge.Position)/$EGGMAXID/2;
    for i:=0 to $EGGMAXID do begin
        s := ExtractFileName(Eggs[i]);
        WizardForm.StatusLabel.Caption:='Uncompressing '+s;
        WizardForm.Update();
        try
            ExtractTemporaryFile(s);
            InstallEgg( MyTempDir()+s, '-N');
        except
            Exit;
        end;
        WizardForm.ProgressGauge.Position := WizardForm.ProgressGauge.Position + incr;
    end;

    WizardForm.StatusLabel.Caption:='Installing OpenAlea ';
    WizardForm.ProgressGauge.Position := 85;
    WizardForm.Update();    
    InstallEgg( 'OpenAlea.Deploy', '-H None -i ' + MyTempDir() + ' -f ' + MyTempDir());
        
    WizardForm.ProgressGauge.Position := 90;
    WizardForm.Update();        
    InstallEgg( 'OpenAlea', '-H None -i ' + MyTempDir() + ' -f ' + MyTempDir());
    Result := True;

    WizardForm.ProgressGauge.Position := 100;
    WizardForm.Update();                   
end;""")
    code = tmpl.substitute(EGGMAXID=eggmaxid)
    return code
    

        
# -- The default generate_pascal_post_install_code(opt) function returns "". --
# -- Let's do something smarter for openalea, to add it to start menu. --                                  
def generate_pascal_post_install_code(egg_pths):
    postInstallPascalTemplate = StrictTemplate("""
    Exec(GetPythonDirectory()+'python.exe', '-c "import sys;sys.path.append(\\"'+ GetPythonDirectory()+'Lib\\site-packages\\'+Eggs[$EGGID]+'\\");import $EGGNAME' + '_postinstall as pi;pi.install()', '',
     SW_HIDE, ewWaitUntilTerminated, ResultCode);""")
    s=""
    names = ["visualea", "deploygui"]

    for i, e in enumerate(egg_pths):
        e = path(e).basename()
        for p in names:
            if p in e.lower():
                s += postInstallPascalTemplate.substitute(EGGID=str(i), EGGNAME=p)
            
    return s
