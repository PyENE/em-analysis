"""SCons.Tool.lex

Tool-specific initialization for lex.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""

__license__ = "Cecill-C"
__revision__ = " $Id: lex.py 2247 2010-02-08 17:14:26Z cokelaer $"
#
# Copyright (c) 2001, 2002, 2003, 2004 The SCons Foundation
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import SCons.Defaults
import SCons.Tool
import SCons.Util

ll_suffix = ['.l', '.ll']

LexAction = SCons.Action.Action("$LEXCOM") # , "$LEXCOMSTR")

def generate(env):
    """Add Builders and construction variables for lex to an Environment."""
    c_file, cxx_file = SCons.Tool.createCFileBuilders(env)

    c_file.add_action( '.l', LexAction)
    for ll in ll_suffix:
        cxx_file.add_action( ll, LexAction)

    env['LEX']      = env.Detect('flex') or 'lex'
    env['LEXFLAGS'] = SCons.Util.CLVar('')
    env['LEXCOM']   = '$LEX $LEXFLAGS -t $SOURCES > $TARGET'

def exists(env):
    return env.Detect(['flex', 'lex'])

