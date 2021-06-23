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




class Nico_Select_Origins_Op(bpy.types.Operator):
    bl_idname = "view3d.select_origins"
    bl_label = "Select Origins"
    

    #bl_description = "Centre Cursor Test"

    def execute(self,context):
        #function to execute
        
        originName=bpy.context.scene.origin_Name
        insertionName=bpy.context.scene.insertion_Name

        muscleCore.attachments_names=[originName,insertionName]

        print("test", bpy.context.scene.muscle_Name)

        muscleCore.create_attachment(0,bpy.context.scene.muscle_Name)

        #print('executing function test')
        return{'FINISHED'}

