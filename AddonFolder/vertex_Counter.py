import math

import bmesh
import bpy

from AddonFolder import muscleCore


def change_vertex_number(
        originCount,
        insertionCount,
        origin_boundary_obj,
        insertion_boundary_obj):
    print("OriginCount = ", originCount, " InsCount =", insertionCount)
    vertexDiff = abs(originCount - insertionCount)
    print("vert Diff", vertexDiff)
    counter = 0
    print(counter)
    print(type(originCount))
    if (originCount < insertionCount):
        print("ORIGIN < INSERTION")
        increment = math.floor((originCount) / vertexDiff)  # rounds down
        if(increment == 0):
            increment += 1
        origin_boundary_obj.select_set(True)
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.context.tool_settings.mesh_select_mode = (
            False, True, False)  # edge select mode
        obj = origin_boundary_obj
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        for x in range(0, originCount - 1, increment):
            if(counter < vertexDiff):
                counter += 1
                bpy.ops.object.mode_set(mode='OBJECT')
                for edge in obj.data.edges:
                    edge.select = False
                obj.data.edges[x].select = True
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.subdivide()
                print(counter)
                print("subdivision successful")
                #bpy.ops.object.mode_set(mode='OBJECT')
    elif (originCount > insertionCount):
        print("ORIGIN > INSERTION")
        # rounds down to nearest whole number increment
        increment = math.floor((insertionCount) / vertexDiff)
        if(increment == 0):
            increment += 1
        print(increment)
        insertion_boundary_obj.select_set(True)
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.context.tool_settings.mesh_select_mode = (
            False, True, False)  # edge select mode
        obj = insertion_boundary_obj
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        for x in range(0, originCount - 1, increment):
            if(counter < vertexDiff):
                counter += 1
                bpy.ops.object.mode_set(mode='OBJECT')
                for edge in obj.data.edges:
                    edge.select = False
                obj.data.edges[x].select = True
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.subdivide()
                print(counter)
                print("subdivision successful")
                #bpy.ops.object.mode_set(mode='OBJECT')
    elif (originCount == insertionCount):
        print('wow, that was lucky')


def reorder_coords(obj):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)  # selects boundary
    # sets boundary as active mesh
    bpy.context.view_layer.objects.active = bpy.data.objects[obj.name]
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.context.tool_settings.mesh_select_mode = (
        True, False, False)  # vertex select mode
    bpy.ops.mesh.select_all(action='SELECT')  # select all vertices
    me = bpy.context.object.data
    bm = bmesh.from_edit_mesh(me)
    if hasattr(bm.verts, "ensure_lookup_table"):
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
        if next is None:
            break
        prev, vert = vert, next
    bm.verts.sort()
    bmesh.update_edit_mesh(me)
    return len(bm.verts)


def OverallVertexCount():

    Muscle = muscleCore.muscleName
    bpy.ops.object.mode_set(mode='OBJECT')
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

    change_vertex_number(
        originCounts,
        insertionCounts,
        origin_boundary_obj,
        insertion_boundary_obj)
