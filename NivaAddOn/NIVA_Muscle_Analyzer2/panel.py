# pylint: skip-file
import bpy
from bpy.types import Panel

class MUSCLE_MEASURE_PT_Panel(Panel):
    bl_space_type = "VIEW_3D"  #this can be changed: where is it displayed
    bl_region_type = "UI"
    bl_label = "Muscle Analyzer"
    bl_category= "Muscle Analyzer"

    def draw(self,context):
        layout=self.layout

        row=layout.row()  #creates a col within the row previosuly defined
        row.prop(context.scene, "file_name", text ="Name")              #we dont have properties yet
        #print (context.scene)

        row=layout.row()  #creates a col within the row previosuly defined
        row.prop(context.scene, "conf_path", text ="")              #we dont have properties yet
        #print (context.scene)

        row=layout.row()
        col=row.column()  #creates a col within the row previosuly defined
        col.operator("object.analyze_all", text = "Make sure you are in Object Mode")              #operatorId needs to be defined!!






