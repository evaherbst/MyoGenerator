import bpy

class Nico_Test_Panel_PT_(bpy.types.Panel):
    bl_idname = "Nico_Test_Panel"
    bl_label = "Test Panel Label"
    bl_category = "Test Addon"
    bl_space_type ="VIEW_3D"
    bl_region_type = "UI"

    def draw(self,context):
        layout = self.layout

        row = layout.row()
        row.prop(context.scene, "muscle_Name", text ="Muscle Name")  
        
        row = layout.row()
        row.operator('view3d.submit_button', text= "Submit Muscle")    # operator idname . it'll invoce the execute function of operator
        


        row = layout.row()
        col1=layout.column()
        col1.prop(context.scene, "origin_Name", text ="Origin Name")  
        col2=layout.column()
        col2.prop(context.scene, "insertion_Name", text ="Insertion Name")  
        row = layout.row()
        row.operator('view3d.select_origins', text= "Select Origins")