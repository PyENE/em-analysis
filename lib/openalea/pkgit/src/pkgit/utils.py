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

import traceback
import sys, os
import subprocess
import zipfile
import tarfile
import string
import fnmatch
try:
    from path import shutil, path, glob
except ImportError:
    raise ImportError('Please install path.py. You can do it doing "pip install path.py"')
try:
    import requests
except ImportError:
    raise ImportError('Please install requests. You can do it doing "pip install requests"')
from re import compile as re_compile
from collections import defaultdict
from .patch import fromfile, fromstring
from setuptools.package_index import PackageIndex as pi
import logging

def eggify_formulas(formula_name, dest_dir=None, without=None, dry_run=False, force=False):
    """
    Eggify formula and deps recursively
    :param formula_name: string name of the formula
    :param dest_dir: directory where to put the egg when it is created
    :return: True if success, else False
    """
    if without == "all":
        formula_list = [formula_name]
    else:
        formula_list = deps(formula_name, without=without)
    logger.debug("----------------------------------------------")
    logger.debug("-----------Will eggify formulas %s-----------------"%str(formula_list))
    logger.debug("----------------------------------------------")
    print("Will eggify formulas %s"%str(formula_list))
    ret = True
    
    if not dry_run:   
        for formula in formula_list:
            formula, ret_ = eggify_formula(formula, dest_dir=dest_dir, dry_run=dry_run, force=force)
            ret = ret & ret_
            
        return ret
                
def eggify_formula(formula_name, dest_dir=None, dry_run=False, force=False):
    """
    Eggify only one formula
    :param formula_name: string name of the formula
    :param dest_dir: directory where to put the egg when it is created
    :return: (instance of the eggified formula), (True if success else False)
    """    
    formula = instanciate_formula(formula_name)
    print("Formula %s instantiated." %formula_name)

    if not dry_run:    
        logger.debug("Formula %s" %(formula_name))
        if dest_dir is not None:
            formula.dist_dir = path(dest_dir).abspath()
        if force:
            formula.force = True
        
        ret = True
        ret = ret & formula._download()
        ret = ret & formula._unpack()
        ret = ret & formula._install()
        ret = ret & formula._configure()
        ret = ret & formula._make()
        ret = ret & formula._make_install()
        ret = ret & formula._bdist_egg()
        ret = ret & formula._copy_installer()
        ret = ret & formula._post_install()
        
        print ""
        print "Formula %s success : %s ==============================" %(formula_name,ret)
        print ""
        
        logger.debug("Formula %s success : %s" %(formula_name,ret))
        return formula, ret
        
def post_install(formula_name, dest_dir=None, dry_run=False):
    """
    Install a formula after packaged it if necessary
    """
    formula = instanciate_formula(formula_name)
    if not formula.packaged()[0]:
        formula, ret = eggify_formula(formula_name, dest_dir=dest_dir, dry_run=dry_run)
    formula.POST_INSTALL = True
    formula._post_install()
    
def packaged(formula_name):
    formula = instanciate_formula(formula_name)
    ret, name = formula.packaged()
    
    new_name = ""
    if isinstance(name, list):
        for n in name:
            new_name = new_name + " " + n
    else:
        new_name = name
        
    if ret:
        print(formula_name + " yet packaged with name " + new_name )
    else:
        print(formula_name + " NOT packaged")
    return ret

def remove_temp(formula_name,download_too=False):
    """
    Remove files created by "easy_pkg package formula_name".
    """
    try:
        formula_name_cap = formula_name[0].capitalize() + formula_name[1:]
        cmd_import = "from pkgit.formulas.%s import %s" %(formula_name,formula_name_cap)
        exec(cmd_import, globals(), locals())
    except ImportError:
        print
        print("Cannot find formula %s. Maybe it is misspelled" %formula_name)
        print
        raise
    
    # instanciate formula
    cmd_instanciate = "%s()" %formula_name_cap
    formula = eval(cmd_instanciate)    
    
    dirs = [formula.sourcedir,formula.eggdir,formula.installdir]
    if download_too:
        dirs.append(formula.archname)
    print "Will remove %s" %str(dirs)
    
    # Remove
    for f in dirs:
        f = path(f)
        if f.exists():
            if f.isdir():
                f.rmtree()
            else:
                f.remove()
        else:
            logger.debug( "Can't remove %s" %f)


def formulas():
    """
    Return the list of formula available.
    """
    path_ = path(__file__).abspath().dirname()
    formula_list = glob.glob(path(path_)/"formulas"/"*.py")

    short_list = list()
    for formu in formula_list:
        formu = path(formu).splitpath()[-1]
        formu = path(formu).splitext()[0]
        short_list.append(str(formu))
        
    if short_list.count("__init__") > 0:
        short_list.remove("__init__")
        
    return short_list
    
def versions():
    """
    :return: the list of formula available and corresponding version.
    """
    result_list = list()
    formula_list = formulas()
    for formula_name in formula_list:
        formula = import_formula(formula_name)
        space_number = 18 - len(formula_name)
        space = ""
        for i in range(space_number):
            space = space + " " 
        result_list.append(str(formula_name+space+formula.version))
    return result_list
	
def who_deps(formula_name):
    """
    Get who formulas depends of formula "formula_name".
    
    :example:
        >>#Search what are dependencies using dependencies
        >>for dep in formulas():
        >>    print("Dependency %s is used by dependency(ies) %s"%(dep, who_deps(dep)))
    """
   
    formulas_names = formulas()
    who = list()
    
    for form_name in formulas_names:
        form = import_formula(form_name)
        for dependency in form.dependencies:
            if str(formula_name) == str(dependency):
                who.append(form_name)
    return who
    
def direct_deps(formula_name, without=list()):
    """
    :param formula_name: name of formula to get dependencies. (str)
    :param without: deps that you want to omit. (list)
    :return: list of dependencies included formula_name (not recursif!). (list)
    """
    parent = import_formula(formula_name)
    children = parent.dependencies
    
    if len(without) > 0:
        for dep in without:
            if dep in children:
                children.remove(dep)
    
    return children
	
def deps(formula_name, without=list(), recursif=True):
	"""
	:param formula_name: name of formula to get dependencies. (str)
    :param without: deps that you want to omit. (list)
	:param recursif: if False return direct dependencies. If True return recursive dependencies. (bool)
	:return: list of dependencies included formula_name. (list)
	"""
    
	if not recursif:
		formula_list = [formula_name]
		for dep in direct_deps(formula_name, without=without):
			index = formula_list.index(formula_name)
			new_name = dep
			formula_list.insert(index,new_name)
		return formula_list
		
	else:
		deps = list()
		to_check = list()
		to_check.append(formula_name)

		while len(to_check) > 0:
			formula_to_check = to_check.pop(0)
			if formula_to_check not in deps:
				deps.insert(0,formula_to_check)
			else:
				index = deps.index(formula_to_check)
				deps.pop(index)
				deps.insert(0,formula_to_check)

			new_deps = direct_deps(formula_to_check, without=without)
			if new_deps is not None:
				if len(new_deps) > 0:
					if isinstance(new_deps, str):
						to_check.insert(0,new_deps)
					elif isinstance(new_deps, list):
						for dep in new_deps:
							to_check.insert(0,dep)
						
		return deps
	
def mask(formula_name):
    """
    Check if formula create an egg, an exe or an msi.
    
    :param formula_name: name of formula to check
    :return: "exe", "msi" or "egg"
    """
    NOFLAG  = 0
    EGG     = 2**0
    EXE     = 2**1
    MSI     = 2**4
    NOT_INSTALLABLE = 2**9
    formula = import_formula(formula_name)
    if "openalea" in formula_name:
        return NOFLAG
    if "vplants" in formula_name:
        return NOFLAG
    if "alinea" in formula_name:
        return NOFLAG
        
    if formula.BDIST_EGG:
        return EGG
    elif formula.COPY_INSTALLER:
        if formula.download_name.split(".")[-1] == "exe":
            return EXE
        elif formula.download_name.split(".")[-1] == "msi":
            return MSI
    return NOT_INSTALLABLE
	
def import_formula(formula_name):
    try:
        formula_name_cap = formula_name[0].capitalize() + formula_name[1:]
        cmd_import = "from pkgit.formulas.%s import %s" %(formula_name,formula_name_cap)
        exec(cmd_import, globals(), locals())
    except ImportError:
        print
        print("Cannot find formula %s. Maybe it is misspelled" %formula_name)
        print("You can only use formulas: %s" %str(formulas())[1:-1])
        print
        raise
    # instanciate formula
    cmd_instanciate = "%s" %formula_name_cap
    return eval(cmd_instanciate)		
	
def instanciate_formula(formula_name):
    try:
        formula_name_cap = formula_name[0].capitalize() + formula_name[1:]
        cmd_import = "from pkgit.formulas.%s import %s" %(formula_name,formula_name_cap)
        exec(cmd_import, globals(), locals())
    except ImportError:
        print
        print("Cannot find formula %s. Maybe it is misspelled" %formula_name)
        print("You can only use formulas: %s" %str(formulas())[1:-1])
        print
        raise
    # instanciate formula
    cmd_instanciate = "%s()" %formula_name_cap
    return eval(cmd_instanciate)	

__oldsyspath__ = sys.path[:]

'''
OPENALEA_PI = "http://openalea.gforge.inria.fr/pi"
OPENALEA_REPOLIST = "http://openalea.gforge.inria.fr/repolist"
def get_repo_list():
    """ Return the list of OpenAlea repository """
    import urllib
    try:
        ret = []
        u = urllib.urlopen(OPENALEA_REPOLIST)
        for i in u:
            ret.append(i.strip())
        return ret

    except Exception, e:
        print e
        return [OPENALEA_PI]

pi = PackageIndex(search_path=[])
pi.add_find_links(get_repo_list())
'''
sj = os.pathsep.join

def uj(*args):
    """Unix-style path joining, useful when working with qmake."""
    return "/".join(args)
    
def get_logger():
    # TODO : doesn't write in the file if user doesn't want
    logger = logging.Logger('log')
    hdlr = logging.FileHandler('./formula.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter) 
    logger.addHandler(hdlr) 
    return logger    

logger = get_logger()

# A file object to redirect output to NULL:
NullOutput = open("NUL", "w")
    
############################################
# A few decorators to factor out some code #
############################################
def try_except( f ) :
    """Encapsulate the function in a try...except structure
    which prints the exception traceback and returns False on exceptions
    or returns the result of f on success."""
    def wrapper(self, *args, **kwargs):
        try:
            ret = f(self, *args, **kwargs)
        except:
            traceback.print_exc()
            return False
        else:
            return ret
    wrapper.__name__ = f.__name__
    return wrapper

def in_dir(directory):
    def dir_changer( f ) :
        """Encapsulate f in a structure that changes to getattr(self,directory),
        calls f and moves back to BuildEnvironment.get_working_path()"""
        def wrapper(self, *args, **kwargs):
            d_ = rgetattr(self, directory)
            message = "Changing to %s for %s" %(d_,f.__name__)
            logger.info(message)
            if not path(d_).exists():
                makedirs(d_)
            os.chdir(d_)
            ret = f(self, *args, **kwargs)
            os.chdir(self._get_working_path())
            return ret
        wrapper.__name__ = f.__name__
        return wrapper
    return dir_changer
    
def with_original_sys_path(f):
    """Calls the decorated function with the original PATH environment variable"""
    def func(*args,**kwargs):
        cursyspath = sys.path[:]
        sys.path = __oldsyspath__[:]
        ret = f(*args, **kwargs)
        sys.path = cursyspath
        return ret
    return func
   
def make_silent(self, silent):
        if silent:
            sys.stdout = self.null_stdout
            sys.stderr = self.null_stdout
        else:
            sys.stdout = self.original_stdout
            sys.stderr = self.original_stderr
            
def memoize(attr):
    def deco_memoize(f):
        def wrapper(self, *args, **kwargs):
            if getattr(self, attr, None) is None:
                v = f(self, *args, **kwargs)
                setattr(self, attr, v)
            return getattr(self, attr)
        return wrapper
    return deco_memoize
    
def option_to_sys_path(option):
    """If optionnal argument "option" was provided on the command line
    it will be prepended to the PATH just for the call this function decorates.
    After the call, the original environment will be restored."""
    def func_decorator(f):
        def wrapper(self, *args, **kwargs):
            opt_pth = self.options.get(option)
            if opt_pth:
                prev_pth = os.environ["PATH"]
                os.environ["PATH"] = sj([opt_pth, prev_pth])
                ret = f(self, *args, **kwargs)
                os.environ["PATH"] = prev_pth
            else:
                message = "option_to_sys_path: %s not provided" %option
                logger.warn(message)
                ret = f(self, *args, **kwargs)
            return ret
        return wrapper
    return func_decorator
   
def option_to_python_path(option):
    """If optionnal argument "option" was provided on the command line
    it will be appended to the PYTHONPATH and sys.path vars just for the
    call this function decorates. After the call, the original environment
    will be restored."""
    def func_decorator(f):
        def wrapper(self, *args, **kwargs):
            opt_pth = self.options.get(option)
            if opt_pth:
                # save original values
                prev_pth = sys.path[:]
                prev_py_pth = os.environ.get("PYTHONPATH", "")
                # modify environment
                sys.path += opt_pth.split(";")
                os.environ["PYTHONPATH"] = sj([opt_pth, prev_py_pth])
                # call the function
                ret = f(self, *args, **kwargs)
                # restore original values
                sys.path = prev_pth
                os.environ["PYTHONPATH"] = prev_py_pth
            else:
                message = "option_to_python_path: %s not provided" %option
                logger.warn(message)
                ret = f(self, *args, **kwargs)
            return ret
        return wrapper
    return func_decorator
   
############################################
# Useful small functions                   #
############################################

def sh(cmd,shell=True):
    """ Execute a cmd """
    return subprocess.call(cmd, shell=shell)

def url(name, dir=None, dl_name=None):
    """ Download from url into dir and renamed it into dl_name. 
    
    TODO : percentage download thanks to http://stackoverflow.com/questions/13909900/progress-of-python-requests-post
    """
    logger.info("Download %s in %s" %(dl_name,dir))
    ret = True
    
    if dir is None:
        dir = '.'
    dir = path(dir).abspath()
    if not dir.exists():
        makedirs(dir)
    
    filename = name.split('/')[-1]
    filename = filename.split('#')[0]
    complete_fn = dir/filename
    if dl_name:
        complete_fn = dir/dl_name

    try:
        reponse = requests.get(name)
        with open(complete_fn, "wb") as code:
            code.write(reponse.content)
            logger.info("%s downloaded." %filename)
            ret = complete_fn
    except:
        ret = False
        
    return ret
 
def install(filename):
    ext = filename.split(".")[-1]
    ret = False
    if ext.lower() == "msi":
        ret = sh('msiexec /i %s' %filename) == 0
        logger.info("%s Installed." %filename)
    elif ext.lower() == "exe":
        ret = sh(filename) == 0
        logger.info("%s Installed." %filename)
    else:
        logger.info("---We can't install %s. Unknow extension.---" %filename)
    return ret
 
def apply_patch_from_file(patchfile):
    """ Apply patch from file
    """
    p = fromfile(patchfile)
    return p.apply()   
    
def apply_patch_from_string(patchstring, root=None):
    """ Apply patch from string
    """
    p = fromstring(patchstring)
    
    print "****"
    if p is False:
        print "Can't patch!"
    else:
        print p.apply(root=root)
    print "****"
    
    return p

def get_dirs():
    """ Return list of directories to create.
        - install dir (install): where 3rd party will be installed
        - source dirs (src): where svn dirs will be checkout
        - egg dirs (egg): where "bdist_egg" will work
        - download dirs (dl) : where files will be download
        - dist dirs (dist) : where the final release files will be copied
    """
    cwd = path(os.getcwd())
    dirs = [
       cwd/"dl",
       cwd/"src",
       cwd/"install",
       cwd/"dist",
       cwd/"egg",
       ]
    return dirs

def safe_rmdir(dirname, listdir):
    """ Remove dirname only if exists in listdir
    """
    if dirname in listdir:
        listdir.remove(dirname)    
    
def rm_temp_dirs():
    """ Remove old directories."""
    dirs = get_dirs()
    for f in dirs:
        if f.exists():
            if f.isdir():
                f.rmtree()
            else:
                f.remove()
        else:
            logger.info( "Can't remove %s" %f)
    
def mk_temp_dirs():
    """ Create the working directories:
    """
    dirs = get_dirs()
    makedirs(dirs)

def download_egg(eggname, dir):
    """Download an egg to a specific place
    
    :param eggname: name of egg to download
    :param dir: destination directory
    :return: local path
    """
    logger.info("Downloading %s"%eggname)
    return pi.download(eggname, dir)
        
def checkout(url, dir=None):
    """ Checkout (SVN) url into dir
    """
    if dir is None:
        dir = '.'
    dir = path(dir)
    cmd = "svn co %s %s " %(url, dir)
    return sh(cmd) == 0
    
def set_windows_env():
    """ Set window environment path
    """
    cmd = "set PATH=%INNO_PATH%;%SVN_PATH%;%PYTHON_PATH%;%PYTHON_PATH%\Scripts;%PATH%"
    return sh(cmd) == 0
'''
def unpack(arch, where):
    """ Unpack a ZIP, TGZ or TAR file from 'where'
    """
    arch = arch
    base, ext = splitext( arch )
    logger.debug("unpacking %s" %arch)
    # TODO : verify that there is no absolute path inside zip.
    if ext == ".zip":
        zipf = zipfile.ZipFile( arch, "r" )
        zipf.extractall( path=where )
    elif ext == ".tgz":
        tarf = tarfile.open( arch, "r:gz")
        tarf.extractall( path=where )
    elif ext == ".tar":
        tarf = tarfile.open( arch, "r")
        tarf.extractall( path=where )
    logger.debug("done")
    return True
'''   
def unpack(arch, where):
    """ Unpack a ZIP, TGZ or TAR file from 'where'
    """
    arch = arch
    base, ext = path( arch ).splitext()
    logger.info("Unpacking %s in %s" %(arch,where))
    # TODO : verify that there is no absolute path inside zip.
    if ext == ".zip":
        zipf = zipfile.ZipFile( arch, "r" )
        zipf.extractall( path=where )
    elif ext == ".tgz":
        tarf = tarfile.open( arch, "r:gz")
        tarf.extractall( path=where )
    elif ext == ".tar":
        tarf = tarfile.open( arch, "r")
        tarf.extractall( path=where )
    logger.info("Unpack done.")
    
    # If ZIP contained only one directory, unpack move everything.
    # ex:
    # ./ann_src.zip/ann_1.1.2/... will begin after unpack ./ann_src/...
    where = path(where).abspath()
    listdirs = os.listdir(where)
    if len(listdirs) == 1:
        from_dirs = where/listdirs[0]
        move(from_dirs, where)
    return True
    
def move(from_src, to_src):
    """ Move a tree from from_src to to_src.
    """
    # If 'from' inside 'to' move in a temp repo and works well
    if to_src in from_src:
        temp_src = path(to_src)/".."/".temp"
        shutil.move(from_src, temp_src)
        from_src = temp_src
    # If 'to' already exists, erase it... Careful!
    if path(to_src).exists():
        shutil.rmtree(to_src)
    shutil.move(from_src, to_src)
    return True

class StrictTemplate(string.Template):
    idpattern = r"[_A-Z0-9]*"
    
class Later(object):
    """ Just a way to be able to check if a process should be done later,
    and not mark it as done or failed (the third guy in a tribool)"""
    pass

def rgetattr(c, attrs):
    """Like getattr, except that you can provide sub attributes:

    >>> rgetattr(obj, "attr.subattr")
    """
    attrs = attrs.split(".")
    value = c
    while len(attrs):
        value = getattr(value, attrs.pop(0))
    return value

class TemplateStr(string.Template):
    delimiter = "@"
    
def into_subdir(base, pattern):
    if pattern is not None:
        pths = glob.glob(path(base)/pattern)
        if len(pths):
            return pths[0]
        else:
            return None
    else:
        return base
        
CompiledRe = type(re_compile(""))
def recursive_glob(dir_, patterns=None, strip_dir_=False, levels=-1):
    """ Goes down a file hierarchy and returns files paths
    that match filepatterns or regexp."""
    files = []
    if isinstance(patterns, CompiledRe):
        filepatterns, regexp = None, patterns
    else:
        filepatterns, regexp = patterns.split(","), None

    lev = 0
    for dir_path, sub_dirs, subfiles in os.walk(dir_):
        if lev == levels:
            break
        if filepatterns:
            for pat in filepatterns:
                for fn in fnmatch.filter(subfiles, pat):
                    files.append( path(dir_path)/fn )
        elif regexp:
            for fn in subfiles:
                if regexp.match(fn): files.append(os.path.join(dir_path, fn))
        lev += 1
    dirlen = len(dir_)
    return files if not strip_dir_ else [ f[dirlen+1:] for f in files]

def recursive_glob_as_dict(dir_, patterns=None, strip_dir_=False,
                           strip_keys=False, prefix_key=None, dirs=False, levels=-1):
    """Recursively globs files and returns a list of the globbed files.
    The globbing can use regexps or shell wildcards.
    """
    files     = recursive_glob(dir_, patterns, strip_dir_, levels)
    by_direct = defaultdict(list)
    dirlen = len(dir_)
    for f in files:
        # target_dir = split(f)[0]
        target_dir = path(f).splitpath()[0]
        if strip_keys:
            target_dir = target_dir[dirlen+1:]
        if prefix_key:
            target_dir = path(prefix_key)/target_dir
        if dirs:
            # f = os.path.split(f)[0]
            f = path(f).splitpath()[0]
            if f not in by_direct[target_dir]:
                by_direct[target_dir].append(f)
        else:
            by_direct[target_dir].append(f)
    return by_direct
    
    
def ascii_file_replace(fname, oldstr, newstr):
    """ Tries to find oldstr in file fname and replaces it with newstr.
    Doesn't do anything if oldstr is not found.
    File is overwritten. Doesn't handle any exception.
    """
    txt = ""
    patch = False
    with open(fname) as f:
        txt = f.read()

    if oldstr in txt:
        patch = True
        txt = txt.replace(oldstr, newstr)

    if patch:
        with open(fname, "w") as f:
            logger.info("Patching %s" %fname)
            f.write(txt)
            
def merge_list_dict(li):
    """ Converts li which is a list of (key,value) into
    a dictionnary where items with the same keys get appended
    to a list instead of overwriting the key."""
    d = defaultdict(list)
    for k, v in li:
        d[k].extend(v)
    return dict( (str(k), str(sj(v))) for k,v in d.iteritems() )
    
# -- Glob and regexp patterns --
class Pattern:
    # -- generalities --
    any     = "*"
    exe     = "*.exe"
    dynlib  = "*.dll"
    stalib  = "*.a"
    include = "*.h,*.hxx"

    # -- pythonities --
    pymod   = "*.py"
    pyext   = "*.pyd"
    pyall   = ",".join([pymod, pyext])

    # -- scintillacities --
    sciapi  = "*.api"

    # -- sip --
    sipfiles = "*.sip"

    # -- Qtities --
    qtstalib = "*.a,*.prl,*.pri,*.pfa,*.pfb,*.qpf,*.ttf,README"
    qtsrc    = "*"#.pro,*.pri,*.rc,*.def,*.h,*.hxx"
    qtinc    = re_compile(r"^Q[0-9A-Z]\w|.*\.h|^Qt\w")
    qtmkspec = "*"
    qttransl = "*.qm"
    
def recursive_copy(sourcedir, destdir, patterns=None, levels=-1, flat=False):
    """Like shutil.copytree except that it accepts a filepattern or a file regexp."""
    src = recursive_glob( sourcedir, patterns, levels=levels )
    dests = [destdir]*len(src) if flat else \
            [ path(destdir)/f[len(sourcedir)+1:] for f in src]
    # bases = set([ split(f)[0] for f in dests])
    bases = set([ path(f).splitpath()[0] for f in dests])
    for pth in bases:
        makedirs(pth)
    for src, dst in zip(src, dests):
        shutil.copy(src, dst)
        
def makedirs(pth, verbose=False):
    """ A wrapper around os.makedirs that prints what
    it's doing and catches harmless errors. """
    try:
        os.makedirs( pth )
    except os.error:
        if verbose:
            traceback.print_exc()
         
def get_python_scripts_dirs():
    dirs = []
    for pth in sorted(sys.path):
        pth = [part for part in pth.split(os.sep)]
        try:
            pth_low = [part.lower() for part in pth]
            idx = pth_low.index("lib")
        except:
            continue
        else:
            script_dir_name = "scripts" if sys.platform == "win32" else "bin"
            script_path = path(*pth[:idx])/[script_dir_name]
            # sys.path contains absolute namesso the split operation above has to
            # be compensated:
            if sys.platform == "win32":
                # restore "driveletter:\\" on windows
                script_path = script_path.replace(":", ":"+os.sep)            
            else:
                # restore "/" on unixes
                script_path = "/"+script_path
            if script_path not in dirs:
                dirs.append(script_path)
    return dirs
    
    
