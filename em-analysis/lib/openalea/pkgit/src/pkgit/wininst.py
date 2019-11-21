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

# The point of this file is to create an inno setup script to install openalea/vplants
# on a machine without having to rely on an internet connection during installation
# while leveraging the power off eggs for later updates.

# It uses the following strategy:
# 0 ) Prepare working dir (remove it if necessary and [re]create it)
# 1 ) from a map of package names and bit masks we:
# - go fetch installers for our Python version in srcDir and copy them into the working dir
# - copy test files for packages whose bitmask says it should be tested
# - configure template_win_inst.iss.in in various ways, filling in the blanks:
    # * files to be packaged into the installer
    # * generating testing and installation code
    # * etc...
# 2 ) Write down the configured template_win_inst to the working directory.
#
# BTW think of this module as a root-level class. It behaves mostly like a class excepted I didn't
# encapsulate it inside a class.

from collections import OrderedDict
import os
import string
import sys
import types
import subprocess
from openalea.core.path import path, glob, shutil

from pkgit.utils import deps, mask, import_formula

import locale
unused, local_enc = locale.getdefaultlocale()

err = sys.stderr.write

__path__ = path(__file__).abspath().dirname()

# -- Some Flags : DONT CHANGE THESE IF YOU DON'T KNOW WHAT YOU'RE DOING --
NOFLAG = 0
# Is it an egg, an exe, a zip to install with easy_install or an msi?
EGG     = 2**0
EXE     = 2**1
ZIPDIST = 2**2
EXEDIST = 2**3
TARDIST = 2**12
MSI     = 2**4
# Does the egg depend on python version?
PY_DEP  = 2**5
# Is it for runtime or development, or both ?
RUNTIME = 2**6
DEVELOP = 2**7
# Should we test for it ?
TEST_ME = 2**8
# If it can't be installed
NOT_INSTALLABLE = 2**9 #if tested and not installable, then fatal!
# Is it architecture dependent (i386 vs x86_64)?
ARCH    = 2**10
# A flag that marks the thing as an innosetup component
COMPONENT = 2**11

# -- Installer and dependency packages description are declared here but are actually defined in the
# -- conf file.
# APPNAME=None
# APPVERSION=None
# thirdPartyPackages = None

class StrictTemplate(string.Template):
    idpattern = r"[_A-Z0-9]*"

# function to test bitmasks
def bt(val, bit):
    return bit==(val&bit)


installerExtensions = { 0:"",
                        EGG:".egg",
                        EXE:".exe",
                        EXEDIST:".exe",
                        ZIPDIST:".zip",
                        TARDIST:".tar.gz",
                        MSI:".msi",
                        }

###########################################################################################
# The following strings will be used as templates to create PascalScript in the installer #
# that test and installs the modules that we wan to install and/or test                   #
###########################################################################################
python_package_test_template = """
(*** Function to detect $PACKAGE ***)
function Detect$PACKAGE(): Boolean;
var
  ResultCode: Integer;
begin
  ExtractTemporaryFile('$PACKAGE_TEST');
  Result:=(Exec(GetPythonDirectory()+'python.exe', MyTempDir()+'$PACKAGE_TEST', '',
          SW_HIDE, ewWaitUntilTerminated, ResultCode)) and (ResultCode=0);
end;

"""

python_package_install_template_pass = """
(*** Function to install $PACKAGE ***)
function Install$PACKAGE(): Boolean;
begin
end;

"""

python_package_install_template_exe = """
(*** Function to install $PACKAGE ***)
function Install$PACKAGE(): Boolean;
begin
  ExtractTemporaryFile('$PACKAGE_INSTALLER');
  Result := InstallExe(MyTempDir()+'$PACKAGE_INSTALLER');
end;

"""

python_package_install_template_egg = """
(*** Function to install $PACKAGE ***)
function Install$PACKAGE(): Boolean;
begin
       ExtractTemporaryFile('$PACKAGE_INSTALLER');
       Result := InstallEgg( MyTempDir()+'$PACKAGE_INSTALLER', '-N');
end;

"""

python_package_install_template_zipdist = """
(*** Function to install $PACKAGE ***)
function Install$PACKAGE(): Boolean;
begin
       ExtractTemporaryFile('$PACKAGE_INSTALLER');
       Result := InstallZipdist( MyTempDir()+'$PACKAGE_INSTALLER');
end;

"""

python_package_install_template_msi = """
(*** Function to install $PACKAGE ***)
function Install$PACKAGE(): Boolean;
begin
       ExtractTemporaryFile('$PACKAGE_INSTALLER');
       Result := InstallMsi( MyTempDir()+'$PACKAGE_INSTALLER');
end;

"""

#"ti" stands for "test and install"
python_package_ti_template_exe    = python_package_test_template+python_package_install_template_exe
python_package_ti_template_egg    = python_package_test_template+python_package_install_template_egg
python_package_ti_template_zipdist= python_package_test_template+python_package_install_template_zipdist
python_package_ti_template_msi    = python_package_test_template+python_package_install_template_msi

def prepare_working_dir(instDir, no_del=False):
    if path(instDir).exists():
        if no_del:
            return
        print instDir, "will be deleted"
        shutil.rmtree(instDir, ignore_errors=False)
    print instDir, "will be created"
    os.makedirs(instDir)

def find_installer_files(tpp_eggDir, srcDir, pyMaj, pyMin, arch, dependencies):

    
    def globInstaller(pk, mask_):
        dir_ = srcDir
        identifier = "*"+pk+"*"
        if bt(mask_, PY_DEP):
            identifier+=pyMaj+"."+pyMin+"*"
        if bt(mask_, MSI): identifier+=".msi"
        elif bt(mask_, EXE): identifier+=".exe"
        elif bt(mask_, EXEDIST): 
            identifier+=".exe"
            dir_ = tpp_eggDir
        elif bt(mask_, ZIPDIST): 
            identifier+=".zip"
            dir_ = tpp_eggDir        
        elif bt(mask_, TARDIST): 
            identifier+=".tar.gz"
            dir_ = tpp_eggDir
        elif bt(mask_, EGG): 
            identifier+=".egg"
            dir_ = tpp_eggDir        
        elif bt(mask_, NOFLAG):
            return None
        else:
            raise Exception("Unknown installer type: " + pk +":"+str(mask_))

        try:
            if bt(mask_, ARCH): #WE CARE ABOUT THE ARCH
                if arch=="win32": #either it has 32 or nothing but not 64
                    files = [f for f in glob.iglob(path(dir_)/identifier)  if arch in f or ("win32" not in f and "64" not in f)]
                else:
                    files = [f for f in glob.iglob(path(dir_)/identifier)  if arch in f]
                return sorted(files, lambda x, y: cmp(len(x), len(y)))[0]
            else:
                return glob.glob(path(dir_)/identifier)[0]
        except:
            #traceback.print_exc()
            err(u"\tNo installer found for %s for %s : %s\n"%(pk, dir_,identifier))
            return None
                        
    print "Gathering paths to binaries..."
    ok = True
    
    for pk, info in dependencies.iteritems():
        mask_ = info[0]
        if not bt(mask_, NOT_INSTALLABLE) and info[1] is None:
            ef = globInstaller(pk, mask_)
            if ef is None:
                #ok = False
                continue
            info[1] = ef
            print "\tWill install %s"%ef        
    return ok
        
def get_project_eggs(arch, globs, outDir, srcDir):
    # real egg names have the project prefix eg, "OpenAlea", "VPlants".
    # then comes the python version "py2.6"
    # and optionnaly the OS "linux-i686", "win32".
    # However, we don't explicitly know which egg has the os in the name
    # so simply encoding the os in the glob is a bad idea. What we do is:
    # [glob for project_prefix*python_version.egg] + [glob for project_prefix*python_version*os.egg]
    # The egg globs at this stage have the project_prefix*python_version*.egg form.   
    
    files = []
    for g in globs:
        files += glob.glob(g)

    # -- then we filter these files --
    files = [f for f in files if (arch in f) or (not "win" in f)]
        
    print "Gathering path to eggs..."
    egg_paths = []
    # localFiles = map(basename, files)
    localFiles = [path(file).basename() for file in files] 
    for f, filename in zip(files, localFiles):
        egg_paths.append(f)
        print "\tWill install %s"%f
    return egg_paths


# -- ATTENTION PLEASE -- must be run after "copy eggs" and "get_installer_files"<
# -- Override me to generate innosetup [setup] section.       
def generate_inno_installer_setup_group(setup):    
    final = ""
    for k, v in setup.iteritems():
        src = path(v).basename()
        if "file" in k.lower():
            src = path(v).abspath()
            print "\t"+src
        final += k + "=" + src + "\n"
    return final
    
# -- ATTENTION PLEASE -- must be run after "copy eggs" and "get_installer_files"<
def generate_inno_installer_files_group(dependencies, egg_pths):
    final = ""
    #installers and test files
    for pk, info in dependencies.iteritems():
        if info[2]: # if we have test files associated
            final += "Source: \""+info[2]+"\"; DestDir: {tmp}; Flags: dontcopy\n"
        if info[1]: #if we have an installer to package
            final += "Source: \""+info[1]+"\"; DestDir: {tmp}; Flags: dontcopy\n"                
    #eggs 
    for f in egg_pths:
        final += "Source: \""+f+"\"; DestDir: {tmp}; Flags: dontcopy\n"        
    return final
    
# -- ATTENTION PLEASE -- must be run after "copy eggs" and "get_installer_files"    
def generate_pascal_test_install_code(dependencies):
    final = ""
    testVariables = {"python":"PyInstalled"} #there's always this variable

    for pk, info in dependencies.iteritems():
        mask_ = info[0]
        testVariables[pk] = pk+"Installed" #always defined
        if bt(mask_,TEST_ME):
            if bt(mask_, NOT_INSTALLABLE):
                template = StrictTemplate(python_package_test_template)
                final += template.substitute(PACKAGE=pk,
                                             PACKAGE_TEST=path(info[2]).basename() )
            else:            
                #"ti" stands for "test and install"
                if bt(mask_, MSI): template = python_package_ti_template_msi
                elif bt(mask_, EXEDIST): template = python_package_ti_template_zipdist
                elif bt(mask_, ZIPDIST): template = python_package_ti_template_zipdist
                elif bt(mask_, TARDIST): template = python_package_ti_template_zipdist
                elif bt(mask_, EGG): template = python_package_ti_template_egg
                elif bt(mask_, EXE): template = python_package_ti_template_exe
                else: raise Exception("Unknown installer type: " + pk +":"+str(mask_))
                template = StrictTemplate(template)
                final+=template.substitute(PACKAGE=pk,
                                           PACKAGE_TEST=path(info[2]).basename(),
                                           PACKAGE_INSTALLER=path(info[1]).basename() )
        else:
            
            if bt(mask_, NOT_INSTALLABLE):
                continue
            else :
                if bt(mask_, MSI): template = python_package_install_template_msi
                elif bt(mask_, EXEDIST): template = python_package_install_template_zipdist
                elif bt(mask_, ZIPDIST): template = python_package_install_template_zipdist
                elif bt(mask_, TARDIST): template = python_package_install_template_zipdist
                elif bt(mask_, EGG): template = python_package_install_template_egg
                elif bt(mask_, EXE): template = python_package_install_template_exe
                else: raise Exception("Unknown installer type: " + pk +":"+str(mask_))
                template = StrictTemplate(template)
                print pk, info[0], info[1]
                final+=template.substitute(PACKAGE=pk,
                                           PACKAGE_INSTALLER=path(info[1]).basename() )                        
    return final, testVariables
    
def generate_pascal_detect_env_body(dependencies, testVars, appname):
    testReportingPascalTemplate = StrictTemplate(
"""
  if not $VAR then
    caption := caption+#13+'$PACKAGE is not installed, $APPNAME will install it for you.'
  else
    caption := caption+#13+'$PACKAGE is already installed.';
""")

    testFatalReportingPascalTemplate = StrictTemplate(
"""
  if not $VAR then
    begin
        caption := caption+#13+'$PACKAGE is not installed, please install it first. Setup will abort';
        MsgBox('$PACKAGE is missing, installation will abort soon.', mbCriticalError, MB_OK);
        ABORTINSTALL := True;
    end
  else
    caption := caption+#13+'$PACKAGE is already installed.';
""")
    testing = ""
    reporting = ""
    for pk, info in dependencies.iteritems():
        mask_ = info[0]  
        if bt(mask_, TEST_ME) or pk == "python":                 
            var = testVars[pk]
            testing += "  "+ var + " := PyInstalled and Detect"+pk+"();\n"
                    
            if bt(mask_, NOT_INSTALLABLE): #if tested and not installable, then fatal!
                reporting += testFatalReportingPascalTemplate.substitute(PACKAGE=pk,
                                                                         VAR=var,
                                                                         APPNAME=appname)
            else:       
                reporting += testReportingPascalTemplate.substitute(PACKAGE=pk,
                                                                    VAR=var,
                                                                    APPNAME=appname)
    return testing, reporting
            
def generate_pascal_deploy_body(dependencies, testVars, step):
    installationPascalTemplate = StrictTemplate(
"""
  if res and not $VAR then
    begin
      WizardForm.StatusLabel.Caption:='Installing $PACKAGE, please wait...'; 
      WizardForm.ProgressGauge.Position := WizardForm.ProgressGauge.Position + $STEP;
      WizardForm.Update();
      res := Install$PACKAGE();
    end;
""")    
    installation = ""
    
    for pk, info in dependencies.iteritems():
        mask_ = info[0]
        if bt(mask_, NOT_INSTALLABLE):
            continue
        var = testVars[pk]
        installation += installationPascalTemplate.substitute(PACKAGE=pk,
                                                              VAR=var,
                                                              STEP=step)
    return installation
          
# -- Override me to generate postInstall pascal code.          
def generate_pascal_post_install_code(options):
    return ""

# -- Override me to generate application installation pascal code.         
def generate_pascal_install_code(eggmaxid):        
    tmpl =  StrictTemplate("""
var i, incr:Integer;
var s:String;
begin
    Result:=False;
    incr := (100 - WizardForm.ProgressGauge.Position)/$EGGMAXID;
    for i:=0 to $EGGMAXID do begin
        s := ExtractFileName(Eggs[i]);
        WizardForm.StatusLabel.Caption:='Uncompressing '+s;
        WizardForm.Update();
        ExtractTemporaryFile(s);
        Result := InstallEgg( MyTempDir()+s, '-N');
        WizardForm.ProgressGauge.Position := WizardForm.ProgressGauge.Position + incr;
    end;
    Result := True;
end;""")
    code = tmpl.substitute(EGGMAXID=eggmaxid)
    return code
    
def configure_inno_setup_without_args(appname, appversion, dependencies, runtime, pyMaj, pyMin, setup, outDir, funcs, egg_pths):
    print "Configuring inno script...",
    f = open( path(__path__)/"template_win_inst.iss.in")
    s = f.read()
    f.close()

    template = StrictTemplate(s)
    eggnum = len(egg_pths)

    eggArrayInit = ""
    for i, e in enumerate(egg_pths):
        eggArrayInit+="Eggs[%i] := '%s';\n"%(i, e) 
    
    s='\n'+"#"*80+'\n'
    print s+eggArrayInit+s
    
    step = int(100./(eggnum+len(dependencies)))    
    detect, testVars = funcs["generate_pascal_test_install_code"](dependencies)
    testingBody, reportingBody = funcs["generate_pascal_detect_env_body"](dependencies, testVars, appname)
    installationBody = funcs["generate_pascal_deploy_body"](dependencies, testVars, step)

    modeStr = "" if runtime else "dev"
    s = template.substitute(APPNAME=appname,
                            APPVERSION=appversion,
                            INSTTYPE=modeStr.upper(),
                            SETUP_CONF=funcs["generate_inno_installer_setup_group"](setup),
                            #configure Python Major and Minor
                            PYTHONMAJOR=pyMaj,
                            PYTHONMINOR=pyMin,
                            #the pascal booleans that store if this or that package is installed or not.
                            TEST_VARIABLES=reduce(lambda x,y: x+", "+y, testVars.itervalues(), "dummy"),
                            #the files that will be packed by the installer.
                            INSTALLER_FILES=funcs["generate_inno_installer_files_group"](dependencies, egg_pths),
                            #configure number of eggs
                            EGGMAXID=str(eggnum-1),
                            #configure the initialisation of egg array
                            EGGINIT=eggArrayInit,
                            #configure other pascal code
                            STEP=step,
                            #configure the functions that detect and install packages
                            INSTALL_AND_DETECTION_CODE=detect,
                            #configure the body of DetectEnv that tests
                            TEST_VAR_RESULTS=testingBody,
                            #configure the body of DetectEnv that reports
                            REPORT_VAR_RESULTS=reportingBody,
                            INSTALL_APP_BODY=funcs["generate_pascal_install_code"](str(eggnum-1)),
                            #configure the body of Deploy that installs the dependencies
                            DEPLOY_BODY=installationBody,
                            #Code to run on post install
                            POSTINSTALLCODE=funcs["generate_pascal_post_install_code"](egg_pths),                            
                            )

    fpath = path(outDir)/appname+"_installer_"+modeStr+".iss"
    f = open( fpath, "w" )
    f.write(s.encode(local_enc))
    f.close()
    print "ok"
    return fpath
    
def make_stitcher( eggDir, pyMaj, pyMin):
    """Creates a function that inserts the pyX.X string
    in the egg glob string if it's not there already."""
    pyfix = "py"+pyMaj+"."+pyMin+"*"
    def __stitch_egg_names(eggName):
        if pyfix in eggName:
            return path(eggDir)/eggName
        part = path(eggName).splitext()
        return path(eggDir)/(part[0]+pyfix+part[1])
    return __stitch_egg_names                        

def wininst(project="openalea", srcDir=None, eggDir=None, outDir=None, tpp_eggDir=None, pyMaj=None, pyMin=None, eggGlobs="*.egg", setup={}, arch="win32", runtime=True):
    """
    :project: openalea, vplants, alinea or oalab
    :srcDir: source third part dir
    :eggDir: egg openalea/vplants/alinea dir
    :outDir: output dir (result)

    :warning: get all eggs in eggDir! So if you wininst alinea, it will package openalea+vplants+alinea but only dependencies for alinea!
    """
    if not srcDir:
        srcDir = path(".").abspath()/"dist"/"thirdpart"
    if not eggDir:
        eggDir = path(".").abspath()/"dist"/project
    # if not srcDir:
        # srcDir = path(".").abspath()/"dist"/"test"
    # if not eggDir:
        # eggDir = path(".").abspath()/"dist"/"test"
    if not outDir:
        outDir = path(srcDir).abspath()/".."/"result"
    if not pyMaj:
        pyMaj = str(sys.version_info.major)
    if not pyMin:
        pyMin = str(sys.version_info.minor)
        
    outDir = path(outDir)/(project+"_"+sys.platform+"_"+pyMaj+"."+pyMin)
    tpp_eggDir = tpp_eggDir or srcDir
    print srcDir #.encode("latin_1")
    
    prepare_working_dir(outDir, no_del=True)
    
    # -- Find the configuration file
    ###confFile  = args.confFile or path(__file__).splitpath()[0]/(args.project+"_conf.py")        
    ###confDict = read_conf_file(confFile)    
    formula = import_formula(project)()
    confDict = formula.conf_dict()
    
    #   -- funcs will contain function overrides read from confFile --
    funcs = dict( (fname, f) for fname, f in globals().iteritems() if isinstance(f, types.FunctionType) )
    funcs.update(dict( (fname, f) for fname, f in confDict.iteritems() if isinstance(f, types.FunctionType)))    
    #   -- vars will contain vars read from confFile --    
    ###thirdPartyPackages = confDict["thirdPartyPackages"]
    ###appname            = confDict["APPNAME"]
    ###appversion         = confDict["APPVERSION"]
    
    thirdPartyPackages = deps(project)
    todelete = [project]
    for dep in thirdPartyPackages:
        if "openalea" in dep:
            todelete.append(dep)
        if "vplants" in dep:
            todelete.append(dep)
        if "alinea" in dep:
            todelete.append(dep)
    if "vplants" in project:
        todelete = todelete + deps("openalea")
    if "alinea" in project:
        todelete = todelete + deps("vplants")
        
    for dep in todelete:
        if dep in thirdPartyPackages:
            thirdPartyPackages.remove(dep)
            print "remove " + dep
            
    appname             = project
    if project == "oalab":
        appname = "openalealab"
    appversion          = import_formula(project).version
                            
    # -- Fix the egg globs to include python version and architecture dependency.
    eggGlobs = map(make_stitcher(eggDir, pyMaj, pyMin), eggGlobs.split("|"))
    print "The following project egg globs will be used:", eggGlobs

    # -- Filter the dependencies to process according to the type of installer (for runtimes or devtools)
    # -- The dict points from package names to package info [bitmask, installer_path, test_script_path]
    ###dependencies = OrderedDict( (pk, [mask, None, None]) for pk, (mask,) in thirdPartyPackages  \
    ###                            if processInstaller(mask, args.runtime) )
    dependencies = OrderedDict( (pk, [mask(pk), None, None]) for pk in thirdPartyPackages )
     
    # -- find out the installers to package for this mega installer --
    # will complete dependencies if they have no info[1].
    ok = find_installer_files(tpp_eggDir, srcDir, pyMaj, pyMin, arch, 
                              dependencies)                            
                            
    if not ok:
        sys.exit(-1)
        
    proj_egg_pths = get_project_eggs(arch, eggGlobs, outDir, srcDir)
    gen = configure_inno_setup_without_args(appname, appversion, dependencies, runtime, pyMaj, pyMin, setup, outDir, funcs, proj_egg_pths)
    print "Done, please check the generated file:", gen
    
    print "Now compiling",    
    if subprocess.call("iscc.exe "+gen, shell=True, env=os.environ):
        return False