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


/*! \file readline.h
    \brief File for readline initialisation.
	Enable only with GNUC.
*/


#ifndef __readline_h__
#define __readline_h__

#if defined( __GNUC__ ) && ! defined(  __MINGW32__ )
#define USE_READLINE
#endif

#ifdef USE_READLINE
/// Init readline or do nothing.
extern void gnu_init_readline();
/// Set the keyword or do nothing.
extern void setKeyword(char ** keyword);
/// Completion Function or do nothing.
extern int readline_input(char*, const char* prompt=0);

#endif

#endif
