import bpy

class Nico_Test_Op(bpy.types.Operator):
    bl_idname = "view3d.test_print"
    bl_label = "Nico Test Operator"
    bl_description = "Centre Cursor Test"

    def execute(self,context):
        #function to execute

        print('executing function test')
        return{'FINISHED'}