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
    "name" : "Test_Addon",
    "author" : "Niccolo Fioritti",
    "description" : "TestAddon",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : "Generic"
}


from AddonFolder.muscleCore import curve_creator
import bpy

#from muscleCore.create_muscle_empties import *
#import bpy.utilis


from . test_op import Nico_Select_Muscle_Op, Nico_Select_Origin_Op,Nico_Select_Insertion_Op,Nico_AllowAttach_Op, Nico_Muscle_Creation_Op,Nico_Curve_Creator_Op

from . test_panel import Nico_Test_Panel_PT_
#classes =(Nico_Test_Op, Nico_Test_Panel_PT_)
#register, unregister = bpy.utils.register_classes_factory(classes)


# REF FOR BUTTON TO MAKE BUTTONS: https://blender.stackexchange.com/questions/57545/can-i-make-a-ui-button-that-makes-buttons-in-a-panel

#OTHER REF GENERAL BLENDER ADDONS: https://b3d.interplanety.org/en/calling-functions-by-pressing-buttons-in-blender-custom-ui/

#REF GRAYOUT BUTTONS: https://blenderartists.org/t/gray-out-a-panel-button/522047/2

#REF GRAOUT BUTTONS 2 https://blender.stackexchange.com/questions/160883/contextually-grey-out-panel-element-in-python-2-8


def register():
    bpy.utils.register_class(Nico_Select_Muscle_Op)
    bpy.utils.register_class(Nico_Select_Origin_Op)
    bpy.utils.register_class(Nico_Select_Insertion_Op)
    bpy.utils.register_class(Nico_AllowAttach_Op)
    bpy.utils.register_class(Nico_Test_Panel_PT_)
    bpy.utils.register_class( Nico_Muscle_Creation_Op)
    bpy.utils.register_class(Nico_Curve_Creator_Op)
    

    
    bpy.types.Scene.origin_object =bpy.props.PointerProperty \
    (
                
        type=bpy.types.Object,        
        name = "origin object"
       # description = "asd",
        #default ='asd'
    )
        
    bpy.types.Scene.insertion_object =bpy.props.PointerProperty \
    (
                
        type=bpy.types.Object,        
        name = "insertion_object"
       # description = "asd",
        #default ='asd'
    )
        

    bpy.types.Scene.muscle_Name=bpy.props.StringProperty \
        (
            name = "Muscle Name",
            description = "Insert your muscle name",
            default ='Insert  muscle name'
        )
    bpy.types.Scene.origin_Name=bpy.props.StringProperty \
        (
            name = "Origin Name",
            description = "Insert origin name",
            default ='Insert origin name'
        )
    bpy.types.Scene.insertion_Name=bpy.props.StringProperty \
        (
            name = "Insertion Name",
            description = "Insert insertion name",
            default ='Insert insertion name'
        )




    #NEED TO ADD PROPERTY Scene.theChosenObject



#### FOR OBJECT EYEDROPPER: https://blender.stackexchange.com/questions/30487/object-selection-box-with-eyedropper

def unregister():
    bpy.utils.register_class(Nico_Select_Muscle_Op)
    bpy.utils.register_class(Nico_Select_Origin_Op)
    bpy.utils.register_class(Nico_Select_Insertion_Op)
    bpy.utils.register_class(Nico_AllowAttach_Op)
    bpy.utils.register_class(Nico_Test_Panel_PT_)
    bpy.utils.register_class( Nico_Muscle_Creation_Op)
    bpy.utils.register_class(Nico_Curve_Creator_Op)
    del bpy.types.Scene.muscle_Name
    
