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
from pkgit.utils import checkout, sh
from openalea.core.path import path

"""
C:\temp_working_dir>pkgit -p oalab --without openalea,plantgl,lpy,mtg,setuptools,ipython --dry-run
"""


class Oalab(Formula):
    version         = "0.1"  	 # Version of the dependency (not of the formula)
    description     = "OpenAlea is an open source project primarily aimed at the plant research community."     # Description of the dependency (not of the formula)
    homepage        = "http://openalea.gforge.inria.fr/dokuwiki/doku.php"     # Url of home-page of the dependency (not of the formula)
    license         = "Cecill-C License"     # License of the dependency (not of the formula)
    authors         = "Inria, INRA, CIRAD"     # Authors of the dependency (not of the formula)
    dependencies    = ["ipython", "openalea", "plantgl", "lpy", "mtg", "configobj"]  ## +Pandas   # List of dependencies of the formula
    download_name   = "oalab"     # Name of the local archive
    download_url    = "https://scm.gforge.inria.fr/svn/vplants/vplants/trunk/oalab"   	 # Url where to download sources (feel only if "DOWNLOAD = True")
    DOWNLOAD = BDIST_EGG = True
    
    def __init__(self,**kwargs):
        super(Oalab, self).__init__(**kwargs)
        self.dist_dir = path(self._get_dist_path())/"openalea"
        
    def _download(self):
        return checkout(self.download_url, self.eggdir)

    def bdist_egg(self):
        cmd = "python setup.py build bdist_egg -d %s"%(self.dist_dir,)
        print cmd
        return sh(cmd) == 0
        
    def _configure_script(self):
        return True

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

    WizardForm.StatusLabel.Caption:='Installing OpenAleaLab ';
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
    names = ["oalab"]

    for i, e in enumerate(egg_pths):
        e = path(e).basename()
        for p in names:
            if p in e.lower():
                s += postInstallPascalTemplate.substitute(EGGID=str(i), EGGNAME=p)
            
    return s
