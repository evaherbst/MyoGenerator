import bpy

class Nico_Test_Panel(bpy.types.Panel):
    bl_idname = "Nico_Test_Panel"
    bl_label = "Test Panel Label"
    bl_category = "Test Addon"
    bl_space_type ="VIEW_3D"
    bl_region_type = "UI"

    def draw(self,context):
        layout = self.layout

        row = layout.row()
        row.operator('view3d.test_print', text= "button text")    # operator idname . it'll invoce the execute function of operator
