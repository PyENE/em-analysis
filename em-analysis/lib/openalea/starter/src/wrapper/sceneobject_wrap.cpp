/*------------------------------------------------------------------------------
 *                                                                              
 *        OpenAlea.Starter: Example package                                     
 *                                                                              
 *        Copyright 2006 INRIA - CIRAD - INRA                      
 *                                                                              
 *        File author(s): Christophe Pradal <christophe.prada@cirad.fr>         
 *                        Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
 *                                                                              
 *        Distributed under the Cecill-C License.                               
 *        See accompanying file LICENSE.txt or copy at                          
 *            http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html       
 *                                                                              
 *        OpenAlea WebSite : http://openalea.gforge.inria.fr                    
 *       
 *        $Id: sceneobject_wrap.cpp 559 2007-05-25 12:25:30Z dufourko $
 *                                                                       
 *-----------------------------------------------------------------------------*/


/* WRAPPER Boost.python for the scene_object hierarchy */

#include "export_scene_object.h"

#include <boost/python.hpp>
using namespace boost::python;


// Define python module "sceneobject"
// Note : Python module and generated dll/so file must have the SAME NAME
BOOST_PYTHON_MODULE(_sceneobject)
{
  
  // Add scene_object wrapper
  class_scene_object();

}
