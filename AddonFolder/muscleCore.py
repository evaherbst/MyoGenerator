# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 12:47:46 2021

@author: evach
this script enables generation of muscle empties. 
These can then be used as parents for muscle origins and insertions, 
to run the Niva_Muscle_Analyzer script
"""
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

attachments_names=[]
muscleName=''


#def make_empty(Muscle):
 #   bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
  #  bpy.context.object.name = Muscle
   # set_edit_mode()

def make_empty(Muscle):
    global muscleName
    muscleName = Muscle
    bpy.ops.object.mode_set(mode = 'OBJECT')
    o = bpy.data.objects.new(Muscle, None)
    bpy.context.scene.collection.objects.link( o )
    o.empty_display_size = 2
    o.empty_display_type = 'PLAIN_AXES'   

	#set_edit_mode()   #go to edit to select faces



def create_attachment(index,Muscle): #function creates attachment as new object,parents to muscle empty, also contains functions to recenter object, get origin_centroid, create boundary, and calculate origin_normal
# keep track of objects in scene to later rename new objects (#can't just rename active object bc duplicated object doesn't automatically become active)

    
    #bpy.data.objects[bone].select_set(True)       #MY LINE TO SELECT MUSCLE


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

    #FOLLOWING LINES UNSURE
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all( action = 'DESELECT' )





#region GENERAL FUNCTIONALITIES: 
def set_edit_mode(): #sets edit mode 
    #go to edit mode and face select mode, clear selection
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.context.tool_settings.mesh_select_mode = (False, False, True)
    bpy.ops.mesh.select_all(action='DESELECT')

#region SPECIFIC FOR create_attachment 
def object_Recenter(obj): 
	# center origin of object on center of mass
    bpy.ops.object.select_all( action = 'DESELECT' ) #make sure nothing else in scene is selected
    obj.select_set(True) #select obj only
    bpy.ops.object.origin_set( type = 'ORIGIN_GEOMETRY' ) #need to set origin to geometry, otherwise all muscles will still have same origin as bone

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

def calculate_centroid(obj):
	centroid=obj.location
	return centroid

#endregion

#endregion
	