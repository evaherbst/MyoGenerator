


import bpy
import bmesh
total = 0
def get_length(name):
    global total
    obj = bpy.data.objects[name]  # particular object by name
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True) #selects obj
    bpy.context.view_layer.objects.active = bpy.data.objects[obj.name] #sets obj as active mesh
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.context.tool_settings.mesh_select_mode = (False, True, False) #vertex select mode
    bpy.ops.mesh.select_all(action='SELECT') #select all vertices
    me = bpy.context.object.data
    bm = bmesh.from_edit_mesh(me)
    if hasattr(bm.verts,"ensure_lookup_table"):
        bm.edges.ensure_lookup_table()
    for i in bm.edges:
        total+=i.calc_length()
    print(total)
    return total

