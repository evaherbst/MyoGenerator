

"""export data with NivaMuscleAnalyzer or variation thereof"""


"""
Method to create muscle empties as parents. Then origin and insertion must be parented to them to run NivaMuscleAnalyzer- not sure yet if this is the best 
way to get all the muscle data or whether to just save as we go along for each muscle"""

import bpy

def make_empty(Muscle):
	o = bpy.data.objects.new(Muscle, None)
	bpy.context.scene.collection.objects.link( o )
	o.empty_display_size = 2
	o.empty_display_type = 'PLAIN_AXES'   

def reorder_coords(obj):
#to use for getting origin and insertion vertex numbers the same
    
#Do I need to deselect all here, and then make this object active? or is it enough to just have the obj argument?
#Do I need to make the object active? or is it fine with the input argument? #Test!
	bpy.ops.object.mode_set(mode = 'OBJECT') 
	bpy.ops.object.select_all(action='DESELECT')
	obj.select_set(True) #selects boundary
	bpy.context.view_layer.objects.active = bpy.data.objects[obj.name] #sets boundary as active mesh
	bpy.ops.object.mode_set(mode = 'EDIT')
	bpy.context.tool_settings.mesh_select_mode = (True, False, False) #vertex select mode
	bpy.ops.mesh.select_all(action='SELECT') #select all vertices

	#somehow the above section and the below section run well separately but not if I run them together as one chunk..
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
	    bpy.ops.object.parent_set(keep_transform=True) #parents new loop to the attachment area - need to double check that the transforms are all global 
	    bpy.context.view_layer.objects.active = bpy.data.objects[name + " boundary"]
	return obj


def calculate_centroid(obj):
    centroid=obj.location
    return centroid



def get_normal():
	obj = bpy.context.object
	bpy.ops.object.mode_set(mode = 'EDIT')
	bpy.context.tool_settings.mesh_select_mode = (False, True, False) #edge select mode
	bpy.ops.mesh.select_all(action='SELECT')
	bpy.ops.mesh.edge_face_add() 
	bm = bmesh.from_edit_mesh(obj.data)
	normal = bm.faces[0].normal
	normal = normal[:]
	typetest = type(normal)
	print(normal)
	print(typetest)

	for f in bm.faces:
	    print(f.normal)
	    normal = f.normal
	bpy.ops.mesh.delete(type='ONLY_FACE')
	return normal


def BezierCurve():

import mathutils

lineLength=math.sqrt((insertion_centroid[0] - origin_centroid[0]) ** 2 + (insertion_centroid[1] - origin_centroid[1]) ** 2 + (insertion_centroid[2] - origin_centroid[2]) ** 2)
scaleFactor = .2*(lineLength)

#need to normalize the vectors called "origin_normal" and "insertion_normal"

curve = bpy.ops.curve.primitive_bezier_curve_add(radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
#Curve becomes active object after renaming so can just name here

bpy.context.active_object.name = Muscle + " curve"


curve = bpy.context.active_object
bez_points = curve.data.splines[0].bezier_points
bez_points[0].co = origin_centroid[:]
bez_points[1].co = insertion_centroid[:]
bez_points[0].handle_left = origin_centroid[:] + (origin_normal[0]*scaleFactor, origin_normal[1]*scaleFactor, origin_normal[2]*scaleFactor)
# bez_points[0].handle_right = origin_centroid[:] + origin 
# bez_points[1].handle_left = insertion_centroid[:] + origin
# bez_points[1].handle_right = insertion_centroid[:] + origin


"""Main Script step by step to convert to add-on"""
import bpy
import math
import bmesh

"""ORIGIN CREATION"""

"""user specifies muscle name"""
Muscle = "mPSTp" 

bpy.ops.object.mode_set(mode = 'OBJECT')

make_empty(Muscle)


"""prompt user to select bone on which to draw origin - needs to be meshed nicely and if several bones they need to be one object""" 

"""Need to check if it works if you select two groups of faces that aren't connected, which might happen with attachments that span multiply bones that are not connecte"""
"""I think it should work though! Because it just uses object origin"""



#go to edit mode and face select mode, clear selection
bpy.ops.object.mode_set(mode = 'EDIT')
bpy.context.tool_settings.mesh_select_mode = (False, False, True)
bpy.ops.mesh.select_all(action='DESELECT')


# keep track of objects in scene to later rename new objects (#can't just rename active object bc duplicated object doesn't automatically become active)
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
"""Ideally have user enter a name in the GUI - but for now I just hardcoded it at the beginning"""
for obj in new_objs:
    obj.name = Muscle + " origin"
    obj.data.name = obj.name #set mesh name to object name
    obj.select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " origin"]



#bpy.ops.object.transform_apply(location=True, rotation=True, scale=True) #set transforms to make sure they are in global CS 
#not sure if we want origins at global origin or set

#Parent to the muscle empty
 
bpy.context.view_layer.objects.active = bpy.data.objects[Muscle]   #This works!
bpy.data.objects[Muscle].select_set(True)
bpy.ops.object.parent_set(keep_transform=True)
bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " origin"]


obj = bpy.context.view_layer.objects.active
origin_centroid = calculate_centroid(obj)
origin_normal = get_normal(obj)


#apply transforms again? or fine just with Niva analyzer





"""INSERTION CREATION"""

"""user specifies muscle name"""
Muscle = "mPSTp"


"""prompt user to select bone on which to draw insertion - needs to be meshed nicely and if several bones they need to be one object""" 


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


new_objs = [ obj for obj in scn.objects if not obj.name in names] #sometimes this doesn't work and throws error bpy.context.view_layer.objects.active = bpy.data.objects[Muscle]
bpy.data.objects[Muscle].select_set(True)
bpy.ops.object.parent_set(keep_transform=True)
bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " insertion"]

#rename new object and select and make active
"""Ideally have user enter a name in the GUI - but for now I just hardcoded  it at the beginning"""
for obj in new_objs:
    obj.name = Muscle + " insertion"
    obj.data.name = Muscle + obj.name #set mesh name to object name
    obj.select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " insertion"]

obj = bpy.context.view_layer.objects.active
insertion_centroid = calculate_centroid(obj)
insertion_normal = get_normal(obj)


#bpy.ops.object.transform_apply(location=True, rotation=True, scale=True) #set transforms to make sure they are in global CS - not sure if necessary but just in case 
#not sure if the above is applied to all objects or only selected or active


#Parent to the muscle empty

bpy.context.view_layer.objects.active = bpy.data.objects[Muscle]
bpy.data.objects[Muscle].select_set(True)
bpy.ops.object.parent_set(keep_transform=True)
bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " insertion"]











"""MUSCLE VOLUME CREATION - IN PROGRESS"""


#create boundary for origin and insertion, duplicate, save serapately 
origin = bpy.data.objects[Muscle + " origin"]
insertion = bpy.data.objects[Muscle + " insertion"]
create_boundary(origin)
create_boundary(insertion)

    if "boundary" in obj.name 
        reorder_coords(obj) 

### match vertex counts of origin and insertion here:
#- count vertices in origin and insertion
#calculate how many subdivisions x are needed (x = difference in vertices between 2 objects)
#take object that has less vertice, and select every n pairs of vertices and subdivide (until there are x number of subdivisions performed









#RESET ORIGINS BEFORE USING CURVE MODIFIER:
#Use geometric origin of Bezier curve to the muscle origin attachment centroid, and also set geometric origin of array mesh the muscle origin attachment centroid



