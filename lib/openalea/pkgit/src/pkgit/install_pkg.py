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

from argparse import ArgumentParser
from pkgit import install_formula

def main():
    # options
    parser = ArgumentParser(prog='install_pkg')
    parser.add_argument('package', type=str, default="openalea",
                         help='Package to install. It can be "openalea", "vplants", "alinea" or other classical package like "qt4", "rpy2", "cgal"...')
                         
                  
    args = parser.parse_args()

    package_name = args.package
    install_formula(package_name)
    
if __name__ == '__main__':
    main()