# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.

#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Muscle_Analyzer",
    "author" : "Eva Herbst, Niccolo Fioritti",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : "Generic"
}

# pylint: skip-file
import bpy

from . operators import MUSCLE_MEASURE_OT_All_Op
from . panel import  MUSCLE_MEASURE_PT_Panel
from bpy.props import *

classes =(MUSCLE_MEASURE_OT_All_Op, MUSCLE_MEASURE_PT_Panel)
def register():
    
    #bpy.types.Scene.conf_path = bpy.props.StringProperty \
    #bpy.path.basename.conf_path =bpy.props.StringProperty \
    
    bpy.types.Scene.conf_path = bpy.props.StringProperty \
        (
            name = "Path",
            default = "",
            #update = lambda s,c: make_path_absolute('conf_path'),
            description = "Select where to save your file...",
            subtype = "DIR_PATH"
        )
    bpy.types.Scene.file_name = bpy.props.StringProperty \
        (
            name = "File_Name",
            default = "",
            #update = lambda s,c: make_path_absolute('conf_path'),
            description = "Your file name. It will be exported as .csv",
            subtype = "FILE_NAME"
        )

    #conf_path: StringProperty(
    #        name = "Path",
    #        description = "Path to the folder containing the files to import",
    #        default = "",
    #        subtype = 'DIR_PATH'
    #        )

    

    
    for c in classes:
        bpy.utils.register_class(c)
      

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    del bpy.types.Scene.conf_path
