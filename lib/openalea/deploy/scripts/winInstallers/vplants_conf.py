# -- Installer and dependency packages description : EDIT THIS --
APPNAME="VPlants"
APPVERSION="1.0"
setup = {"LicenseFile":pj(__path__,"LICENSE.TXT"), "WizardSmallImageFile":pj(__path__,"vplogo.bmp")}  

eggGlobs = "*\\dist\\VPlants*.egg|*\\dist\\OpenAlea*.egg|tissue\\*\\dist\\VPlants*.egg|*\\dist\\c*.egg"

# package -> (installerFlags, installationOrder)
thirdPartyPackages = [   ("python", (NOT_INSTALLABLE|RUNTIME|DEVELOP,)), #always tested
                         ("openalea", (NOT_INSTALLABLE|RUNTIME|DEVELOP,)),
                         ("scons", (EGG|DEVELOP,)),
                         ("bisonflex", (EGG|DEVELOP,)),
                         ("boost", (EGG|PY_DEP|ARCH|RUNTIME|DEVELOP,)),
                         ("ann", (EGG|ARCH|RUNTIME,)),
                         ("cgal", (EGG|ARCH|RUNTIME,)),
                         ("qhull", (EGG|ARCH|DEVELOP,)),
                         ("gnuplot", (EXE|ARCH|RUNTIME|DEVELOP,)),
                         ("pyopengl", (EXE|ARCH|RUNTIME|DEVELOP,)),
                         ("pyqglviewer", (EGG|ARCH|PY_DEP|RUNTIME|DEVELOP,)),
                         ("qt4_dev", (EGG|ARCH|DEVELOP,)),
                         ("mingw", (EGG|ARCH|DEVELOP,))                               
                         ]    
                         #("networkx", (EGG|PY_DEP|RUNTIME|DEVELOP,)), 
                         

                         
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
        e = basename(e)
        for p in names:
            if p in e.lower():
                s += egg_post_inst.substitute(EGGID=str(i), EGGNAME=p)          
    return s    