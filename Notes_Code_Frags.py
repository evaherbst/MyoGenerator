# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import bpy
import math
import bmesh



#Get ACtive Object
bpy.context.view_layer.objects.active = bpy.data.objects[objName]


#Get Object origin coords (make sure to set origin to geometry first)
obj.location











def reorder_coords():
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.context.tool_settings.mesh_select_mode = (True, False, False) #vertex select mode
    me = bpy.context.object.data
    bm = bmesh.from_edit_mesh(me)
    # index of the start vertex
    initial = bm.verts[0]
    vert = initial
    prev = None
    for i in range(len(bm.verts)):
        print(vert.index, i)
        vert.index = i
        next = None
        adjacent = []
        for v in [e.other_vert(vert) for e in vert.link_edges]:
            if (v != prev and v != initial):
                next = v
        if next == None: break
        prev, vert = vert, next
    bm.verts.sort()
    bmesh.update_edit_mesh(me)
	
	
def export_coords():
    path = 'C:/Users/evach/Dropbox/MuscleTool/test_new_code_coords.txt'
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True) #need to set transforms to make sure they are in global CS
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.context.tool_settings.mesh_select_mode = (True, False, False) #vertex select mode
    obj = bpy.context.object
    file = open(path,'w')
    # Get the active mesh
    obj = bpy.context.edit_object
    me = obj.data
    # Get a BMesh representation
    bm = bmesh.from_edit_mesh(me)
    bm.faces.active = None
    for v in bm.verts:
        if v.select:
            file.write(str(tuple(v.co) )+'\n')
		



"""Main Script step by step to convert to add-on"""
import bpy
import math
import bmesh

"""prompt user to select bone on which to draw attachment sites""" 


#go to edit mode and face select mode, clear selection
bpy.ops.object.mode_set(mode = 'EDIT')
bpy.context.tool_settings.mesh_select_mode = (False, False, True)
bpy.ops.mesh.select_all(action='DESELECT')


# keep track of objects in scene to later rename new objects
scn = bpy.context.scene
names = [ obj.name for obj in scn.objects]


"""prompt user to select origin attachment area""" 

#select outer loop, duplicate, separate
# bpy.ops.mesh.region_to_loop() #omit this if you want to copy all faces - but will still need loop isolated, for generating input for the muscle decomposition tool, 
# so could move this to the reorder_coords fxn, make separate outside loop, reorder and export points, then delete extra loop
bpy.ops.mesh.duplicate()
bpy.ops.mesh.separate(type='SELECTED')

bpy.ops.object.mode_set(mode = 'OBJECT')
bpy.ops.object.select_all(action='DESELECT') 


new_objs = [ obj for obj in scn.objects if not obj.name in names]

#rename new object and select and make active
"""Ideally have user enter a name in the GUI - but for now I just hardcoded it as an example"""
for obj in new_objs:
    obj.name = "AMEM insertion"
    obj.data.name = "AMEM insertion"
    obj.select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects['AMEM insertion']

bpy.ops.object.transform_apply(location=True, rotation=True, scale=True) #set transforms to make sure they are in global CS - not sure if necessary but just in case 
#not sure if the above is applied to all objects or only selected or active


"""reorder vertices in loop and export to file for muscle strand generator (MuscleDecompositionTool) before filling edge loop
"""

reorder_coords()
export_coords()

#now select edges and fill face
bpy.ops.object.mode_set(mode = 'EDIT')
bpy.context.tool_settings.mesh_select_mode = (False, True, False) #edge select mode
bpy.ops.mesh.select_all(action='SELECT')

#fill edge loop to make 1 face
bpy.ops.mesh.edge_face_add()



"""prompt user to select insertion attachment area - repeat same as above"""

"""add modified tube tool or add shape key method to make muscle volume
note if we use shape key, should not make single face but instead save all the faces of the attachment area
could also do that with modifying tube tool so that the centroids are more accurate.."""

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



"""