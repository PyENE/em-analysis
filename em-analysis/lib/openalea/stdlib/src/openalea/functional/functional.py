# -*- python -*-
#
#       OpenAlea.StdLib
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################
""" Standard python functions for functional programming. """

__license__ =  "Cecill-C"
__revision__ = " $Id: functional.py 3612 2012-06-18 14:23:54Z pradal $ "

from openalea.core import Node, ITextStr, ICodeStr

def pymap(func, seq):
    """ map(func, seq) """

    if func is not None and seq is not None and len(seq):
        return ( map(func, seq), )
    else:
        return ( [], )


def pyfilter(func, seq):
    """ filter(func, seq) """

    if func is not None and seq is not None and len(seq):
        return ( filter(func, seq), )
    else:
        return ( [], )


def pyreduce(func, seq):
    """ reduce(func, seq) """

    if func is not None and seq is not None and len(seq):
        return ( reduce(func, seq), )
    else:
        return ( [], )



def pyapply(func, seq, one_argument=False):
    """ apply(func, seq)"""

    if one_argument:
        seq = [seq]

    if func is not None:
        return apply(func, seq)
    else:
        return ()

def pyifelse(val, cond, f, g):

    h = f if bool(cond) else g
    return h(val),

"""
def pyfunction(func_str):
    ''' creates a function from a text string '''

    if func_str:
        func_str = str(func_str)
        # Extract the function name
        l = func_str.split('\n')
        for line in l:
            if 'def ' in line:
                break
        name = line.split('def ')[1]
        name = name.split('(')[0]

        # local dictionary
        d = {}
        exec(str(func_str), d, globals())

        return d.get(name, None)
    else:
        return None
"""
class pyfunction(Node):
    """
    Function method

    :param ins: the function code
    :param outs: the function object
    """

    def __init__(self, ins, outs):
        Node.__init__(self, ins, outs)
        self.add_input( name="func_str", interface=ICodeStr)
        self.add_output( name="function")

    def __call__(self, inputs):
        """ inputs is the list of input values

        :returns: the value
        """
        func_str = inputs[0]
        if func_str is not None:
            # Extract the function name
            l = func_str.split('\n')
            line = ''
            for line in l:
                if 'def ' in line:
                    break
                if 'lambda ' in line:
                    break

            name = ''
            if 'def' in line:
                name = line.split('def ')[1]
                name = name.split('(')[0].strip()
            elif 'lambda' in line:
                name = line.split('=')[0].strip()
            else:
                return None

            self.set_caption(name)

            # local dictionary
            d = {}
            exec(str(func_str), d)

            return (d.get(name, None), )
        else:
            return None

