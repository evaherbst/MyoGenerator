# # -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 12:47:46 2021

@author: evach
this script enables generation of muscle empties. 
These can then be used as parents for muscle origins and insertions, 
to run the Niva_Muscle_Analyzer script
"""
from AddonFolder import test_op
import bpy
import mathutils
from mathutils import Vector, Matrix
import math
import bmesh
import csv
from operator import itemgetter, truediv

# from AddonFolder import globalVariables
from AddonFolder.test_op import testAttch0,testAttch1




origin_centroid = mathutils.Vector()
insertion_centroid = mathutils.Vector()
origin_normal = mathutils.Vector()
insertion_normal = mathutils.Vector()

origin_centroid=0
origin_normal=0
insertion_centroid=0
insertion_normal=0

# attachment_centroids=[0,0]
# attachment_normals=[0,0]

muscleName=''



def make_empty(Muscle):

    from AddonFolder import globalVariables

    global muscleName
    globalVariables.muscleName=Muscle
    muscleName = Muscle

    globalVariables.allMuscleParameters[muscleName]=[0,0,0,0,0,0,0] #assigning to dict()



    bpy.ops.object.mode_set(mode = 'OBJECT')
    o = bpy.data.objects.new(Muscle, None)
    o.empty_display_size = 2
    o.empty_display_type = 'PLAIN_AXES'
    # Set target collection to a known collection 
    coll_target = bpy.context.scene.collection.children.get("Collection")
    # If target found and object list not empty
    for coll in o.users_collection:
        # Unlink the object
        coll.objects.unlink(o)
    # Link each object to the target collection
    coll_target.objects.link(o)





def create_attachment(index,Muscle): #function creates attachment as new object,parents to muscle empty, also contains functions to recenter object, get origin_centroid, create boundary, and calculate origin_normal
# keep track of objects in scene to later rename new objects (#can't just rename active object bc duplicated object doesn't automatically become active)

    from AddonFolder import globalVariables


    # global attachment_centroids
    # global attachment_normals
  

     

    attachmentNames = [' origin', ' insertion']
    attachmentName = attachmentNames[index]
    scn = bpy.context.scene
    names = [ obj.name for obj in scn.objects]
    #select faces, duplicate, separate
    bpy.ops.mesh.duplicate()
    bpy.ops.mesh.separate(type='LOOSE')
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
    bpy.data.objects[Muscle].select_set(False) #make sure only origin is selected  #DOUBLE CHECK
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + attachmentName]
    obj = bpy.context.view_layer.objects.active
    object_Recenter(obj)
    norm = get_normal(obj)
    globalVariables.attachment_normals[index]=norm
    bpy.ops.object.mode_set(mode = 'OBJECT')
    att=calculate_centroid(obj)
    globalVariables.attachment_centroids[index]=att
    boundary = create_boundary(obj)


    area = get_attachment_area(obj)
    
    if(index ==0):
        centroidIdx=2
        areaIdx=0
    else:
        centroidIdx=3
        areaIdx=1


    #Store the centroid values int the dictionary. 
    globalVariables.allMuscleParameters[globalVariables.muscleName][centroidIdx]=att
    globalVariables.allMuscleParameters[globalVariables.muscleName][areaIdx]=area

    if(index == 1): #calculate linear length only once both centroids are calculated
        a = globalVariables.allMuscleParameters[globalVariables.muscleName][2]
        b = globalVariables.allMuscleParameters[globalVariables.muscleName][3]
        linearLength = math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2) 
        globalVariables.allMuscleParameters[globalVariables.muscleName][4]=linearLength
        print("a = ",a)
        print("b = ",b)
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all( action = 'DESELECT' )



#calculate muscle attachment 
def get_attachment_area(obj):
    
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)  #set scale = 1 to get correct area values
    objName=obj.name 
    me = obj.data
    me.name=objName
    # Get a BMesh representation
    bm = bmesh.new()# create an empty BMesh
    bm.from_mesh(me)# fill it in from a Mesh
    area = sum(f.calc_area() for f in bm.faces)
    print("area = " + str(area))
    return area


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
    bpy.context.view_layer.objects.active = bpy.data.objects[name]
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    #select outer loop, duplicate, separate
    bpy.ops.mesh.region_to_loop()
    bpy.ops.mesh.duplicate()
    bpy.ops.mesh.separate(type='LOOSE')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all(action='DESELECT') 
    #for item in scn.objects:
        #if obj.name in names:
           # print("skip")
        #else:
            #print(obj.name + " is new")
    new_objs = [ obj for obj in scn.objects if not obj.name in names]#
    #rename new object and select and make active
    for item in new_objs:
            print(item.name + " is a new item")
            item.name = name + " boundary"
            item.data.name = item.name #set mesh name to object name
            item.select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects[name]
            bpy.data.objects[name].select_set(True)
            bpy.ops.object.parent_set(keep_transform=True) #parents new loop to the attachment area 
            bpy.ops.object.select_all(action='DESELECT') 
            bpy.context.view_layer.objects.active = bpy.data.objects[name + " boundary"]
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.context.tool_settings.mesh_select_mode = (False, False, True)
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.delete(type='ONLY_FACE')
            boundary = bpy.context.view_layer.objects.active
    bpy.ops.object.mode_set(mode = 'OBJECT')
    return boundary

def get_normal(obj):
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.context.tool_settings.mesh_select_mode = (False, False, True)
    bpy.ops.mesh.select_all(action='SELECT')
    bm = bmesh.from_edit_mesh( obj.data )
    # Reference selected face indices
    bm.faces.ensure_lookup_table()
    selFaces = [ f.index for f in bm.faces if f.select ]
    # Calculate the average normal vector
    avgNormal = Vector()
    for i in selFaces: avgNormal += bm.faces[i].normal
    avgNormal = avgNormal / len( selFaces )
    normal = avgNormal
    
    return normal


def calculate_centroid(obj):
    centroid=obj.location
    return centroid

#endregion

#endregion
def curve_creator(attachment_centroids,attachment_normals,Muscle): #need muscle name as input
    
    global origin_centroid
    global insertion_centroid
    global origin_normal
    global insertion_normal
    origin_centroid = attachment_centroids[0]
    insertion_centroid = attachment_centroids[1]
    origin_normal = attachment_normals[0]
    insertion_normal = attachment_normals[1]
    lineLength=math.sqrt((insertion_centroid[0] - origin_centroid[0]) ** 2 + (insertion_centroid[1] - origin_centroid[1]) ** 2 + (insertion_centroid[2] - origin_centroid[2]) ** 2)
    scaleFactor = .1*(lineLength) #decide on scale factor!
    origin_normal = Vector(origin_normal)
    origin_normal_unit = origin_normal/origin_normal.length
    insertion_normal = Vector(insertion_normal)
    insertion_normal_unit = insertion_normal/insertion_normal.length
    bpy.ops.curve.primitive_nurbs_path_add(radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1)) #makes nurbs path with 5 points 
    curve = bpy.context.view_layer.objects.active
    curve.name = Muscle + " curve"
    spline = bpy.data.objects[curve.name].data.splines[0]
    point1 = origin_centroid + (origin_normal_unit*scaleFactor) #
    point3 = insertion_centroid + (insertion_normal_unit*scaleFactor)
    point2 = (point1[0]+point3[0])/2,(point1[1]+point3[1])/2,(point1[2]+point3[2])/2
    spline.points[0].co = [origin_centroid[0],origin_centroid[1],origin_centroid[2],1] #convert vector to tuple, 4th number is nurbs weight, currently set to =1
    spline.points[1].co = [point1[0],point1[1],point1[2],1]
    spline.points[2].co = [point2[0],point2[1],point2[2],1]
    spline.points[3].co = [point3[0],point3[1],point3[2],1]
    spline.points[4].co = [insertion_centroid[0],insertion_centroid[1],insertion_centroid[2],1]
    # add two more points for more refined control 
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.curve.select_all(action='DESELECT')
    curve.data.splines.active.points[1].select = True
    curve.data.splines.active.points[2].select = True
    bpy.ops.curve.subdivide()
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.curve.select_all(action='DESELECT') #note this changes the numbers so now need to select 3 and 4
    curve.data.splines.active.points[3].select = True
    curve.data.splines.active.points[4].select = True 
    bpy.ops.curve.subdivide()

    #now create cross section for muscle from muscle origin

    bpy.ops.object.editmode_toggle() #somehow mode_set (mode = 'OBJECT') did not work but this worked
    bpy.ops.object.select_all(action='DESELECT')
    # select origin boundary loop for that particular muscle
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " origin" + " boundary"] #make active 
    bpy.data.objects[Muscle + " origin" + " boundary"].select_set(True)
    bpy.ops.object.duplicate()
    #duplicated objects now becomes selected and active
    #rename and unparent
    
    cross_section = bpy.context.view_layer.objects.active
    cross_section.name = Muscle + " cross section template"
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')


    align_with_XY(Muscle) #take cross section and move main dimension to XY plane, so that projection on curve is correct, also converts to curve
    #Bevel nurbs path with origin boundary curve
    bpy.ops.object.mode_set(mode = 'OBJECT')   ##NICO ADD
    bpy.ops.object.select_all(action='DESELECT')

    cross_section = bpy.context.view_layer.objects.active
    bpy.ops.object.origin_set( type = 'ORIGIN_GEOMETRY' )
    bpy.data.objects[Muscle + " cross section template"].select_set(True)
    bpy.ops.object.convert(target='CURVE')

    bpy.ops.object.mode_set(mode = 'OBJECT')   ##NICO ADD
    bpy.ops.object.select_all(action='DESELECT')

    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " curve"] #make curve active
    bpy.data.objects[Muscle + " cross section template"].select_set(True)
    #bevel
    bpy.context.object.data.bevel_mode = 'OBJECT'
    bpy.context.object.data.bevel_object = bpy.data.objects[cross_section.name] 
    bpy.context.object.data.bevel_factor_start = 0  #user can adjust this in add-on
    bpy.context.object.data.bevel_factor_end = 1
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " cross section template"] #make curve active
    bpy.data.objects[Muscle + " cross section template"].select_set(True)
    bpy.ops.object.hide_view_set(unselected=False) #hide cross section template
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " curve"] #make curve active



def align_with_XY(Muscle):
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " cross section template"] #make active 
    bpy.data.objects[Muscle + " cross section template"].select_set(True)
    bpy.data.objects[Muscle + " origin" + " boundary"].select_set(False)
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.context.tool_settings.mesh_select_mode = (False, True, False)   # edge selection mode
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.edge_face_add() #add face   
    bpy.context.tool_settings.mesh_select_mode = (False, False, True) # face selection mode
    bpy.ops.mesh.select_all(action='SELECT')
    me = bpy.context.edit_object.data
    #get bmesh (Object needs to be in Edit mode)
    bm=bmesh.from_edit_mesh(me)
    if hasattr(bm.faces,"ensure_lookup_table"):
        bm.faces.ensure_lookup_table()
    bm.select_history.add(bm.faces[0])
    context = bpy.context
    ob = context.edit_object
    me = ob.data
    bm = bmesh.from_edit_mesh(me)
    face = bm.select_history.active
    o = face.calc_center_median()
    face.normal_update()
    edges = sorted((e for e in face.edges), key=lambda e: abs((e.verts[1].co - e.verts[0].co).dot(face.normal)))
    e = edges[0]
    T = Matrix.Translation(-o)
    up = Vector((0, 0, 1))
    R = face.normal.rotation_difference(up).to_matrix()
    bmesh.ops.transform(bm, verts=bm.verts, matrix=R, space=T)
    forward = Vector((0, 1, 0))
    R = (e.verts[1].co - e.verts[0].co).rotation_difference(forward).to_matrix()
    bmesh.ops.transform(bm, verts=bm.verts, matrix=R, space=T)
    T = Matrix.Translation(face.calc_center_median() - o)
    bmesh.ops.transform(bm, verts=bm.verts, matrix=T)
    bmesh.update_edit_mesh(me)





# def Transform_to_Mesh(Muscle):

#     bpy.ops.object.mode_set(mode = 'OBJECT')
#     bpy.ops.object.select_all(action='DESELECT')
#     bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " curve"]
#     bpy.data.objects[Muscle + " curve"].select_set(True)

#     bpy.ops.object.convert(target="MESH")



def Transform_to_Mesh(Muscle):

    try:
        bpy.ops.object.mode_set(mode='OBJECT')
    except:
        pass
    bpy.ops.object.select_all(action='DESELECT')

    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " curve"]
    bpy.data.objects[Muscle + " curve"].select_set(True)
    bpy.ops.object.convert(target="MESH")


##### NRE JOIN



def duplicate_boundaries(Muscle):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " origin" + " boundary"] #make active 
    bpy.data.objects[Muscle + " origin" + " boundary"].select_set(True)
    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(True, True, True), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
    bpy.context.view_layer.objects.active.name = str(Muscle + " origin_merge_with_volume")
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " insertion" + " boundary"] #make active 
    bpy.data.objects[Muscle + " insertion" + " boundary"].select_set(True)
    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(True, True, True), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
    bpy.context.view_layer.objects.active.name = str(Muscle + " insertion_merge_with_volume")
    bpy.data.objects[Muscle + " insertion_merge_with_volume"].select_set(True)
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
    #select items to join
    bpy.ops.object.select_all(action='DESELECT')

def duplicate_attachment_areas(Muscle):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " origin"] #make active 
    bpy.data.objects[Muscle + " origin"].select_set(True)
    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(True, True, True), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
    bpy.context.view_layer.objects.active.name = str(Muscle + " origin_area_merge_with_volume")
    bpy.data.objects[Muscle + " origin_area_merge_with_volume"].select_set(True)
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " insertion"] #make active 
    bpy.data.objects[Muscle + " insertion"].select_set(True)
    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(True, True, True), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
    bpy.context.view_layer.objects.active.name = str(Muscle + " insertion_area_merge_with_volume")
    bpy.data.objects[Muscle + " insertion_area_merge_with_volume"].select_set(True)
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
    #select items to join
    bpy.ops.object.select_all(action='DESELECT')


def get_volume_perimeter(Muscle, index, n,both_ends):     
    #vertices_loop = []
    boundaryNames = [' origin_merge_with_volume',
                     ' insertion_merge_with_volume']

    vertexGroupId=['_origin','_insertion']

    boundaryName = boundaryNames[index]
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    # make active
    # bpy.data.objects[Muscle + " curve"].select_set(False)
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + boundaryName]
    bpy.data.objects[Muscle + boundaryName].select_set(True)

    boundary = bpy.context.view_layer.objects.active
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS') #set object origin to geometry
    loc = boundary.location
   
    print("boundary center" + str(loc))


    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " curve"]
    bpy.data.objects[Muscle + " curve"].select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.context.tool_settings.mesh_select_mode = (
        True, False, False)  # vertex select mode
    bpy.ops.mesh.select_all(action='DESELECT')
    #find points on curve that are closest to boundary loop


    for point in both_ends:
        co = point[1]           #point = [ind,vector,dist]
        print("coordinate is " + str(co))
        distance = math.sqrt(
            (co[0] - loc[0]) ** 2 + (co[1] - loc[1]) ** 2 + (co[2] - loc[2]) ** 2)

        point.append(distance)
        print(point)


    distance_list_ascending = sorted((both_ends), key=itemgetter(2)) #rank distances between points and cursor
    shortest_n= distance_list_ascending[0:n]
    vertices_loop = [item[0] for item in shortest_n] #gets correct vertices on muscle curve, closest to origin
    print("vertices loop for bridging:" + str(vertices_loop))
    #select ends of curve mesh that need to be bridged, assign to vertex group
    bpy.context.active_object.vertex_groups.new(name='CURVE_VERTS'+vertexGroupId[index])
    obj = bpy.context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    vertices= [e for e in bm.verts]

    for i in vertices_loop: 
        vertices[i].select=True


    bpy.ops.object.vertex_group_set_active(group='CURVE_VERTS'+vertexGroupId[index])
    bpy.ops.object.vertex_group_assign()

    #make boundary active to identify and select vertices that need to be bridged
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.data.objects[Muscle + boundaryName].select_set(True) 
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + boundaryName]
    bpy.data.objects[Muscle + " curve"].select_set(False)

    bpy.ops.object.mode_set(mode='EDIT')
    obj = bpy.context.edit_object
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.context.tool_settings.mesh_select_mode = (
    True, False, False)  # vertex select mode required to add groups
    bpy.ops.mesh.select_all()  # select vertices in boundary loop
    bpy.context.active_object.vertex_groups.new(name='BOUNDARY_VERTS'+vertexGroupId[index])
    #print the boundary loop coords here
    loop = []
    obj = bpy.context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    for v in bm.verts:
        if v.select:
            loop.append([v.index, v.co])  
    print("loop " + str(loop))
    bpy.ops.object.vertex_group_assign()
    bpy.ops.object.mode_set(mode='OBJECT')
    #bpy.data.objects[Muscle + boundaryName].select_set(True) 
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " curve"]
    bpy.data.objects[Muscle + " curve"].select_set(True)
    bpy.ops.object.join()
    bpy.ops.object.mode_set(mode='EDIT')
    #select vertex group (merged from 2 original objects)
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.vertex_group_set_active(group='CURVE_VERTS'+vertexGroupId[index])
    bpy.ops.object.vertex_group_select()
    bpy.ops.object.vertex_group_set_active(group='BOUNDARY_VERTS'+vertexGroupId[index])
    bpy.ops.object.vertex_group_select()


# bridge edge loops
    bpy.ops.mesh.bridge_edge_loops()
    bpy.ops.mesh.select_all(action='DESELECT')



def join_muscle(Muscle):
    boundaryNames = [' origin_merge_with_volume',
                     ' insertion_merge_with_volume']

    vertexGroupId=['_origin','_insertion']
    duplicate_boundaries(Muscle)
    
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')

    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + boundaryNames[0]]
    bpy.data.objects[Muscle + boundaryNames[0]].select_set(True)

    #get center of origin loop
    boundary = bpy.context.view_layer.objects.active
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS') #set object origin to geometry
    loc_origin = boundary.location
    print("boundary center" + str(loc_origin))
        
    #scn = bpy.context.scene
    #names = [ obj.name for obj in scn.objects]

    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " curve"]
    bpy.data.objects[Muscle + " curve"].select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.context.tool_settings.mesh_select_mode = (
        True, False, False)  # vertex select mode
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_non_manifold()
    #duplicate
    bpy.ops.mesh.duplicate()
    bpy.ops.mesh.separate(type='LOOSE')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    tube_ends = []
    #new_objs = [ obj for obj in scn.objects if not obj.name in names
    bpy.data.objects[Muscle + " curve"].select_set(False)
    for obj in bpy.context.selected_objects:
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS') #set object origin to geometry
        center = obj.location
        distance_to_origin = math.sqrt(
                (center[0] - loc_origin[0]) ** 2 + (center[1] - loc_origin[1]) ** 2 + (center[2] - loc_origin[2]) ** 2)
        tube_ends.append([obj.name, distance_to_origin])
    print("tube ends list " + str(tube_ends))
    distance_list_ascending = sorted((tube_ends), key=itemgetter(1))
    print("distances list ascending is " + str(distance_list_ascending))
    origin_side = distance_list_ascending[0][0]
    insertion_side = distance_list_ascending[1][0]
    print("origin object is " + str(origin_side))

    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[origin_side].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[origin_side]
    bpy.data.objects[Muscle + boundaryNames[0]].select_set(True)
    bpy.ops.object.join()
    # bridge edge loops
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.bridge_edge_loops()

    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[insertion_side].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[insertion_side]
    bpy.data.objects[Muscle + boundaryNames[1]].select_set(True)
    bpy.ops.object.join()
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.bridge_edge_loops()

    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.data.objects[Muscle + " curve"].select_set(True)
    bpy.data.objects[origin_side].select_set(True)
    bpy.data.objects[insertion_side].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " curve"]
    bpy.ops.object.join()
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles()


    bpy.ops.object.mode_set(mode='OBJECT')
    muscle_volume = bpy.context.view_layer.objects.active
    muscle_volume.name = Muscle + " volume"
    # parent to empty
    muscle_volume.select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle]
    bpy.data.objects[Muscle].select_set(True)
    bpy.ops.object.parent_set(keep_transform=True)
    #deselect empty
    bpy.data.objects[Muscle].select_set(False)
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " volume"]
    # then duplicate origin and insertions (with faces) and merge
    duplicate_attachment_areas(Muscle)
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[str(Muscle + " volume")].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " volume"] #make active
    bpy.data.objects[str(Muscle + " origin_area_merge_with_volume")].select_set(True)
    bpy.data.objects[str(Muscle + " insertion_area_merge_with_volume")].select_set(True)
    bpy.ops.object.join()
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles() #get rid of edge duplicates
    bpy.ops.mesh.normals_make_consistent(inside=False) #recalculate outside normals
    bpy.ops.object.mode_set(mode='OBJECT')





def get_length():

    from AddonFolder import globalVariables

    length=0

    name = globalVariables.muscleName + " curve" 

    try:
        bpy.ops.object.mode_set(mode='OBJECT')
    except:
        pass
    bpy.context.view_layer.objects.active = bpy.data.objects[globalVariables.muscleName + " curve"]
    bpy.data.objects[globalVariables.muscleName + " curve"].select_set(True)
    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(True, True, True), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
    bpy.context.view_layer.objects.active.name = "curve_copy" 
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = bpy.data.objects["curve_copy"]
    bpy.data.objects["curve_copy"].select_set(True)
    bpy.context.object.data.bevel_object = None
    bpy.ops.object.convert(target="MESH")

    obj = bpy.data.objects["curve_copy"]  # particular object by name
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True) #selects obj
    bpy.context.view_layer.objects.active = bpy.data.objects[obj.name] #sets obj as active mesh
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.context.tool_settings.mesh_select_mode = (False, True, False) #edges select mode
    bpy.ops.mesh.select_all(action='DESELECT') #select all edges
    bpy.ops.mesh.select_all(action='SELECT') #select all edges
    me = bpy.context.object.data
    bm = bmesh.from_edit_mesh(me)
    if hasattr(bm.verts,"ensure_lookup_table"):
        bm.edges.ensure_lookup_table()
    for i in bm.edges:
        length+=i.calc_length()
    print(length)


    try:
        bpy.ops.object.mode_set(mode='OBJECT')
    except:
        pass
    bpy.ops.object.delete()
    globalVariables.allMuscleParameters[globalVariables.muscleName][5]=length  
    print(globalVariables.allMuscleParameters[globalVariables.muscleName])




    dir=globalVariables.csvDir       #"C:/Users/evach/Dropbox/Blender Myogenerator and Reconstruction Paper"

    DictionaryExporter(globalVariables.allMuscleParameters, dir)
    
def DictionaryExporter(d, dir):
    import csv
    import os
    directory = dir
    rows = []
    # for key in d:
    #     temp =[]
    #     temp.append(key)
    #     temp = temp + d[key]
    #     # temp.append(d[key])
    #     rows.append(temp)
    print(rows)
    #print(directory)
    # header = ['muscle_name', 'origin_area', 'insertion_area', 'origin_centroid', 'insertion_centroid', 'linear_length', 'muscle_length', 'muscle_volume']
    with open(directory, "a",  newline='') as f:
        
        writer = csv.writer(f)
        
        for key in d:
            row = []
            row.append(key)
            row = row + d[key]
            writer.writerow(row)
          

        # with open(directory, "a",  newline='') as f:
        #     writer = csv.writer(f)
            # writer.writerow(header)

        # #if file exists
        # if os.path.isfile(directory):
        #     writer.writerows(d.items())
        # else:
    



def measure_muscle_volume(obj):
    import bmesh
    bpy.ops.object.transform_apply(location = False, scale = True, rotation = False) #set scale = 1 to get correct volume values
    me = obj.data
    # Get a BMesh representation
    bm = bmesh.new() # create an empty BMesh
    bm.from_mesh(me) # fill it in from a Mesh
    # triangulate prior makes the difference
    bmesh.ops.triangulate(bm, faces=bm.faces)
    print("Volume")
    volume = bm.calc_volume()
    print(volume)
    return volume
    #bm.clear()

#def updateVolumes(path, fileName): #want inputs in final add-on instead of hard coding directory
def updateVolumes():
    from AddonFolder import globalVariables

    try:
        bpy.ops.object.mode_set(mode='OBJECT')
    except:
        pass
    bpy.ops.object.select_all(action='DESELECT')
    #fileNameConv = fileName+'.csv'
    #directory = os.sep.join([path, fileNameConv])
    directory = globalVariables.csvDir
    muscleMetrics= {}
    #Open the file in read mode
    with open(directory, mode='r') as infile:
    #Open a reader to the csv
        reader = csv.reader(infile, delimiter=',') #double check if Add-on produces ; delimited file
    #Read into the dictionary using dictionary comprehension, key is the first column and row are rest of the columns
        for row in reader:
            print(row)
            row[3] = row[3].replace("<Vector (","")
            row[3] = row[3].replace(")>","")
            row[4] = row[4].replace("<Vector (","")
            row[3] = row[3].replace(")>","")
            muscleMetrics[row[0]] = row[1:]#create dictionary where key = muscle name, value = all values
    print("muscle metrics from csv: " + str(muscleMetrics))
    bpy.ops.object.select_all(action='SELECT')
    #now calculate muscle volumes for all volumes in scence
    for obj in bpy.context.selected_objects:
        print(obj)
        if obj.type == 'EMPTY':
            muscleName=obj.name
            print(muscleName)
            children = []
            children = obj.children
            for obj in children:
                if "volume" in obj.name:
                    muscleVolume=measure_muscle_volume(obj)
                    muscleMetrics[muscleName][6]=muscleVolume
                #make dictionary with key = muscleName and value = muscle_volume
            print("updated values: " + str(muscleMetrics))
    header = ['muscle_name', 'origin_area', 'insertion_area', 'origin_centroid', 'insertion_centroid', 'linear_length', 'muscle_length', 'muscle_volume']

    d_new = muscleMetrics

    with open(directory, "w",  newline='') as f:
        writer = csv.writer(f)
        if d_new.get("muscle_name"):
            print("header already written") #header will already exist *if* volumes were already calculated, this checks and only writes if header doesn't exist
        else:
            writer.writerow(header) 
        #writer.writerow(row)
        for key in d_new:
            row = []
            row.append(key)
            row = row + d_new[key]
            writer.writerow(row)

## DEPRECATED
# #join origin and insertion boundaries to muscle volume mesh (duplicate origin and insertion boundaries first so that I can keep boundaries for muscle deconstruction tool)
# #duplicate and unparent




#     #Transform_to_Mesh(Muscle)
#     attachmentName =  str(Muscle + " origin")

#     bpy.ops.object.select_all(action='DESELECT')
#     bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " origin" + " boundary"] #make active 
#     bpy.data.objects[Muscle + " origin" + " boundary"].select_set(True)
#     bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(True, True, True), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
#     bpy.context.view_layer.objects.active.name = str(Muscle + "origin_merge_with_volume")
#     bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
#     bpy.ops.object.select_all(action='DESELECT')
#     bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " insertion" + " boundary"] #make active 
#     bpy.data.objects[Muscle + " insertion" + " boundary"].select_set(True)
#     bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(True, True, True), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
#     bpy.context.view_layer.objects.active.name = str(Muscle + "insertion_merge_with_volume")
#     bpy.data.objects[Muscle + "insertion_merge_with_volume"].select_set(True)
#     bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
#     #select items to join
#     bpy.ops.object.select_all(action='DESELECT')
#     bpy.data.objects[str(Muscle + " curve")].select_set(True)
#     bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " curve"] #make active 
#     bpy.data.objects[str(Muscle + "origin_merge_with_volume")].select_set(True)
#     bpy.data.objects[str(Muscle + "insertion_merge_with_volume")].select_set(True)
#     bpy.ops.object.join()
#     muscle_volume = bpy.context.view_layer.objects.active
#     muscle_volume.name = Muscle + " volume"
#     #parent to empty
#     #muscle_volume.selected=True
#     muscle_volume.select_set(state=True)
#     bpy.context.view_layer.objects.active = bpy.data.objects[Muscle]  
#     bpy.data.objects[Muscle].select_set(True)
#     bpy.ops.object.parent_set(keep_transform=True)
#     bpy.data.objects[Muscle].select_set(False) #make sure only origin is selected
#     bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " volume"]
#     #go to edit mode
#     bpy.ops.object.editmode_toggle()
#     bpy.context.tool_settings.mesh_select_mode = (True, False, False) #vertex select mode
#     #select edge loops
#     bpy.ops.mesh.select_all(action='SELECT')
#     bpy.ops.mesh.region_to_loop() #selects edge loops of muscle mesh, saves
#     obj = bpy.context.edit_object
#     me = obj.data
#     # Get a BMesh representation
#     bm = bmesh.from_edit_mesh(me)
#     edge_Vertices = []
#     for v in bm.verts:
#         if v.select:
#             edge_Vertices.append(v.index)
#     bpy.context.tool_settings.mesh_select_mode = (False, True, False) #edge select mode required for select_loose to work #throws errpr
#     bpy.ops.mesh.select_loose() #select origin and attachment boundary loops
#     bpy.context.tool_settings.mesh_select_mode = (True, False, False) #vertex select mode
#     for v in bm.verts:
#         if v.select:
#             edge_Vertices.append(v.index)
#     bpy.ops.object.mode_set(mode = 'OBJECT') #now use this list to select all boundary loops that need to be bridged
#     for i in edge_Vertices:
#         obj.data.vertices[i].select = True
#     bpy.ops.object.mode_set(mode = 'EDIT')
#     #bridge edge loops
#     bpy.ops.mesh.bridge_edge_loops()
#     # cap ends
#     bpy.ops.mesh.region_to_loop()
#     #triangulate mesh
#     bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
