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
from pkgit.utils import sh, checkout, StrictTemplate
from openalea.core.path import path

class Vplants(Formula):
    version = '1.0'
    homepage = "http://openalea.gforge.inria.fr/dokuwiki/doku.php"
    # download_url = "https://scm.gforge.inria.fr/svn/vplants/vplants/branches/release_1_0"
    download_url = "https://scm.gforge.inria.fr/svn/vplants/vplants/trunk"
    license = "Cecill-C License"
    authors = "Virtual Plants team (Inria)"
    description = "Set of packages to analyse, model and simulate plant architecture and its development at different scales (tissue, organ, axis and plant)"
    download_name  = "VPlants"
    dependencies = ["openalea", "ann", "bisonflex", "boost", "cgal", "mingw",
                    "gnuplot", "pyopengl", "qt4", "qt4_dev", "qhull", "mingw_rt",
                    "rpy2", "scons", "svn", "pyqglviewer"]#"glut","glut-dev","nose-dev","networkx",
    DOWNLOAD = BDIST_EGG = True
    
    def __init__(self,**kwargs):
        super(Vplants, self).__init__(**kwargs)
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
        
def generate_pascal_install_code(eggmaxid):        
    manuallyInstalled = ["VPlants"]

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
        ExtractTemporaryFile(s);
        try        
            InstallEgg( MyTempDir()+s, '-N');
        except
            Exit;
        end;
        WizardForm.ProgressGauge.Position := WizardForm.ProgressGauge.Position + incr;
    end;
    """)
    s = tmpl.substitute(EGGMAXID=eggmaxid)
    
    manInstTemplate = StrictTemplate("""
    WizardForm.StatusLabel.Caption:='Installing $PACKAGE';
    WizardForm.Update();
    Result := InstallEgg('$PACKAGE', '-H None -i ' + MyTempDir() + ' -f ' + MyTempDir()); 
    """)       
    
    for pk in manuallyInstalled:
        s += manInstTemplate.substitute(PACKAGE=pk)
        
    s += """               
     WizardForm.ProgressGauge.Position := 100;
    end;
    """ 

    return s
    
    
# -- The default generate_pascal_post_install_code(opt) function returns "". --
# -- For alinea, let's make sure RPy2 has everything to work correctly. --                         
def generate_pascal_post_install_code(egg_pths):
    s=""
    s += """
        RegQueryStringValue(HKEY_LOCAL_MACHINE, 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment',
                'PATH', str1);
        if RegQueryStringValue(HKEY_LOCAL_MACHINE, 'Software\R-core\R', 'InstallPath', str2) then
                RegWriteStringValue(HKEY_LOCAL_MACHINE, 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment',
                'R_HOME', str2);
                        
        if (Pos('%R_HOME%', str1) = 0) then
            RegWriteStringValue(HKEY_LOCAL_MACHINE, 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment',
                'PATH', str1+';%R_HOME%');  
    """
          
    egg_post_inst = StrictTemplate("""
    Exec(GetPythonDirectory()+'python.exe', '-c "import sys;sys.path.append(\\"'+ GetPythonDirectory()+'Lib\\site-packages\\'+Eggs[$EGGID]+'\\");import $EGGNAME' + '_postinstall as pi;pi.install()', '',
     SW_HIDE, ewWaitUntilTerminated, ResultCode);""")
    
    names = ["lpygui"]

    for i, e in enumerate(egg_pths):
        e = path(e).basename()
        for p in names:
            if p in e.lower():
                s += egg_post_inst.substitute(EGGID=str(i), EGGNAME=p)          
    return s        