import bpy
from mathutils import Vector, Matrix
import math
import bmesh

from AddonFolder import muscleCore


#super ugly...
# origin_centroid = muscleCore.origin_centroid
# insertion_centroid = muscleCore.insertion_centroid
# origin_normal = muscleCore.origin_normal
# insertion_normal = muscleCore.insertion_normal
# attachment_centroids = muscleCore.attachment_centroids
# attachment_normals =muscleCore.attachment_normals
# muscleName=muscleCore.muscleName



def change_vertex_number(originCount,insertionCount,origin_boundary_obj,insertion_boundary_obj):
  print("OriginCount = ", originCount," InsCount =", insertionCount)
  vertexDiff=abs(originCount-insertionCount)
  print ("vert Diff", vertexDiff)
  counter = 0
  print(counter)
  print(type(originCount))
  if (originCount < insertionCount):
    print("ORIGIN < INSERTION")
    increment = math.floor((originCount)/vertexDiff) #rounds down 
    origin_boundary_obj.select_set(True)
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.context.tool_settings.mesh_select_mode = (False, True, False) #edge select mode
    obj = origin_boundary_obj
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    for x in range(0, originCount-1, increment):
      if(counter< vertexDiff):
        counter+=1
        bpy.ops.object.mode_set(mode = 'OBJECT')
        for edge in obj.data.edges:
          edge.select = False
        obj.data.edges[x].select = True
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.subdivide()
        print(counter)
        print("subdivision successful")
  elif (originCount > insertionCount):
    print("ORIGIN > INSERTION")
    increment = math.floor((insertionCount)/vertexDiff) #rounds down to nearest whole number increment
    print(increment)
    insertion_boundary_obj.select_set(True)
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.context.tool_settings.mesh_select_mode = (False, True, False) #edge select mode
    obj = insertion_boundary_obj
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')
    for x in range(0, originCount-1, increment):
      if(counter< vertexDiff):
        counter+=1
        bpy.ops.object.mode_set(mode = 'OBJECT')
        for edge in obj.data.edges:
          edge.select = False
        obj.data.edges[x].select = True
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.subdivide()
        print(counter)
        print("subdivision successful")
  elif (originCount == insertionCount):
    print('wow, that was lucky')

def reorder_coords(obj):
  bpy.ops.object.mode_set(mode = 'OBJECT')
  bpy.ops.object.select_all(action='DESELECT')
  obj.select_set(True) #selects boundary
  bpy.context.view_layer.objects.active = bpy.data.objects[obj.name] #sets boundary as active mesh
  bpy.ops.object.mode_set(mode = 'EDIT')
  bpy.context.tool_settings.mesh_select_mode = (True, False, False) #vertex select mode
  bpy.ops.mesh.select_all(action='SELECT') #select all vertices
  me = bpy.context.object.data
  bm = bmesh.from_edit_mesh(me)
  if hasattr(bm.verts,"ensure_lookup_table"):
      bm.verts.ensure_lookup_table()
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
  return len(bm.verts)


def OverallVertexCount():


  Muscle = muscleCore.muscleName
  bpy.ops.object.mode_set(mode = 'OBJECT')
  bpy.ops.object.select_all(action='DESELECT')
  bpy.ops.object.select_all(action='SELECT')
  print(len(bpy.context.selected_objects))
  for obj in bpy.context.selected_objects:
    if Muscle in obj.name and "boundary" in obj.name:
      print(obj)
      if "origin" in obj.name:
        originCounts = reorder_coords(obj)
        origin_boundary_obj = obj
        print("reordering origin") 
      if "insertion" in obj.name:
        insertionCounts = reorder_coords(obj)
        insertion_boundary_obj = obj
        print("reordering insertion")

  change_vertex_number(originCounts,insertionCounts,origin_boundary_obj,insertion_boundary_obj)

# ################
# def align_with_XY(Muscle):
#     bpy.ops.object.mode_set(mode = 'OBJECT')
#     bpy.ops.object.select_all(action='DESELECT')
#     bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " cross section template"] #make active 
#     bpy.data.objects[Muscle + " cross section template"].select_set(True)
#     bpy.ops.object.mode_set(mode = 'EDIT')
#     bpy.context.tool_settings.mesh_select_mode = (False, True, False)   # edge selection mode
#     bpy.ops.mesh.select_all(action='SELECT')
#     bpy.ops.mesh.edge_face_add() #add face
#     bpy.context.tool_settings.mesh_select_mode = (False, False, True) # face selection mode
#     bpy.ops.mesh.select_all(action='SELECT')
#     me = bpy.context.edit_object.data
#     #get bmesh (Object needs to be in Edit mode)
#     bm=bmesh.from_edit_mesh(me)
#     bm.select_history.add(bm.faces[0])
#     context = bpy.context
#     ob = context.edit_object
#     me = ob.data
#     bm = bmesh.from_edit_mesh(me)
#     face = bm.select_history.active
#     o = face.calc_center_median()
#     face.normal_update()
#     norm = face.normal
#     edges = sorted((e for e in face.edges), key=lambda e: abs((e.verts[1].co - e.verts[0].co).dot(face.normal)))
#     e = edges[0]
#     T = Matrix.Translation(-o)
#     up = Vector((0, 0, 1))
#     R = face.normal.rotation_difference(up).to_matrix()
#     bmesh.ops.transform(bm, verts=bm.verts, matrix=R, space=T)
#     forward = Vector((0, 1, 0))
#     R = (e.verts[1].co - e.verts[0].co).rotation_difference(forward).to_matrix()
#     bmesh.ops.transform(bm, verts=bm.verts, matrix=R, space=T)
#     T = Matrix.Translation(face.calc_center_median() - o)
#     bmesh.ops.transform(bm, verts=bm.verts, matrix=T)
#     bmesh.update_edit_mesh(me)


# def curve_creator(attachment_centroids,attachment_normals,Muscle): #need muscle name as input
#     global origin_centroid
#     global insertion_centroid
#     global origin_normal
#     global insertion_normal
#     origin_centroid = attachment_centroids[0]
#     insertion_centroid = attachment_centroids[1]
#     origin_normal = attachment_normals[0]
#     insertion_normal = attachment_normals[1]
#     lineLength=math.sqrt((insertion_centroid[0] - origin_centroid[0]) ** 2 + (insertion_centroid[1] - origin_centroid[1]) ** 2 + (insertion_centroid[2] - origin_centroid[2]) ** 2)
#     scaleFactor = .1*(lineLength) #decide on scale factor!
#     origin_normal = Vector(origin_normal)
#     origin_normal_unit = origin_normal/origin_normal.length
#     insertion_normal = Vector(insertion_normal)
#     insertion_normal_unit = insertion_normal/insertion_normal.length
#     bpy.ops.curve.primitive_nurbs_path_add(radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1)) #makes nurbs path with 5 points 
#     curve = bpy.context.view_layer.objects.active
#     curve.name = Muscle + " curve"
#     spline = bpy.data.objects[curve.name].data.splines[0]
#     point1 = origin_centroid + (origin_normal_unit*scaleFactor) #
#     point3 = insertion_centroid + (insertion_normal_unit*scaleFactor)
#     spline.points[0].co = [origin_centroid[0],origin_centroid[1],origin_centroid[2],1] #convert vector to tuple, 4th number is nurbs weight, currently set to =1
#     spline.points[1].co = [point1[0],point1[1],point1[2],1]
#     #point 2 just leave at default position
#     spline.points[3].co = [point3[0],point3[1],point3[2],1]
#     spline.points[4].co = [insertion_centroid[0],insertion_centroid[1],insertion_centroid[2],1]
#     # add two more points for more refined control - or do this beforehand?
#     bpy.ops.object.mode_set(mode = 'EDIT')
#     bpy.ops.curve.select_all(action='DESELECT')
#     spline.points[1].select = True
#     spline.points[2].select = True
#     bpy.ops.curve.subdivide()
#     bpy.ops.object.mode_set(mode = 'EDIT')
#     bpy.ops.curve.select_all(action='DESELECT') #note this changes the numbers so now need to select 3 and 4
#     spline.points[3].select = True
#     spline.points[4].select = True 
#     bpy.ops.curve.subdivide()
#     #now create cross section for muscle from muscle origin
#     bpy.ops.object.mode_set(mode = 'OBJECT')
#     bpy.ops.object.select_all(action='DESELECT')
#     # select origin boundary loop for that particular muscle
#     bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " origin" + " boundary"] #make active 
#     bpy.data.objects[Muscle + " origin" + " boundary"].select_set(True)
#     bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(True, True, True), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
#     #duplicated objects now becomes selected and active
#     #rename and unparent
#     cross_section = bpy.context.view_layer.objects.active
#     cross_section.name = Muscle + " cross section template"
#     bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
#     align_with_XY(Muscle) #take cross section and move main dimension to XY plane, so that projection on curve is correct, also converts to curve
#     #Bevel nurbs path with origin boundary curve
#     bpy.ops.object.select_all(action='DESELECT')
#     bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " curve"] #make curve active
#     bpy.data.objects[Muscle + " cross section template"].select_set(True)
#     #bevel
#     bpy.context.object.data.bevel_mode = 'OBJECT'
#     bpy.context.object.data.bevel_object = bpy.data.objects[cross_section.name] 
#     bpy.context.object.data.bevel_factor_start = 0.2  #THIS NEEDS TO BE ADJUSTED BY USER SLIDER
#     bpy.context.object.data.bevel_factor_end = 0.8

# ### BREAK FOR USER ADJUSTMENT
# #user will likely have to change curve tilt to align cross section to origin and attachment orientations 
# #user can adjust curve shape, endpoint tilts etc, so add a button to confirm they have made those changes (curve alignment stuff) before the next piece of code

# bpy.ops.object.convert(target='MESH') #then convert curve to mesh

# ### BREAK FOR USER ADJUSTMENT
# #user can scale some edgeloops etc to adjust more

# def join_muscle(Muscle):
# #join origin and insertion boundaries to muscle volume mesh (duplicate origin and insertion boundaries first so that I can keep boundaries for muscle deconstruction tool)
# #duplicate and unparent

#     bpy.ops.object.select_all(action='DESELECT')
#     bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " origin" + " boundary"] #make active 
#     bpy.data.objects[Muscle + " origin" + " boundary"].select_set(True)
#     bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(True, True, True), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
#     bpy.context.view_layer.objects.active.name = [Muscle + "origin_merge_with_volume"]
#     bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
#     bpy.ops.object.select_all(action='DESELECT')
#     bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " insertion" + " boundary"] #make active 
#     bpy.data.objects[Muscle + " origin" + " boundary"].select_set(True)
#     bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(True, True, True), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
#     bpy.context.view_layer.objects.active.name = [Muscle + "insertion_merge_with_volume"]
#     bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
#     #select items to join
#     bpy.ops.object.select_all(action='DESELECT')
#     bpy.data.objects[Muscle + " curve"].select_set(True)
#     bpy.data.objects[Muscle + "origin_merge_with_volume"].select_set(True)
#     bpy.data.objects[Muscle + "insertion_merge_with_volume"].select_set(True)
#     bpy.ops.object.join()
#     muscle_volume = bpy.context.view_layer.objects.active
#     muscle_volume.name = Muscle + " volume"
#     #parent to empty
#     muscle_volume.select_set = True
#     bpy.context.view_layer.objects.active = bpy.data.objects[Muscle]  
#     bpy.data.objects[Muscle].select_set(True)
#     bpy.ops.object.parent_set(keep_transform=True)
#     bpy.data.objects[Muscle].select_set(False) #make sure only origin is selected
#     bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + attachmentName]
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