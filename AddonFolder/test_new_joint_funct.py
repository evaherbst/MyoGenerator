import mathutils
import bmesh
import bpy

def duplicate_boundaries():
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

#get edge loop by selecting closest n vertices on muscle volume to origin loop, where n = number of vertices in origin loop
def get_volume_perimeter(Muscle,index,n):
    global vertices_loop
    boundaryName = boundaryNames[index]
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + boundaryName] #make active 
    bpy.data.objects[Muscle + boundaryName].select_set(True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            override = bpy.context.copy()
            override['area'] = area
            override['region'] = area.regions[4]
            bpy.ops.view3d.snap_cursor_to_selected( override )
    #bpy.ops.view3d.snap_cursor_to_selected()
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " curve"]
    bpy.data.objects[Muscle + " curve"].select_set(True)
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.context.tool_settings.mesh_select_mode = (True, False, False) #vertex select mode
    bpy.ops.mesh.select_all(action='DESELECT')
    # create a kd-tree from a mesh
    obj = bpy.context.edit_object
    mesh = obj.data
    size = len(mesh.vertices)
    kd = mathutils.kdtree.KDTree(size)
    for i, v in enumerate(mesh.vertices):
        kd.insert(v.co, i)
    kd.balance()
    # 3d cursor relative to the object data
    co_find = obj.matrix_world.inverted() @ context.scene.cursor.location
    # Find the closest n points to the 3d cursor
    print("Closest n points")
    for (co, index, dist) in kd.find_n(co_find, n): 
        #print(index)
        vertices_loop.append(index)
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.data.objects[Muscle + boundaryName].select_set(True)
    bpy.ops.object.join()
    muscle_volume = bpy.context.view_layer.objects.active
    muscle_volume.name = Muscle + " volume"
    bpy.ops.object.mode_set(mode = 'EDIT')
    obj = bpy.context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    bpy.context.tool_settings.mesh_select_mode = (False, True, False) #edgeselect mode
    bpy.ops.mesh.select_loose() #select origin boundary loop
    bpy.context.tool_settings.mesh_select_mode = (True, False, False) #vertex select mode
    for v in bm.verts:
        if v.select:
            vertices_loop.append(v.index)
    bpy.ops.object.mode_set(mode = 'OBJECT') #now use this list to select all boundary loops that need to be bridged
    for i in vertices_loop:
        obj.data.vertices[i].select = True
    bpy.ops.object.mode_set(mode = 'EDIT')
    #bridge edge loops
    bpy.ops.mesh.bridge_edge_loops()

vertices_loop = []
Muscle = "Muscle"
boundaryNames = [' origin_merge_with_volume', ' insertion_merge_with_volume']
n = 32 #later as function have n be an input of number of vertices in origin boundary (maybe with loop and length, or extract from renumber vertices function)
#on origin loop copy, set origin to geometry, set 3D cursor here
get_volume_perimeter(Muscle,0,n)








#then do insertion


#then duplicate and merge with vertices


#then remove duplicates function to get rid of edge duplicates
bpy.ops.mesh.remove_doubles()


#then parent?




