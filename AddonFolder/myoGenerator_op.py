import math
import os
import sys

import bpy


from AddonFolder import muscleCore, myoGenerator_panel, vertex_Counter

isSubmittingOrigin = False


testAttch0 = "baseAttch0"
testAttch1 = "baseAttch1"

testList = ["list"]


class Select_Muscle_Op(bpy.types.Operator):
    bl_idname = "view3d.submit_button"
    bl_label = "Submit Muscle Name"
    bl_description = "Submit Muscle Name"

    def execute(self, context):

        # function to execute
        objName = bpy.context.scene.muscle_Name
        muscleCore.make_empty(objName)
        myoGenerator_panel.parentMuscleGenerated = True

        return{'FINISHED'}


class AllowAttach_Op(bpy.types.Operator):
    bl_idname = "view3d.attch"
    bl_label = "Test"

    def execute(self, context):

        global isSubmittingOrigin
        isSubmittingOrigin = not isSubmittingOrigin
        # deselecting all, selecting picked obj
        bpy.ops.object.select_all(action='DESELECT')

        ob = bpy.context.scene.origin_object if isSubmittingOrigin else bpy.context.scene.insertion_object
        bpy.context.view_layer.objects.active = ob   # Make the cube the active object
        ob.select_set(True)
        myoGenerator_panel.allowAttachmentSelection = True
        muscleCore.set_edit_mode()
        return{'FINISHED'}


class Select_Origin_Op(bpy.types.Operator):
    bl_idname = "view3d.select_origin"
    bl_label = "Select Origin"

    def execute(self, context):

        myoGenerator_panel.originSubmitted = True
        muscleCore.create_attachment(0, bpy.context.scene.muscle_Name)
        return{'FINISHED'}


class Select_Insertion_Op(bpy.types.Operator):
    bl_idname = "view3d.select_insertion"
    bl_label = "Select Insertion"

    def execute(self, context):

        myoGenerator_panel.insertionSubmitted = True
        muscleCore.create_attachment(1, bpy.context.scene.muscle_Name)
        bpy.ops.object.mode_set(mode='OBJECT')
        return{'FINISHED'}


class Muscle_Creation_Op(bpy.types.Operator):
    bl_idname = "view3d.muscle_creation"
    bl_label = "Muscle Creation"

    def execute(self, context):
        print("ALL OK")
        myoGenerator_panel.vertexCountMatched = True
        vertex_Counter.OverallVertexCount()
        return{'FINISHED'}


class Curve_Creator_Op(bpy.types.Operator):

    bl_idname = "view3d.curve_creator"
    bl_label = "Curve Creator"

    def execute(self, context):

        from AddonFolder import globalVariables
        print("FINAL OVERALL TEST", globalVariables.attachment_normals)
        originNormal = globalVariables.attachment_normals[0]
        attachNormal = globalVariables.attachment_normals[1]
        print(
            globalVariables.attachment_centroids[0],
            globalVariables.attachment_centroids[1],
            originNormal,
            attachNormal)
        muscleCore.curve_creator(
            globalVariables.attachment_centroids, [
                originNormal, attachNormal], muscleCore.muscleName)
        myoGenerator_panel.curveCreated = True
        return {'FINISHED'}


class Join_Muscle_Op(bpy.types.Operator):
    bl_idname = "view3d.join_muscle"
    bl_label = "Join Muscle"

    def execute(self, context):

        print(bpy.context.scene.muscle_Name, "JOINMUSCLE")
        muscleCore.join_muscle(bpy.context.scene.muscle_Name)

        return{"FINISHED"}


class Transform_To_Mesh_Op(bpy.types.Operator):
    bl_idname = "view3d.convert_to_mesh"
    bl_label = "Convert To Mesh"

    def execute(self, context):

        from AddonFolder import globalVariables

        globalVariables.csvDir = os.path.join(
            context.scene.conf_path,
            (context.scene.file_name + ".csv"))

        muscleCore.get_length()  # ASSIGN NURBS LENGTH TO DICTIONARY
        muscleCore.Transform_to_Mesh(bpy.context.scene.muscle_Name)
        myoGenerator_panel.curveToMesh = True
        return{"FINISHED"}


def SetAttach(index, thisValue):

    print(thisValue, "VALUEPASSED")

    global testAttch1
    global testAttch0

    if(index == 1):
        testAttch0 = thisValue

    else:
        testAttch1 = thisValue



class SetBevel_Op(bpy.types.Operator):
    bl_idname = "view3d.set_bevel"
    bl_label = "SetBevel"

    def execute(self, context):

        muscleCore.bpy.context.object.data.bevel_factor_start = bpy.context.scene.bevel


class SetBevel2_Op(bpy.types.Operator):
    bl_idname = "view3d.set_bevel2"
    bl_label = "SetBevel"

    def execute(self, context):

        muscleCore.bpy.context.object.data.bevel_factor_end = bpy.context.scene.bevel2
        # return {'FINISHED'}


class SetTilt_Op(bpy.types.Operator):
    bl_idname = "view3d.set_tilt"
    bl_label = "SetTilt"

    def execute(self, context):

        if(not bpy.context.active_object.mode == 'EDIT'):
            bpy.ops.object.editmode_toggle()

        bpy.ops.curve.select_all(action='SELECT')
        tilt = bpy.context.scene.tilt * 0.0174533

        bpy.ops.curve.tilt_clear()
        bpy.ops.transform.tilt(value=tilt)



class Calculate_Volume_Op(bpy.types.Operator):
    bl_idname = "view3d.calculate_volume"
    bl_label = "CalculateVolume"

    def execute(self, context):

        muscleCore.updateVolumes()
        return {'FINISHED'}



class Mirror_Cross_Section_Op(bpy.types.Operator):
    bl_idname = "view3d.mirror_cross_section"
    bl_label = "MirrorCrossSection"

    def execute(self, context):
        from AddonFolder import globalVariables
        muscleCore.mirror_bevel(globalVariables.muscleName)
        return {'FINISHED'}


class Reset_Variables_Op(bpy.types.Operator):
    bl_idname = "view3d.reset_variables"
    bl_label = "ResetVariables"

    def execute(self, context):

        from AddonFolder import globalVariables

        globalVariables.muscleName = ''
        globalVariables.attachment_centroids = [0, 0]
        globalVariables.attachment_normals = [0, 0]
        globalVariables.allMuscleParameters.clear()

        bpy.context.scene.muscle_Name = "Insert muscle name"
        bpy.context.scene.origin_object = None
        bpy.context.scene.insertion_object = None
        bpy.context.scene.tilt = 0
        bpy.context.scene.bevel = 0
        bpy.context.scene.bevel2 = 0

        myoGenerator_panel.parentMuscleGenerated = False
        myoGenerator_panel.originSubmitted = False
        myoGenerator_panel.insertionSubmitted = False
        myoGenerator_panel.vertexCountMatched = False
        myoGenerator_panel.curveCreated = False
        myoGenerator_panel.curveToMesh = False

        return {'FINISHED'}
