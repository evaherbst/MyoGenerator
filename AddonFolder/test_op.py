import bpy

class Nico_Select_Muscle_Op(bpy.types.Operator):
    bl_idname = "view3d.submit_button"
    bl_label = "Nico Test Operator"
    bl_description = "Centre Cursor Test"

    def execute(self,context):
        #function to execute

        print('executing function test')
        return{'FINISHED'}




class Nico_Select_Origins_Op(bpy.types.Operator):
    bl_idname = "view3d.select_origins"
    bl_label = "Select Origins"
    #bl_description = "Centre Cursor Test"

    def execute(self,context):
        #function to execute

        print('executing function test')
        return{'FINISHED'}

