/* -*-c++-*- 
 *  ----------------------------------------------------------------------------
 *
 *       AMAPmod: Exploring and Modeling Plant Architecture 
 *
 *       Copyright 1995-2010 UMR Cirad/Inra Modelisation des Plantes
 *
 *       File author(s): Ch. Godin (christophe.godin@cirad.fr) 
 *
 *       Forum for AMAPmod developers    : amldevlp@cirad.fr
 *               
 *  ----------------------------------------------------------------------------
 * 
 *                      GNU General Public Licence
 *           
 *       This program is free software; you can redistribute it and/or
 *       modify it under the terms of the GNU General Public License as
 *       published by the Free Software Foundation; either version 2 of
 *       the License, or (at your option) any later version.
 *
 *       This program is distributed in the hope that it will be useful,
 *       but WITHOUT ANY WARRANTY; without even the implied warranty of
 *       MERCHANTABILITY or FITNESS For A PARTICULAR PURPOSE. See the
 *       GNU General Public License for more details.
 *
 *       You should have received a copy of the GNU General Public
 *       License along with this program; see the file COPYING. If not,
 *       write to the Free Software Foundation, Inc., 59
 *       Temple Place - Suite 330, Boston, MA 02111-1307, USA.
 *
 *  ----------------------------------------------------------------------------
 */				




#ifndef _DIRNAMES_H__
#define _DIRNAMES_H__

/*! \file dirnames.h
    \brief File for filename queries.
*/

#include <string>
#include "tools_namespace.h"

VPTOOLS_BEGIN_NAMESPACE

/*! get the directory part of a filename (the filename might be not expanded).
    the filename stored  "../../fruit.drf" or fruit.drf for example.
    get_dirname() returns ../.. and . respectively
*/
std::string VPTOOLS_API get_dirname(const std::string& filename);

/*! get the file part (not directory name part) of a filename (the filename might be not expanded).
    the filename might be "../../fruit.drf" or fruit.drf for example.
    get_notdirname returns fruit.drf in both cases.
*/
std::string VPTOOLS_API get_filename(const std::string& filename);

/*! Expands the forms ./../ in a filename and resolves the symbolic links.
 */
std::string VPTOOLS_API absolute_dirname(const std::string& filename);

/*! Expands the forms ./../ in a filename and resolves the symbolic links.
 */
std::string VPTOOLS_API absolute_filename(const std::string& filename);


/*! Expands filename in a short name on win32 else do nothing.
 */
std::string VPTOOLS_API short_dirname(const std::string& filename);


/*! Gets the name of the current working directory. The string is empty if an error occured.
 */
std::string VPTOOLS_API get_cwd();

/*! changes the current working directory to newdir. New dir can integrate '.' chars that
    are thus interpreted according to the former working directory. Returns true if succeeded.
 */
bool VPTOOLS_API chg_dir(const std::string& newdir);

/*! adds a suffix to filename. Returns true if the suffix is actually added
    and false if the suffix was already present at the end of the filname
    (and therefore was not added)
*/
std::string VPTOOLS_API append_suffix(const std::string& filename, const std::string& suffix);

/*! cat a dirname and a filename to make up a complete filename
    ex: cat_dir_file("../foodir", "name1") -> "../foodir/name1"
    ex: cat_dir_file("../foodir/", "name1")-> "../foodir/name1"
*/
std::string VPTOOLS_API cat_dir_file(const std::string &filename, const std::string &);

/*!
 Return the extension of filename. If none exist, return empty string.
*/
std::string VPTOOLS_API get_suffix(const std::string& filename);

/*!
  Change the current extension of the filename by \e ext.
*/
std::string VPTOOLS_API set_suffix(const std::string& filename,const std::string& ext);

/*!
  Return whether the file already exists.
*/
bool VPTOOLS_API exists(const std::string& filename);

/*!
  Return whether 2 filename are similar.
*/
bool VPTOOLS_API similar_dir(const std::string& filename,const std::string& filename2);

bool VPTOOLS_API copy(const std::string& src,const std::string& dest);


VPTOOLS_END_NAMESPACE

#endif
