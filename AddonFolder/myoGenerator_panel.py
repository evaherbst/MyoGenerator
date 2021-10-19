import bpy

from bpy.props import PointerProperty, FloatProperty
from AddonFolder import muscleCore

parentMuscleGenerated = False
originSubmitted = False
insertionSubmitted = False
vertexCountMatched = False
curveCreated = False
curveToMesh = False

class myoGenerator_panel_PT_(bpy.types.Panel):

    bl_idname = "MyoGenerator"
    bl_label = "MyoGenerator: create muscle"
    bl_category = "MyoGenerator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(text="Data Storage Location")
        row = box.row()
        row.prop(context.scene, "conf_path", text="")

        row = box.row()
        row.prop(context.scene, "file_name", text="")

        layout.separator()

        box = layout.box()
        box.label(text="Muscle Id")
        row = box.row()
        row.prop(context.scene, "muscle_Name", text="Muscle Name")
        row.enabled = (context.scene.file_name != "")

        row = box.row()
        row.operator('view3d.submit_button', text="Submit Muscle")
        row.enabled = context.scene.muscle_Name != "Insert muscle name"

        layout.separator()

        box = layout.box()
        box.label(text="Origin Creation")
        row = box.row()
        row.prop(context.scene, "origin_object", text='Origin\'s Bone')


        row = box.row()
        col1=row.column()
        col1.operator("view3d.attch", text="Start Origin Selection")
        col1.enabled = context.scene.origin_object is not None

        col2 = row.column()
        col2.operator('view3d.select_origin', text="Submit Origin") 
        col2.enabled = context.scene.origin_object is not None

        layout.separator()

        box = layout.box()
        box.label(text="Insertion Creation")
        row1 = box.row()
        row1.prop(context.scene, "insertion_object", text='Insertion\'s Bone')
    
        row2 = box.row()
        col1 = row2.column()
        col1.operator("view3d.attch", text="Start Insertion Selection")
        col1.enabled = context.scene.insertion_object is not None

        col2 = row2.column()
        col2.operator('view3d.select_insertion', text="Submit Insertion")
        col2.enabled = context.scene.insertion_object is not None

        layout.separator()

        box = layout.box()
        box.label(text="Muscle Curve Creation")
        row = box.row()
        row.operator(
            "view3d.muscle_creation",
            text="Match Attachment Vertex Counts")
        row.enabled = (originSubmitted and insertionSubmitted)

        row = box.row()
        row.operator("view3d.curve_creator", text="Create Muscle Curve")
        row.enabled = vertexCountMatched

        layout.separator()

        box = layout.box()
        box.label(text="Edit Muscle Curve")
        row = box.row()
        row.prop(context.scene, "tilt", text="Set Tilt", slider=True)
        row.enabled = curveCreated

        row = box.row()
        row.prop(context.scene, "bevel", text="Bevel Start", slider=True)
        row.enabled = curveCreated

        row = box.row()
        row.prop(context.scene, "bevel2", text="Bevel End", slider=True)
        row.enabled = curveCreated

        layout.separator()

        box = layout.box()
        box.label(text="Muscle Finalization")
        row = box.row()
        row.operator("view3d.convert_to_mesh", text="Convert Curve To Mesh")
        row.enabled = curveCreated

        row = box.row()
        row.operator("view3d.join_muscle", text="Join Muscle")
        row.enabled = curveToMesh

        layout.separator()

        row = layout.row()
        row.operator("view3d.reset_variables", text="Next Muscle")

        layout.separator()

        row = layout.row()
        row.operator("view3d.calculate_volume", text="Calculate Volumes")
