import bpy
import sys 


#from . muscleCore import make_muscle_empties
from AddonFolder import muscleCore
#from Muscle_Volume_Sculptor import create_muscle_empties 
from AddonFolder import test_panel

class Nico_Select_Muscle_Op(bpy.types.Operator):
    bl_idname = "view3d.submit_button"
    bl_label = "Nico Test Operator"
    bl_description = "Centre Cursor Test"

    def execute(self,context):
        #function to execute
        objName = bpy.context.scene.muscle_Name
        muscleCore.make_empty(objName)
       # make_muscle_empties()

        test_panel.parentMuscleGenerated = True

        print('executing function test')
      
        return{'FINISHED'}


class Nico_AllowAttach_Op(bpy.types.Operator):
    bl_idname="view3d.attch"
    bl_label = "Test"
    def execute(self,context):
        test_panel.allowAttachmentSelection=True
        muscleCore.set_edit_mode()
        return{'FINISHED'}

class Nico_Select_Origin_Op(bpy.types.Operator):
    bl_idname = "view3d.select_origin"
    bl_label = "Select Origin"

    def execute(self,context):
        test_panel.originSelected=True
        muscleCore.create_attachment(0,bpy.context.scene.muscle_Name)
        return{'FINISHED'}


class Nico_Select_Insertion_Op(bpy.types.Operator):
    bl_idname = "view3d.select_insertion"
    bl_label = "Select Insertion"

    def execute(self,context):

        muscleCore.create_attachment(1,bpy.context.scene.muscle_Name)
        return{'FINISHED'}
