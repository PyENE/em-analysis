/* -*-c++-*-
 *  ----------------------------------------------------------------------------
 *
 *       PlantGL: Plant Graphic Library
 *
 *       Copyright 1995-2003 UMR Cirad/Inria/Inra Dap - Virtual Plant Team
 *
 *       File author(s): F. Boudon
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



#ifndef __util_tool_hash_h__
#define __util_tool_hash_h__

#include "config.h"

/*! \file util_hash.h
    \brief Utility for hashing std::string.
*/

#include <string>


#ifndef WIN32_STL_EXTENSION

/**
   \strust eqstr
   \brief Comparison between 2 string.
*/

struct tool_eqstr
{
  /// Compare the 2 string.
  bool operator() (const std::string& s1, const std::string& s2) const
    { return s1 == s2; }
};


/**
   \strust hashstr
   \brief Find using a hasher a place for the string.
*/
struct tool_hashstr
{
  typedef tool_hash<const char*> hash_cstr;

  /// hash of the string.
  std:size_t operator() (const std::string& s1) const
    { return my_hasher(s1.c_str()); }

   hash_cstr my_hasher;
};


#endif

#endif
