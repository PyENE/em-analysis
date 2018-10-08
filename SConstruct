# -*-python-*-

from openalea.sconsx import config, environ
import os
pj = os.path.join
ALEASolution = config.ALEASolution

options = Variables(['../options.py', 'options.py'], ARGUMENTS)
options.Add(BoolVariable('with_test', 'build test modules', 0))
options.Add(BoolVariable('with_efence', 'build tests with efence library', 0))

tools = ['boost_python', 'vplants.tool','vplants.stat_tool','vplants.sequence_analysis','qt4', 'install', 'alea']

env = ALEASolution(options, tools)

# Build stage
prefix = env['build_prefix']
#SConscript(pj(prefix,"src/cpp/SConscript"),
#           exports='env')
#SConscript(pj(prefix,"src/wrapper/SConscript"),
#           exports='env')

if env['with_test']:
    SConscript(pj(prefix,"test/cpp/SConscript"), exports="env")

import compileall
compileall.compile_dir('./src', force=True)
