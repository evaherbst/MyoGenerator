import bpy
import sys 


#from Muscle_Volume_Sculptor import create_muscle_empties 


class Nico_Select_Muscle_Op(bpy.types.Operator):
    bl_idname = "view3d.submit_button"
    bl_label = "Nico Test Operator"
    bl_description = "Centre Cursor Test"

    def execute(self,context):
        #function to execute
        objName = bpy.context.scene.muscle_Name

       # make_muscle_empties()

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

        print(originName, insertionName)

        #print('executing function test')
        return{'FINISHED'}

