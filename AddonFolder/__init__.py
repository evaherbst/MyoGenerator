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


import bpy

from AddonFolder.muscleCore import curve_creator

from .myoGenerator_op import (AllowAttach_Op, Calculate_Volume_Op,
                              Curve_Creator_Op, Join_Muscle_Op,
                              Muscle_Creation_Op, Reset_Variables_Op,
                              Select_Insertion_Op, Select_Muscle_Op,
                              Select_Origin_Op, SetBevel2_Op, SetBevel_Op,
                              SetTilt_Op, Transform_To_Mesh_Op)
from .myoGenerator_panel import myoGenerator_panel_PT_

bl_info = {
    "name": "MyoGenerator",
    "author": "Niccolo Fioritti and Eva Herbst",
    "description": "This add-on enables generation of 3D muscles based on user selected origin and insertion areas and an adjustable muscle path.",
    "blender": (2, 80, 0),
    "version": (0, 0, 1),
    "location": "View3D",
    "doc_url": "https://github.com/evaherbst/-Muscle_Volume_Sculptor/blob/main/README.md",
    "warning": "",
    "category": "Mesh"
}


def register():
    bpy.utils.register_class(Select_Muscle_Op)
    bpy.utils.register_class(Select_Origin_Op)
    bpy.utils.register_class(Select_Insertion_Op)
    bpy.utils.register_class(AllowAttach_Op)
    bpy.utils.register_class(myoGenerator_panel_PT_)
    bpy.utils.register_class(Muscle_Creation_Op)
    bpy.utils.register_class(Curve_Creator_Op)
    bpy.utils.register_class(Join_Muscle_Op)
    bpy.utils.register_class(Transform_To_Mesh_Op)
    bpy.utils.register_class(SetBevel_Op)
    bpy.utils.register_class(SetBevel2_Op)
    bpy.utils.register_class(SetTilt_Op)
    bpy.utils.register_class(Calculate_Volume_Op)
    bpy.utils.register_class(Reset_Variables_Op)

    bpy.types.Scene.conf_path = bpy.props.StringProperty(
        name="Path",
        default="",
        description="Select where to save your file...",
        subtype="DIR_PATH"
    )
    bpy.types.Scene.file_name = bpy.props.StringProperty(
        name="File_Name",
        default="",
        description="Your file name. It will be exported as .csv",
        subtype="FILE_NAME"
    )

    bpy.types.Scene.origin_object = bpy.props.PointerProperty(

        type=bpy.types.Object,
        name="origin object"
    )

    bpy.types.Scene.insertion_object = bpy.props.PointerProperty(

        type=bpy.types.Object,
        name="insertion_object"
    )

    bpy.types.Scene.muscle_Name = bpy.props.StringProperty(
        name="Muscle Name",
        description="Insert your muscle name",
        default='Insert muscle name'
    )
    bpy.types.Scene.origin_Name = bpy.props.StringProperty(
        name="Origin Name",
        description="Insert origin name",
        default='Insert origin name'
    )
    bpy.types.Scene.insertion_Name = bpy.props.StringProperty(
        name="Insertion Name",
        description="Insert insertion name",
        default='Insert insertion name'
    )

    bpy.types.Scene.bevel = bpy.props.FloatProperty(
        name="bevel",
        min=0,
        max=1,
        update=SetBevel_Op.execute

    )

    bpy.types.Scene.bevel2 = bpy.props.FloatProperty(

        name="bevel2",
        min=0,
        max=1,
        update=SetBevel2_Op.execute

    )

    bpy.types.Scene.tilt = bpy.props.FloatProperty(

        name="tilt",
        min=0,
        max=360,
        update=SetTilt_Op.execute

    )


def unregister():
    bpy.utils.unregister_class(Select_Muscle_Op)
    bpy.utils.unregister_class(Select_Origin_Op)
    bpy.utils.unregister_class(Select_Insertion_Op)
    bpy.utils.unregister_class(AllowAttach_Op)
    bpy.utils.unregister_class(myoGenerator_panel_PT_)
    bpy.utils.unregister_class(Muscle_Creation_Op)
    bpy.utils.unregister_class(Curve_Creator_Op)
    bpy.utils.unregister_class(Join_Muscle_Op)
    bpy.utils.unregister_class(Transform_To_Mesh_Op)
    bpy.utils.unregister_class(SetBevel_Op)
    bpy.utils.unregister_class(SetBevel2_Op)
    bpy.utils.unregister_class(SetTilt_Op)
    bpy.utils.unregister_class(Calculate_Volume_Op)
    bpy.utils.unregister_class(Reset_Variables_Op)

    del bpy.types.Scene.muscle_Name
    del bpy.types.Scene.bevel
    del bpy.types.Scene.conf_path
    del bpy.types.Scene.file_name
