def export_coords():
path = 'C:/Users/evach/Dropbox/MuscleTool/test_new_code_coords.txt'
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True) #need to set transforms to make sure they are in global CS
bpy.ops.object.mode_set(mode = 'EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.context.tool_settings.mesh_select_mode = (True, False, False) #vertex select mode
obj = bpy.context.object
file = open(path,'w')
# Get the active mesh
obj = bpy.context.edit_object
me = obj.data
# Get a BMesh representation
bm = bmesh.from_edit_mesh(me)
bm.faces.active = None
for v in bm.verts:
    if v.select:
        file.write(str(tuple(v.co) )+'\n')
        print(str(tuple(v.co)))
