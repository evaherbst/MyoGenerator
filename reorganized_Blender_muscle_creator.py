

"""export data with NivaMuscleAnalyzer or variation thereof"""


"""
Method to create muscle empties as parents. Then origin and insertion must be parented to them to run NivaMuscleAnalyzer- not sure yet if this is the best 
way to get all the muscle data or whether to just save as we go along for each muscle"""

import bpy
import mathutils
from mathutils import Vector
import math
import bmesh



origin_centroid = mathutils.Vector()
insertion_centroid = mathutils.Vector()
origin_normal = mathutils.Vector()
insertion_normal = mathutils.Vector()
attachment_centroids = [0,0]
attachment_normals = [0,0]

def make_empty(Muscle):
    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    bpy.context.object.name = Muscle
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.context.tool_settings.mesh_select_mode = (False, False, True)
    bpy.ops.mesh.select_all(action='DESELECT')

def set_edit_mode(): #sets edit mode 
    #go to edit mode and face select mode, clear selection
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.context.tool_settings.mesh_select_mode = (False, False, True)
    bpy.ops.mesh.select_all(action='DESELECT')


#to be used for each muscle origins
def object_Recenter(obj): 
# center origin of object on center of mass
    bpy.ops.object.select_all( action = 'DESELECT' ) #make sure nothing else in scene is selected
    obj.select_set(True) #select obj only
    bpy.ops.object.origin_set( type = 'ORIGIN_GEOMETRY' ) #need to set origin to geometry, otherwise all muscles will still have same origin as bone

#to be used for each muscle origins
def calculate_centroid(obj):
    centroid=obj.location
    return centroid

#to be used for each muscle origins
def create_boundary(obj): #this works well - makes boundary, parents to attachment area area
    name = obj.name
    # keep track of objects in scene to later rename new objects
    scn = bpy.context.scene
    names = [ obj.name for obj in scn.objects]
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    #select outer loop, duplicate, separate
    bpy.ops.mesh.region_to_loop()
    bpy.ops.mesh.duplicate()
    bpy.ops.mesh.separate(type='SELECTED')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all(action='DESELECT') 
    new_objs = [ obj for obj in scn.objects if not obj.name in names]
    #rename new object and select and make active
    for obj in new_objs:
        obj.name = name + " boundary"
        obj.data.name = obj.name #set mesh name to object name
        obj.select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects[name]
        bpy.data.objects[name].select_set(True)
        bpy.ops.object.parent_set(keep_transform=True) #parents new loop to the attachment area 
        bpy.context.view_layer.objects.active = bpy.data.objects[name + " boundary"]
        boundary = bpy.context.view_layer.objects.active
    return boundary

#to be used for each muscle origins
def get_normal(boundary):#fills boundary with face, gets normal, deletes face
    bpy.ops.object.select_all( action = 'DESELECT' ) #make sure nothing else in scene is selected
    boundary.select_set(True) #select boundary only
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.context.tool_settings.mesh_select_mode = (False, True, False) #edge select mode
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.edge_face_add() 
    bm = bmesh.from_edit_mesh(boundary.data)
    normal = bm.faces[0].normal
    normal = normal[:]
    typetest = type(normal)
    print(normal)
    for f in bm.faces:
        print(f.normal)
        normal = f.normal
    bpy.ops.mesh.delete(type='ONLY_FACE')
    return normal


def create_attachment(index): #function creates attachment as new object, parents to muscle empty, also contains functions to recenter object, get origin_centroid, create boundary, and calculate origin_normal
# keep track of objects in scene to later rename new objects (#can't just rename active object bc duplicated object doesn't automatically become active)
    global attachment_centroids
    global attachment_normals
    attachmentNames = [' origin', ' insertion']
    attachmentName = attachmentNames[index]
    scn = bpy.context.scene
    names = [ obj.name for obj in scn.objects]
    #select faces, duplicate, separate
    bpy.ops.mesh.duplicate()
    bpy.ops.mesh.separate(type='SELECTED')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all(action='DESELECT') 
    new_objs = [ obj for obj in scn.objects if not obj.name in names] 
    #rename new object and select and make active
    for obj in new_objs:
        obj.name = Muscle + attachmentName
        obj.data.name = obj.name #set mesh name to object name
        obj.select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + attachmentName]
    #Parent to the muscle empty 
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle]   #This works!
    bpy.data.objects[Muscle].select_set(True)
    bpy.ops.object.parent_set(keep_transform=True)
    bpy.data.objects[Muscle].select_set(False) #make sure only origin is selected
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + attachmentName]
    obj = bpy.context.view_layer.objects.active
    object_Recenter(obj)
    attachment_centroids[index]=calculate_centroid(obj)
    boundary = create_boundary(obj)
    attachment_normals[index] = get_normal(boundary)







"""Main Script step by step to convert to add-on"""



"""User enters muscle name"""

Muscle = "mDm" 

bpy.ops.object.mode_set(mode = 'OBJECT')

make_empty(Muscle)

"""ORIGIN CREATION"""


"""prompt user to select bone on which to draw origin - needs to be meshed nicely and if several bones they need to be one object""" 

#user inputs two obj names (makes a list) once once attachment is confirmed, go to nameList[1] (as in next in the list) 


set_edit_mode()


"""prompt user to select origin attachment area""" 


create_attachment(0) #function creates attachment as new object, parents to muscle empty, also contains functions to recenter object, get origin_centroid, create boundary, and calculate origin_normal


"""INSERTION CREATION"""

bpy.ops.object.mode_set(mode = 'OBJECT')
bpy.ops.object.select_all( action = 'DESELECT' )

"""prompt user to select bone on which to draw insertion - needs to be meshed nicely and if several bones they need to be one object""" 


set_edit_mode()


"""prompt user to select insertion attachment area""" 


create_attachment(1) #function creates attachment as new object, parents to muscle empty, also contains functions to recenter object, get insertion_centroid, create boundary, and get insertion_normal


"""MUSCLE VOLUME CREATION - IN PROGRESS"""

change_vertex_number(originCounts,insertionCounts,origin_boundary_obj,insertion_boundary_obj) #see Vertex_Count.py


#curve creator here

#slider for creating extent of bevel - I think this need to be done straight in the add-on but here is some code on defining extent of bevels:



#then, maybe at end one button that runs NivaMuscleAnalyzer to export data from all muscles in scene? and it can be run separately from rest of GUI

#also, *if time and after everything else works*, use NurbsPath_length.py to calculate nirbs path length and store *before* curve is converted to mesh