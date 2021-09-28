import bpy
import sys 
import mathutils
from mathutils import Vector
import math
import bmesh
import os


#from . muscleCore import make_muscle_empties
from AddonFolder import muscleCore


#from Muscle_Volume_Sculptor import create_muscle_empties 
from AddonFolder import test_panel
from AddonFolder import vertex_Counter
#from AddonFolder import curve_creator
# from AddonFolder import globalVariables


isSubmittingOrigin = False


testAttch0="baseAttch0"
testAttch1="baseAttch1"

testList=["list"]

class Nico_Select_Muscle_Op(bpy.types.Operator):
    bl_idname = "view3d.submit_button"
    bl_label = "Nico Test Operator"
    bl_description = "Centre Cursor Test"

    def execute(self,context):


        #function to execute
        objName = bpy.context.scene.muscle_Name
        muscleCore.make_empty(objName)
       # make_muscle_empties()

        test_panel.parentMuscleGenerated = True

        print('executing function test')
      
        return{'FINISHED'}


class Nico_AllowAttach_Op(bpy.types.Operator):
    bl_idname="view3d.attch"
    bl_label = "Test"

    
    def execute(self,context):

        #QUITE SKETCHY!
        global isSubmittingOrigin
        isSubmittingOrigin= not isSubmittingOrigin
        #deselecting all, selecting picked obk
        bpy.ops.object.select_all(action='DESELECT') 
       
        ob=bpy.context.scene.origin_object if isSubmittingOrigin else bpy.context.scene.insertion_object
        bpy.context.view_layer.objects.active = ob   # Make the cube the active object 
        ob.select_set(True)
        
        #bpy.data.objects[bpy.context.scene.origin_object.name].select_set(True)   

        test_panel.allowAttachmentSelection=True
        muscleCore.set_edit_mode()
        return{'FINISHED'}

class Nico_Select_Origin_Op(bpy.types.Operator):
    bl_idname = "view3d.select_origin"
    bl_label = "Select Origin"

    def execute(self,context):
        test_panel.originSelected=True

        muscleCore.create_attachment(0,bpy.context.scene.muscle_Name)
       # muscleCore.create_orig(bpy.context.scene.muscle_Name)
        return{'FINISHED'}


class Nico_Select_Insertion_Op(bpy.types.Operator):
    bl_idname = "view3d.select_insertion"
    bl_label = "Select Insertion"

    def execute(self,context):

        muscleCore.create_attachment(1,bpy.context.scene.muscle_Name)
        #muscleCore.create_insertion(bpy.context.scene.muscle_Name)
        bpy.ops.object.mode_set(mode='OBJECT')
        return{'FINISHED'}
        

class Nico_Muscle_Creation_Op(bpy.types.Operator):
    bl_idname="view3d.muscle_creation"
    bl_label="Muscle Creation"

    def execute(self,context):
        print("ALL OK")
        vertex_Counter.OverallVertexCount()
        return{'FINISHED'}


    

class Nico_Curve_Creator_Op(bpy.types.Operator):



    bl_idname="view3d.curve_creator"
    bl_label="Curve Creator"
    def execute(self,context):
        
        from AddonFolder import globalVariables 
        #print(muscleCore.attachment_centroids,muscleCore.attachment_normals,muscleCore.muscleName)
       # print("TEST ATTCH",muscleCore.origin_centroid,muscleCore.origin_normal,muscleCore.insertion_centroid,muscleCore.insertion_normal)
        print("FINAL OVERALL TEST", globalVariables.attachment_normals)
        
        
        #newVector = mathutils.Vector(muscleCore.attachment_normals[0].strip('<Vector ()>')
        # originNormal = mathutils.Vector((float(muscleCore.attachment_normals[0].strip('\'<Vector ()>\'').split(',')[0]),float(muscleCore.attachment_normals[0].strip('\'<Vector ()>\'').split(',')[1]),float(muscleCore.attachment_normals[0].strip('\'<Vector ()>\'').split(',')[2])))
        # attachNormal = mathutils.Vector((float(muscleCore.attachment_normals[1].strip('\'<Vector ()>\'').split(',')[0]),float(muscleCore.attachment_normals[1].strip('\'<Vector ()>\'').split(',')[1]),float(muscleCore.attachment_normals[1].strip('\'<Vector ()>\'').split(',')[2])))
        originNormal = globalVariables.attachment_normals[0]
        attachNormal = globalVariables.attachment_normals[1]
        print(globalVariables.attachment_centroids[0],globalVariables.attachment_centroids[1],originNormal, attachNormal)
       
        #print(mathutils.Vector((4,4,4)))
       
       
        muscleCore.curve_creator(globalVariables.attachment_centroids,[originNormal, attachNormal],muscleCore.muscleName)

        test_panel.curveCreated=True
        #muscleCore.curve_creator(muscleCore.attachment_centroids,[Vector((0.56, 0.7, )),muscleCore.attachment_normals[1]],muscleCore.muscleName)
       
       # curve_creator(muscleCore.attachment_centroids,muscleCore.attachment_normals,muscleCore.muscleName)#PASS HERE ATTACH CENTROIDS,NORMALS,MUSCLE NAME)

       

        return {'FINISHED'}


class Nico_Join_Muscle_Op(bpy.types.Operator):
    bl_idname="view3d.join_muscle"
    bl_label = "Join Muscle"

    def execute(self,context):

        print(bpy.context.scene.muscle_Name, "JOINMUSCLE")
        muscleCore.join_muscle(bpy.context.scene.muscle_Name)
        
        return{"FINISHED"}



class Nico_Transform_To_Mesh_Op(bpy.types.Operator):
    bl_idname="view3d.convert_to_mesh"
    bl_label="Convert To Mesh"

    def execute(self,context):
     
        from AddonFolder import globalVariables 


        globalVariables.csvDir = os.path.join(context.scene.conf_path, (context.scene.file_name+".csv"))
       


        muscleCore.get_length()             #ASSIGN NURBS LENGTH TO DICTIONARY
        muscleCore.Transform_to_Mesh(bpy.context.scene.muscle_Name)
        return{"FINISHED"}


def SetAttach (index, thisValue):

    print(thisValue, "VALUEPASSED")

    global testAttch1
    global testAttch0

    if(index==1):
        testAttch0=thisValue
        print(testAttch0, "FROMWONKY FUN")
    else:
        testAttch1=thisValue
        print(testAttch1,"FROMWONKY FUN")

#     testList.append(thisValue)

class SetBevel_Op(bpy.types.Operator):
    bl_idname = "view3d.set_bevel"
    bl_label="SetBevel"


    def execute(self,context):
   
        print("worked?! ", bpy.context.scene.bevel )
        muscleCore.bpy.context.object.data.bevel_factor_start =  bpy.context.scene.bevel
        # bpy.context.scene.bevel=bpy.props.FloatProperty(update=test)
        
        # props = self.properties
        # self.report({'INFO'}, "The value of the slider: " + str(self.properties))
        #return value that tells blender we finished without failure
        #return {'FINISHED'}

class SetBevel2_Op(bpy.types.Operator):
    bl_idname = "view3d.set_bevel2"
    bl_label="SetBevel"


    def execute(self,context):
   
      
        muscleCore.bpy.context.object.data.bevel_factor_end =  bpy.context.scene.bevel2
        #return {'FINISHED'}



class SetTilt_Op(bpy.types.Operator):
    bl_idname="view3d.set_tilt"
    bl_label="SetTilt"


    
    def execute(self,context):
   

        if(not bpy.context.active_object.mode == 'EDIT'):
            bpy.ops.object.editmode_toggle()


        bpy.ops.curve.select_all(action='SELECT')
        tilt=bpy.context.scene.tilt*0.0174533

        bpy.ops.curve.tilt_clear()
        bpy.ops.transform.tilt(value=tilt)

        return {'FINISHED'}



class Calculate_Volume_Op(bpy.types.Operator):
    bl_idname="view3d.calculate_volume"
    bl_label="CalculateVolume"

    def execute(self,context):

        #ADD HERE THE FUNCTION YOu WANNA CALL

        muscleCore.updateVolumes()
        return {'FINISHED'}
        
            

