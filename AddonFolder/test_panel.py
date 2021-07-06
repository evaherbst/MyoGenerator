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
        


        row = layout.row()
        row.prop(context.scene, "muscle_Name", text ="Muscle Name")  
        
        row = layout.row()
        row.operator('view3d.submit_button', text= "Submit Muscle")    # operator idname . it'll invoce the execute function of operator
        


        #row = layout.row()
        col1=layout.column()
        col1.prop(context.scene, "origin_object", text='Origin\'s Bone')
        #col1.enabled=allowAttachmentSelection    #maybe check if selected face ' is not None '
       
        row = layout.row()
        row.operator( "view3d.attch", text="Select Origin")
        row.enabled=context.scene.origin_object is not None
        
        row = layout.row()
        col1=layout.column()
        col1.operator('view3d.select_origin', text= "Submit Origin")
        col1.enabled =  context.scene.origin_object is not None

        col1=layout.column()
        col1.prop(context.scene, "insertion_object", text='Insertion\'s Bone')
        #col1.enabled=allowAttachmentSelection   

        row = layout.row()
        row.operator( "view3d.attch", text="Select Insertion")
      
        col2=layout.column()
        col2.operator('view3d.select_insertion', text= "Submit Insertion")
        col2.enabled =  context.scene.insertion_object is not None


        
        row = layout.row()
        row.operator("view3d.muscle_creation", text = "Create Muscle Volume")

    
        