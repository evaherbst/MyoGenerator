import bpy
from mathutils import Vector, Matrix
import math
import bmesh

from AddonFolder import muscleCore


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