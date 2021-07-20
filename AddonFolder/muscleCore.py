# -*- coding: utf-8 -*-
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

from AddonFolder.test_op import testAttch0,testAttch1


origin_centroid = mathutils.Vector()
insertion_centroid = mathutils.Vector()
origin_normal = mathutils.Vector()
insertion_normal = mathutils.Vector()

origin_centroid=0
origin_normal=0
insertion_centroid=0
insertion_normal=0

attachment_centroids=[0,0]
attachment_normals=[0,0]

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

def create_orig(Muscle): #function creates attachment as new object,parents to muscle empty, also contains functions to recenter object, get origin_centroid, create boundary, and calculate origin_normal
# keep track of objects in scene to later rename new objects (#can't just rename active object bc duplicated object doesn't automatically become active)

    
    #bpy.data.objects[bone].select_set(True)       #MY LINE TO SELECT MUSCLE


   # global attachment_centroids
   # global attachment_normals
   # global attachmentNames

    global origin_centroid
    global origin_normal

    attachmentName = ' origin'
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
    att=calculate_centroid(obj)
    origin_centroid=att
    boundary = create_boundary(obj)
    norm = get_normal(boundary)
    print("NORM VALUE FROM CORE", norm,"BOUNDARY", boundary)
    origin_normal=norm
    
    attachment_centroids.append(origin_centroid)
    attachment_normals.append(origin_normal)
    #FOLLOWING LINES UNSURE
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all( action = 'DESELECT' )

    print("List first Step",attachment_centroids, attachment_normals)

def create_insertion(Muscle): #function creates attachment as new object,parents to muscle empty, also contains functions to recenter object, get origin_centroid, create boundary, and calculate origin_normal
# keep track of objects in scene to later rename new objects (#can't just rename active object bc duplicated object doesn't automatically become active)

    
    #bpy.data.objects[bone].select_set(True)       #MY LINE TO SELECT MUSCLE

    global insertion_centroid
    global insertion_normal

    attachmentName = ' insertion'
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
    att=calculate_centroid(obj)
    insertion_centroid=att
    boundary = create_boundary(obj)
    nnorm = get_normal(boundary)
    print("NORM VALUE FROM CORE", nnorm,"BOUNDARY", boundary)
    insertion_normal=nnorm
    
    attachment_centroids.append(insertion_centroid)
    attachment_normals.append(insertion_normal)
    print(attachment_centroids,attachment_normals,"ALL VAR",origin_normal)
    #FOLLOWING LINES UNSURE
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all( action = 'DESELECT' )








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
    norm = get_normal(obj)
    attachment_normals[index]=norm
    bpy.ops.object.mode_set(mode = 'OBJECT')
    att=calculate_centroid(obj)
    attachment_centroids[index]=att
    boundary = create_boundary(obj)



  
        
    
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
    return str(normal)


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
    spline.points[0].co = [origin_centroid[0],origin_centroid[1],origin_centroid[2],1] #convert vector to tuple, 4th number is nurbs weight, currently set to =1
    spline.points[1].co = [point1[0],point1[1],point1[2],1]
    #point 2 just leave at default position
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
    #now create cross section for muscle from muscle origin
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    # select origin boundary loop for that particular muscle
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " origin" + " boundary"] #make active 
    bpy.data.objects[Muscle + " origin" + " boundary"].select_set(True)
    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(True, True, True), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
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
    bpy.data.objects[Muscle + " cross section template"].select_set(True)
    bpy.ops.object.convert(target='CURVE')

    bpy.ops.object.mode_set(mode = 'OBJECT')   ##NICO ADD
    bpy.ops.object.select_all(action='DESELECT')

    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " curve"] #make curve active
    bpy.data.objects[Muscle + " cross section template"].select_set(True)
    #bevel
    bpy.context.object.data.bevel_mode = 'OBJECT'
    bpy.context.object.data.bevel_object = bpy.data.objects[cross_section.name] 
    bpy.context.object.data.bevel_factor_start = 0.2  #THIS NEEDS TO BE ADJUSTED BY USER SLIDER
    bpy.context.object.data.bevel_factor_end = 0.8


def align_with_XY(Muscle):
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " cross section template"] #make active 
    bpy.data.objects[Muscle + " cross section template"].select_set(True)
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
    normal = bm.faces[0].normal
    bm.select_history.add(bm.faces[0])
    context = bpy.context
    ob = context.edit_object
    me = ob.data
    bm = bmesh.from_edit_mesh(me)
    face = bm.select_history.active
    o = face.calc_center_median()
    face.normal_update()
    norm = face.normal
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





def Transform_to_Mesh(Muscle):

    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " curve"]
    bpy.data.objects[Muscle + " curve"].select_set(True)

    bpy.ops.object.convert(target="MESH")





def join_muscle(Muscle):
#join origin and insertion boundaries to muscle volume mesh (duplicate origin and insertion boundaries first so that I can keep boundaries for muscle deconstruction tool)
#duplicate and unparent


    #Transform_to_Mesh(Muscle)
    attachmentName =  str(Muscle + " origin")

    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " origin" + " boundary"] #make active 
    bpy.data.objects[Muscle + " origin" + " boundary"].select_set(True)
    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(True, True, True), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
    bpy.context.view_layer.objects.active.name = str(Muscle + "origin_merge_with_volume")
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " insertion" + " boundary"] #make active 
    bpy.data.objects[Muscle + " insertion" + " boundary"].select_set(True)
    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(True, True, True), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
    bpy.context.view_layer.objects.active.name = str(Muscle + "insertion_merge_with_volume")
    bpy.data.objects[Muscle + "insertion_merge_with_volume"].select_set(True)
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
    #select items to join
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[str(Muscle + " curve")].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " curve"] #make active 
    bpy.data.objects[str(Muscle + "origin_merge_with_volume")].select_set(True)
    bpy.data.objects[str(Muscle + "insertion_merge_with_volume")].select_set(True)
    bpy.ops.object.join()
    muscle_volume = bpy.context.view_layer.objects.active
    muscle_volume.name = Muscle + " volume"
    #parent to empty
    #muscle_volume.selected=True
    muscle_volume.select_set(state=True)
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle]  
    bpy.data.objects[Muscle].select_set(True)
    bpy.ops.object.parent_set(keep_transform=True)
    bpy.data.objects[Muscle].select_set(False) #make sure only origin is selected
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " volume"]
    #go to edit mode
    bpy.ops.object.editmode_toggle()
    bpy.context.tool_settings.mesh_select_mode = (True, False, False) #vertex select mode
    #select edge loops
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.region_to_loop() #selects edge loops of muscle mesh, saves
    obj = bpy.context.edit_object
    me = obj.data
    # Get a BMesh representation
    bm = bmesh.from_edit_mesh(me)
    edge_Vertices = []
    for v in bm.verts:
        if v.select:
            edge_Vertices.append(v.index)
    bpy.context.tool_settings.mesh_select_mode = (False, True, False) #edge select mode required for select_loose to work #throws errpr
    bpy.ops.mesh.select_loose() #select origin and attachment boundary loops
    bpy.context.tool_settings.mesh_select_mode = (True, False, False) #vertex select mode
    for v in bm.verts:
        if v.select:
            edge_Vertices.append(v.index)
    bpy.ops.object.mode_set(mode = 'OBJECT') #now use this list to select all boundary loops that need to be bridged
    for i in edge_Vertices:
        obj.data.vertices[i].select = True
    bpy.ops.object.mode_set(mode = 'EDIT')
    #bridge edge loops
    bpy.ops.mesh.bridge_edge_loops()
    # cap ends
    bpy.ops.mesh.region_to_loop()
    #triangulate mesh
    bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
