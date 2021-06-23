#planning curve creator script

#make 5 points, beg. and end set to origin and insertion centroids, and positions locked
#Use nurbs path (not curve) instead of Bezier curve

#NOTE- make sure centroids are calculated based on centroids of muscle attachment and not of bone - need to test this at end to make sure

import bpy
from mathutils import Vector
import bmesh
import math


#useful functions for tests
def calculate_centroid(obj):
    centroid=obj.location
    return centroid


obj = bpy.context.view_layer.objects.active
origin_centroid = calculate_centroid(obj)

#repeat for insertion
obj = bpy.context.view_layer.objects.active
insertion_centroid = calculate_centroid(obj)

# get normal
boundary = obj = bpy.context.view_layer.objects.active
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
bpy.ops.mesh.delete(type='ONLY_FACE') #doesnt delete
origin_normal = normal

#go back to object mode

# get normal
boundary = obj = bpy.context.view_layer.objects.active
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
insertion_normal = normal




import bpy
from mathutils import Vector
import bmesh
import math

lineLength=math.sqrt((insertion_centroid[0] - origin_centroid[0]) ** 2 + (insertion_centroid[1] - origin_centroid[1]) ** 2 + (insertion_centroid[2] - origin_centroid[2]) ** 2)
scaleFactor = .1*(lineLength) #decide on scale factor!
origin_normal = Vector(origin_normal)
origin_normal_unit = origin_normal/origin_normal.length
insertion_normal = Vector(insertion_normal)
insertion_normal_unit = insertion_normal/insertion_normal.length
bpy.ops.curve.primitive_nurbs_path_add(radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1)) #makes nurbs path with 5 points 
spline = bpy.data.objects["NurbsPath.002"].data.splines[0] #need to change name later


point1 = origin_centroid + (origin_normal_unit*scaleFactor)
point3 = insertion_centroid + (insertion_normal_unit*scaleFactor)
spline.points[0].co = [origin_centroid[0],origin_centroid[1],origin_centroid[2],1] #convert vector to tuple, 4th number is nurbs weight, currently set to =1
spline.points[1].co = [point1[0],point1[1],point1[2],1]
#spline.points[2].co = .. though about setting this to midpoint of origin and insertion but don't want that bc it would mess up curve (e.g. be straight line), so leave default for now
spline.points[3].co = [point3[0],point3[1],point3[2],1]
spline.points[4].co = [insertion_centroid[0],insertion_centroid[1],insertion_centroid[2],1]

# add two more points for more refined control - or do this beforehand?
bpy.ops.object.mode_set(mode = 'EDIT')
bpy.ops.curve.select_all(action='DESELECT')
spline.points[1].select = True
spline.points[2].select = True
bpy.ops.curve.subdivide()
bpy.ops.object.mode_set(mode = 'EDIT')
bpy.ops.curve.select_all(action='DESELECT') #note this changes the numbers so now need to select 3 and 4
spline.points[3].select = True
spline.points[4].select = True 
bpy.ops.curve.subdivide()








#TESTS FOR BEVELING

#get object with "origin" and "boundary" and Muscle in name (to make sure it's only done for that specific muscle)

#duplicate, because converting back will cause a different boundary which we do not want

#rename (when you duplicate and separate the new object does not become active so you need to select it using the other method keeping track of new and old objects)

#convert to curve
bpy.ops.object.convert(target='CURVE')


#then, make nurbs path active

bpy.context.object.data.bevel_mode = 'OBJECT'
bpy.context.object.data.bevel_object = bpy.data.objects["BezierCircle"] #ADD NAME OF ORIGIN BOUNDARY CONVERTED TO CURVE 

#user can adjust curve shape, endpoint tilts etc

#then convert curve to mesh

bpy.ops.object.convert(target='MESH')

#then user can scale some edgeloops etc

#then need to join curve with origin_boundary and insertion_boundary

#select edge loops

#bridge edge loops

# cap ends

#user has option to do boolean ops to get more exact ends

#Things to look into
# - nurbs weight
# - smooth tilt
# - smooth radius
# - adjusting tilt of individual points - especially endpoints - can do manually for now
# - adjusting radius - not ideal, better to do with edge loops after it's converted to a mesh















