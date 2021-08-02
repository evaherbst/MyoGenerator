import bpy
import mathutils
from mathutils import Vector, Matrix
import math
import bmesh
from operator import itemgetter


def duplicate_boundaries(Muscle):
    bpy.ops.object.select_all(action='DESELECT')
    # make active
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle +
                                                             " origin" + " boundary"]
    bpy.data.objects[Muscle + " origin" + " boundary"].select_set(True)
    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked": False, "mode": 'TRANSLATION'}, TRANSFORM_OT_translate={"value": (0, 0, 0), "orient_type": 'GLOBAL', "orient_matrix": ((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type": 'GLOBAL', "constraint_axis": (True, True, True), "mirror": True, "use_proportional_edit": False, "proportional_edit_falloff": 'SMOOTH', "proportional_size": 1,
                                  "use_proportional_connected": False, "use_proportional_projected": False, "snap": False, "snap_target": 'CLOSEST', "snap_point": (0, 0, 0), "snap_align": False, "snap_normal": (0, 0, 0), "gpencil_strokes": False, "cursor_transform": False, "texture_space": False, "remove_on_cancel": False, "release_confirm": False, "use_accurate": False, "use_automerge_and_split": False})
    bpy.context.view_layer.objects.active.name = str(
        Muscle + " origin_merge_with_volume")
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
    bpy.ops.object.select_all(action='DESELECT')
    # make active
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle +
                                                             " insertion" + " boundary"]
    bpy.data.objects[Muscle + " insertion" + " boundary"].select_set(True)
    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked": False, "mode": 'TRANSLATION'}, TRANSFORM_OT_translate={"value": (0, 0, 0), "orient_type": 'GLOBAL', "orient_matrix": ((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type": 'GLOBAL', "constraint_axis": (True, True, True), "mirror": True, "use_proportional_edit": False, "proportional_edit_falloff": 'SMOOTH', "proportional_size": 1,
                                  "use_proportional_connected": False, "use_proportional_projected": False, "snap": False, "snap_target": 'CLOSEST', "snap_point": (0, 0, 0), "snap_align": False, "snap_normal": (0, 0, 0), "gpencil_strokes": False, "cursor_transform": False, "texture_space": False, "remove_on_cancel": False, "release_confirm": False, "use_accurate": False, "use_automerge_and_split": False})
    bpy.context.view_layer.objects.active.name = str(
        Muscle + " insertion_merge_with_volume")
    bpy.data.objects[Muscle + " insertion_merge_with_volume"].select_set(True)
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
    # select items to join
    bpy.ops.object.select_all(action='DESELECT')


def duplicate_attachment_areas(Muscle):
    bpy.ops.object.select_all(action='DESELECT')
    # make active
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " origin"]
    bpy.data.objects[Muscle + " origin"].select_set(True)
    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked": False, "mode": 'TRANSLATION'}, TRANSFORM_OT_translate={"value": (0, 0, 0), "orient_type": 'GLOBAL', "orient_matrix": ((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type": 'GLOBAL', "constraint_axis": (True, True, True), "mirror": True, "use_proportional_edit": False, "proportional_edit_falloff": 'SMOOTH', "proportional_size": 1,
                                  "use_proportional_connected": False, "use_proportional_projected": False, "snap": False, "snap_target": 'CLOSEST', "snap_point": (0, 0, 0), "snap_align": False, "snap_normal": (0, 0, 0), "gpencil_strokes": False, "cursor_transform": False, "texture_space": False, "remove_on_cancel": False, "release_confirm": False, "use_accurate": False, "use_automerge_and_split": False})
    bpy.context.view_layer.objects.active.name = str(
        Muscle + " origin_area_merge_with_volume")
    bpy.data.objects[Muscle +
                     " origin_area_merge_with_volume"].select_set(True)
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
    bpy.ops.object.select_all(action='DESELECT')
    # make active
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " insertion"]
    bpy.data.objects[Muscle + " insertion"].select_set(True)
    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked": False, "mode": 'TRANSLATION'}, TRANSFORM_OT_translate={"value": (0, 0, 0), "orient_type": 'GLOBAL', "orient_matrix": ((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type": 'GLOBAL', "constraint_axis": (True, True, True), "mirror": True, "use_proportional_edit": False, "proportional_edit_falloff": 'SMOOTH', "proportional_size": 1,
                                  "use_proportional_connected": False, "use_proportional_projected": False, "snap": False, "snap_target": 'CLOSEST', "snap_point": (0, 0, 0), "snap_align": False, "snap_normal": (0, 0, 0), "gpencil_strokes": False, "cursor_transform": False, "texture_space": False, "remove_on_cancel": False, "release_confirm": False, "use_accurate": False, "use_automerge_and_split": False})
    bpy.context.view_layer.objects.active.name = str(
        Muscle + " insertion_area_merge_with_volume")
    bpy.data.objects[Muscle +
                     " insertion_area_merge_with_volume"].select_set(True)
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
    # select items to join
    bpy.ops.object.select_all(action='DESELECT')


def get_volume_perimeter(Muscle, index, n, both_ends):
    #vertices_loop = []
    boundaryNames = [' origin_merge_with_volume',
                     ' insertion_merge_with_volume']
    boundaryName = boundaryNames[index]
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    # make active
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + boundaryName]
    bpy.data.objects[Muscle + boundaryName].select_set(True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            override = bpy.context.copy()
            override['area'] = area
            override['region'] = area.regions[4]
            bpy.ops.view3d.snap_cursor_to_selected(override)
    cursor = bpy.context.scene.cursor.location
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " curve"]
    bpy.data.objects[Muscle + " curve"].select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.context.tool_settings.mesh_select_mode = (
        True, False, False)  # vertex select mode
    bpy.ops.mesh.select_all(action='DESELECT')
   # now in all vertices in both_ends list, need to find closest n points to cursor
    distance_list = []
    for point in both_ends:
        co = point[1]
        distance = math.sqrt(
            (co[0] - cursor[0]) ** 2 + (co[1] - cursor[1]) ** 2 + (co[2] - cursor[2]) ** 2)
        # Look up slice notation - [:] makes it become a tuple
        point.append(distance)
    # for index, co in both_ends:
    #     distance = math.sqrt(
    #         (v.co[0] - cursor[0]) ** 2 + (v.co[1] - cursor[1]) ** 2 + (v.co[2] - cursor[2]) ** 2)
    #     # Look up slice notation - [:] makes it become a tuple
    #     distance_list.append([i, distance])
    distance_list_ascending = sorted((both_ends), key=itemgetter(2))
    shortest_n= distance_list_ascending[0:n]
    vertices_loop = [item[0] for item in shortest_n]
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.data.objects[Muscle + boundaryName].select_set(True)
    bpy.ops.object.join()
    bpy.ops.object.mode_set(mode='EDIT')
    obj = bpy.context.edit_object
    bpy.context.tool_settings.mesh_select_mode = (
        True, False, False)  # vertex select mode
    bpy.ops.mesh.select_all(action='DESELECT')
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    bpy.context.tool_settings.mesh_select_mode = (
        False, True, False)  # edgeselect mode
    bpy.ops.mesh.select_loose()  # select origin boundary loop
    bpy.context.tool_settings.mesh_select_mode = (
        True, False, False)  # vertex select mode
    for v in bm.verts:
        if v.select:
            vertices_loop.append(v.index)
    print(vertices_loop)
    # now use this list to select all boundary loops that need to be bridged
    bpy.ops.object.mode_set(mode='OBJECT')
    for i in vertices_loop:
        obj.data.vertices[i].select = True
    bpy.ops.object.mode_set(mode='EDIT')
    # bridge edge loops
    bpy.ops.mesh.bridge_edge_loops()
    bpy.ops.mesh.select_all(action='DESELECT')


def join_muscle(Muscle):
    #duplicate_boundaries(Muscle)
    both_ends = []
    boundaryNames = [' origin_merge_with_volume',
                     ' insertion_merge_with_volume']
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " curve"]
    bpy.data.objects[Muscle + " curve"].select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.context.tool_settings.mesh_select_mode = (
        True, False, False)  # vertex select mode
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_non_manifold()
    obj = bpy.context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    for v in bm.verts:
        if v.select:
            both_ends.append([v.index, v.co])
    print(len(both_ends))  # works till here
    n = int(len(both_ends)/2)
    print(n)
    get_volume_perimeter(Muscle, 0, n, both_ends)
    both_ends = []
    bpy.context.tool_settings.mesh_select_mode = (
        True, False, False)  # vertex select mode
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_non_manifold()
    obj = bpy.context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    for v in bm.verts:
        if v.select:
            both_ends.append(v.index, v.co)
    print(len(both_ends))  # works till here
    n = int(len(both_ends)/2)
    print(n)
    get_volume_perimeter(Muscle, 1, n, both_ends)
    muscle_volume = bpy.context.view_layer.objects.active
    muscle_volume.name = Muscle + " volume"
    # parent to empty
    muscle_volume.select_set(state=True)
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle]
    bpy.data.objects[Muscle].select_set(True)
    bpy.ops.object.parent_set(keep_transform=True)
    # make sure only origin is selected
    bpy.data.objects[Muscle].select_set(False)
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " volume"]
    # then duplicate origin and insertions (with faces) and merge
    # duplicate_attachment_areas()
    # bpy.ops.object.select_all(action='DESELECT')
    # bpy.data.objects[str(Muscle + " volume")].select_set(True)
    # bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " volume"] #make active
    # bpy.data.objects[str(Muscle + " origin_area_merge_with_volume")].select_set(True)
    # bpy.data.objects[str(Muscle + " insertion_area_merge_with_volume")].select_set(True)
    # bpy.ops.object.join()
    # #get rid of edge duplicates
    # bpy.ops.mesh.remove_doubles()
    # #then triangulate mesh
    # bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
