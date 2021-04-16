

"""export data with NivaMuscleAnalyzer or variation thereof"""


"""
Method to create muscle empties as parents. Then origin and insertion must be parented to them to run NivaMuscleAnalyzer- not sure yet if this is the best 
way to get all the muscle data or whether to just save as we go along for each muscle"""

import bpy

def make_muscle_empties():
	#enter your list of muscles here
	muscle_List = ["mPT", "mLPt", "mPPt","mPSTs", "mPSTp", "mAMEP", "mAMEM", "mAMES", "mAMP", "mDM"]
	for i in muscle_List:
		print(i)
		o = bpy.data.objects.new(i, None)
		bpy.context.scene.collection.objects.link( o )
		o.empty_display_size = 2
		o.empty_display_type = 'PLAIN_AXES'   
		 

make_muscle_empties()












"""Main Script step by step to convert to add-on"""
import bpy
import math
import bmesh

"""ORIGIN CREATION"""

"""user specifies muscle name"""
Muscle = "mAMES"

"""prompt user to select bone on which to draw origin""" 


#go to edit mode and face select mode, clear selection
bpy.ops.object.mode_set(mode = 'EDIT')
bpy.context.tool_settings.mesh_select_mode = (False, False, True)
bpy.ops.mesh.select_all(action='DESELECT')


# keep track of objects in scene to later rename new objects
scn = bpy.context.scene
names = [ obj.name for obj in scn.objects]


"""prompt user to select origin attachment area""" 

#select faces, duplicate, separate
bpy.ops.mesh.duplicate()
bpy.ops.mesh.separate(type='SELECTED')

bpy.ops.object.mode_set(mode = 'OBJECT')
bpy.ops.object.select_all(action='DESELECT') 


new_objs = [ obj for obj in scn.objects if not obj.name in names]

#rename new object and select and make active
"""Ideally have user enter a name in the GUI - but for now I just hardcoded it as an example"""
for obj in new_objs:
    obj.name = Muscle + " origin"
    obj.data.name = Muscle + " origin"
    obj.select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + "origin"]

bpy.ops.object.transform_apply(location=True, rotation=True, scale=True) #set transforms to make sure they are in global CS - not sure if necessary but just in case 
#not sure if the above is applied to all objects or only selected or active


#Parent to the muscle empty

bpy.context.view_layer.objects.active = bpy.data.objects[Muscle]
bpy.data.objects[Muscle].select_set(True)
bpy.ops.object.parent_set(keep_transform=True)
bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " origin"]


#apply transforms again? or fine just with Niva analyzer





"""INSERTION CREATION"""

"""user specifies muscle name"""
Muscle = "mAMES"


"""prompt user to select bone on which to draw insertion""" 


#go to edit mode and face select mode, clear selection
bpy.ops.object.mode_set(mode = 'EDIT')
bpy.context.tool_settings.mesh_select_mode = (False, False, True)
bpy.ops.mesh.select_all(action='DESELECT')


# keep track of objects in scene to later rename new objects
scn = bpy.context.scene
names = [ obj.name for obj in scn.objects]


"""prompt user to select insertion attachment area""" 

#select faces, duplicate, separate
bpy.ops.mesh.duplicate()
bpy.ops.mesh.separate(type='SELECTED')

bpy.ops.object.mode_set(mode = 'OBJECT')
bpy.ops.object.select_all(action='DESELECT') 


new_objs = [ obj for obj in scn.objects if not obj.name in names]

#rename new object and select and make active
"""Ideally have user enter a name in the GUI - but for now I just hardcoded it as an example"""
for obj in new_objs:
    obj.name = Muscle + " insertion"
    obj.data.name = Muscle + " insertion"
    obj.select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + "insertion"]

bpy.ops.object.transform_apply(location=True, rotation=True, scale=True) #set transforms to make sure they are in global CS - not sure if necessary but just in case 
#not sure if the above is applied to all objects or only selected or active


#Parent to the muscle empty

bpy.context.view_layer.objects.active = bpy.data.objects[Muscle]
bpy.data.objects[Muscle].select_set(True)
bpy.ops.object.parent_set(keep_transform=True)
bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " insertion"]











"""MUSCLE VOLUME CREATION"""


"""add modified tube tool or add shape key method to make muscle volume


if we use tube tool, need to add conver origins and insertions into single face with:
create_boundary script (see exporter_for_MuscleDecomposition) and this:


bpy.ops.object.mode_set(mode = 'EDIT')
bpy.context.tool_settings.mesh_select_mode = (False, True, False) #edge select mode
bpy.ops.mesh.select_all(action='SELECT')

fill edge loop to make 1 face
bpy.ops.mesh.edge_face_add() 

- need to decide if we want to export centroid coords before simplifying to single face
- try to figure out how to calculate curve length for muscle length"""







