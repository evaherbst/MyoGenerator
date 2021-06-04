

"""export data with NivaMuscleAnalyzer or variation thereof"""


"""
Method to create muscle empties as parents. Then origin and insertion must be parented to them to run NivaMuscleAnalyzer- not sure yet if this is the best 
way to get all the muscle data or whether to just save as we go along for each muscle"""

import bpy
import mathutils
from mathutils import Vector
import math
import bmesh



origin_centroid = mathutils.Vector(0)
insertion_centroid = mathutils.Vector(0)
origin_normal = mathutils.Vector(0)
insertion_normal = mathutils.Vector(0)


attachments_centroids = [0,0]
attachments_normals=[0,0]

def make_empty(Muscle):
    o = bpy.data.objects.new(Muscle, None)
    bpy.context.scene.collection.objects.link( o )
    o.empty_display_size = 2
    o.empty_display_type = 'PLAIN_AXES'   

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
def get_normal(boundary):
     #fills boundary with face, gets normal, deletes face
    


    bpy.ops.object.select_all( action = 'DESELECT' ) #make sure nothing else in scene is selected
    boundary.select_set(True) #select boundary only
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


def create_attachments(index): #function creates attachment as new object, parents to muscle empty, also contains functions to recenter object, get origin_centroid, create boundary, and calculate origin_normal
    # keep track of objects in scene to later rename new objects (#can't just rename active object bc duplicated object doesn't automatically become active)

    global origin_centroid
    global insertion_centroid
    global origin_normal

    attachMentNames = [' origin', ' insertion']
    attachmentName = attachMentNames[index]

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

    attachments_centroids[index]=calculate_centroid(obj)
    boundary = create_boundary(obj)
    attachments_centroids[index]=get_normal(boundary)
    #origin_normal = get_normal(boundary)




#to be used for each muscle origins
def create_origin_attachment(): #function creates attachment as new object, parents to muscle empty, also contains functions to recenter object, get origin_centroid, create boundary, and calculate origin_normal
    # keep track of objects in scene to later rename new objects (#can't just rename active object bc duplicated object doesn't automatically become active)
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
        obj.name = Muscle + " origin"
        obj.data.name = obj.name #set mesh name to object name
        obj.select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " origin"]
    #Parent to the muscle empty 
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle]   #This works!
    bpy.data.objects[Muscle].select_set(True)
    bpy.ops.object.parent_set(keep_transform=True)
    bpy.data.objects[Muscle].select_set(False) #make sure only origin is selected
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " origin"]
    obj = bpy.context.view_layer.objects.active
    object_Recenter(obj)
    origin_centroid = calculate_centroid(obj)
    boundary = create_boundary(obj)
    origin_normal = get_normal(boundary)


def create_insertion_attachment(): #function creates attachment as new object, parents to muscle empty, also contains functions to recenter object, get insertionb_centroid, create boundary, and get insertion_normal
    # keep track of objects in scene to later rename new objects (#can't just rename active object bc duplicated object doesn't automatically become active)
    scn = bpy.context.scene
    names = [ obj.name for obj in scn.objects]
    #select faces, duplicate, separate
    bpy.ops.mesh.duplicate()
    bpy.ops.mesh.separate(type='SELECTED')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all(action='DESELECT') 
    new_objs = [ obj for obj in scn.objects if not obj.name in names] #sometimes this doesn't work and throws error bpy.context.view_layer.objects.active = bpy.data.objects[Muscle]
    for obj in new_objs:
        obj.name = Muscle + " insertion"
        obj.data.name = obj.name #set mesh name to object name
        obj.select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " insertion"]
    #Parent to the muscle empty 
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle]   #This works!
    bpy.data.objects[Muscle].select_set(True)
    bpy.ops.object.parent_set(keep_transform=True)
    bpy.data.objects[Muscle].select_set(False) #make sure only origin is selected
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " insertion"]
    obj = bpy.context.view_layer.objects.active
    object_Recenter(obj)
    insertion_centroid = calculate_centroid(obj)
    boundary =create_boundary(obj)
    insertion_normal = get_normal(boundary)


def reset_origin(curve):
    offset = origin_centroid - curve.location
    me = curve.data
    for v in me.vertices:
        v.co = v.co - offset
    me.update()
    curve.location = curve.location + offset


def BezierCurve():

    lineLength=math.sqrt((insertion_centroid[0] - origin_centroid[0]) ** 2 + (insertion_centroid[1] - origin_centroid[1]) ** 2 + (insertion_centroid[2] - origin_centroid[2]) ** 2)
    scaleFactor = .2*(lineLength)
    origin_normal_unit = origin_normal/origin_normal.length
    insertion_normal_unit = insertion_normal/insertion_normal.length
    bpy.ops.curve.primitive_bezier_curve_add(radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    #Curve becomes active object after creating so can just name here
    bpy.context.active_object.name = Muscle + " curve"
    curve = bpy.context.active_object
    bez_points = curve.data.splines[0].bezier_points
    bez_points[0].co = origin_centroid
    bez_points[0].handle_left = origin_centroid + (origin_normal_unit*scaleFactor)
    bez_points[0].handle_right = origin_centroid - (origin_normal_unit*scaleFactor)
    bez_points[1].co = insertion_centroid
    bez_points[1].handle_left = insertion_centroid + (insertion_normal_unit*scaleFactor)
    bez_points[1].handle_right = insertion_centroid - (insertion_normal_unit*scaleFactor)
    reset_origin(curve)



"""Main Script step by step to convert to add-on"""



"""User enters muscle name"""

Muscle = "mPSTp" 

bpy.ops.object.mode_set(mode = 'OBJECT')

make_empty(Muscle)

"""ORIGIN CREATION"""


"""prompt user to select bone on which to draw origin - needs to be meshed nicely and if several bones they need to be one object""" 

#user inputs two obj names (makes a list) once once attachment is confirmed, go to nameList[1] (as in next in the list) 


set_edit_mode()


"""prompt user to select origin attachment area""" 

create_origin_attachment() #function creates attachment as new object, parents to muscle empty, also contains functions to recenter object, get origin_centroid, create boundary, and calculate origin_normal





"""INSERTION CREATION"""


"""prompt user to select bone on which to draw insertion - needs to be meshed nicely and if several bones they need to be one object""" 


set_edit_mode()


"""prompt user to select insertion attachment area""" 

create_insertion_attachment() #function creates attachment as new object, parents to muscle empty, also contains functions to recenter object, get insertionb_centroid, create boundary, and get insertion_normal




"""MUSCLE VOLUME CREATION - IN PROGRESS"""


Bezier_curve()

### function vertex counts of origin and insertion here

# create array

#RESET ORIGINS BEFORE USING CURVE MODIFIER:
#Use geometric origin of Bezier curve to the muscle origin attachment centroid, and also set geometric origin of array mesh the muscle origin attachment centroid


# curve modifier function

#then, maybe at end one button that runs NivaMuscleAnalyzer to export data from all muscles in scene? and it can be run separately from rest of GUI