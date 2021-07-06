import bpy
from bpy.props import PointerProperty
from AddonFolder import muscleCore
parentMuscleGenerated = False
originSelected=False
allowAttachmentSelection=False

class Nico_Test_Panel_PT_(bpy.types.Panel):

    

    bl_idname = "Nico_Test_Panel"
    bl_label = "Test Panel Label"
    bl_category = "Test Addon"
    bl_space_type ="VIEW_3D"
    bl_region_type = "UI"

    def draw(self,context):
        layout = self.layout

        layout.prop(context.scene, "theChosenObject")
        row = layout.row()
        row.prop(context.scene, "muscle_Name", text ="Muscle Name")  
        
        row = layout.row()
        row.operator('view3d.submit_button', text= "Submit Muscle")    # operator idname . it'll invoce the execute function of operator
        
        row = layout.row()
        row.operator( "view3d.attch", text="Select Attachments")


        #row = layout.row()
        col1=layout.column()
      #  col1.prop(context.scene, "selected_object", text='Origin\'s Bone')
      #  col1.enabled=allowAttachmentSelection    #maybe check if selected face ' is not None '
        #row = layout.row()
        col1=layout.column()
        col1.operator('view3d.select_origin', text= "Select Origin")
        col1.enabled =  allowAttachmentSelection

        col1=layout.column()
      #  col1.prop(context.scene, "selected_object", text='Origin\'s Bone')
      #  col1.enabled=allowAttachmentSelection    #maybe check if selected face ' is not None '
        col2=layout.column()
        col2.operator('view3d.select_insertion', text= "Select Insertion")
        col2.enabled =  originSelected and allowAttachmentSelection
        

    
        