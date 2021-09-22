import bpy
from bpy.props import PointerProperty,FloatProperty
from AddonFolder import muscleCore
parentMuscleGenerated = False
originSelected=False
allowAttachmentSelection=False
curveCreated=False

class Nico_Test_Panel_PT_(bpy.types.Panel):

    

    bl_idname = "MyoGenerator"
    bl_label = "MyoGenerator: create muscle"
    bl_category = "MyoGenerator"
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
        row.operator( "view3d.attch", text="Start Origin Selection")
        row.enabled=context.scene.origin_object is not None
        
        row = layout.row()
        col1=layout.column()
        col1.operator('view3d.select_origin', text= "Submit Origin")
        col1.enabled =  context.scene.origin_object is not None

        col1=layout.column()
        col1.prop(context.scene, "insertion_object", text='Insertion\'s Bone')
        #col1.enabled=allowAttachmentSelection   

        row = layout.row()
        row.operator( "view3d.attch", text="Start Insertion Selection")
      
        col2=layout.column()
        col2.operator('view3d.select_insertion', text= "Submit Insertion")
        col2.enabled =  context.scene.insertion_object is not None
        
        row = layout.row()
        row.operator("view3d.muscle_creation", text = "Create Muscle Boundaries")

        row = layout.row()
        row.operator("view3d.curve_creator", text = "Create Muscle Curve")

        row = layout.row()
        row.prop(context.scene, "bevel",text="Bevel Start", slider=True) 
        row.enabled=curveCreated

        row = layout.row()
        row.prop(context.scene, "bevel2",text="Bevel End", slider=True) 
        row.enabled=curveCreated
        
        row = layout.row()
        row.prop(context.scene, "tilt",text="Set Tilt", slider=True) 
        # row.enabled=curveCreated
        


        row=layout.row()
        row.operator("view3d.convert_to_mesh", text ="Convert Curve To Mesh")

        row=layout.row()
        row.operator("view3d.join_muscle", text = "Join Muscle")


        