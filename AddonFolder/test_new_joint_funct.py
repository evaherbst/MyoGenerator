#get edge loop by selecting closest n vertices on muscle volume to origin loop, where n = number of vertices in origin loop

n = 32 #later as function have n be an input of number of vertices in origin boundary (maybe with loop and length, or extract from renumber vertices function)
#on origin loop copy, set origin to geometry, set 3D cursor here
#[select origin loop copy]
bpy.ops.object.mode_set(mode = 'OBJECT')
bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + "origin_merge_with_volume"] #make active 
bpy.data.objects[Muscle + "origin_merge_with_volume"].select_set(True)
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
bpy.ops.view3d.snap_cursor_to_selected()
bpy.ops.object.mode_set(mode = 'EDIT')
bpy.context.tool_settings.mesh_select_mode = (True, False, False) #vertex select mode
bpy.ops.object.select_all(action='DESELECT')




























#with edge selected
bpy.ops.mesh.loop_multi_select(ring=False)


#if you join objects edge indices change, but can select edge loop and then merge and selection will still be there


#planning

#get closest edge on muscle volume to origin loop


#on origin loop copy, set origin to geometry, set 3D cursor here
#[select origin loop copy]
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
bpy.ops.view3d.snap_cursor_to_selected()



import mathutils

# create a kd-tree from a mesh
from bpy import context
obj = context.object

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
for (co, index, dist) in kd.find_n(co_find, 2): #trying n = 2
    print("    ", co, index, dist)




#unselect all, then select that edge


#select edge loop connected to that edge
bpy.ops.mesh.loop_multi_select(ring=False)

#join to origin loop




#get closest edge on muscle volume to insertion loop


#unselect all, then select that edge


#select edge loop connected to that edge
bpy.ops.mesh.loop_multi_select(ring=False)

#join to insertion loop







#then also make copies of origin and insertion areas and join

#then merge by distance (but this could maybe cause issues if other people's resolutions are high/each units are a small increment)
#maybe just make it really really small distance
#select all (works on either faces or edges)
bpy.ops.mesh.remove_doubles()



import bpy, bmesh

me = bpy.context.object.data

bm = bmesh.new()
bm.from_mesh(me)

me.vertices[0].select = True #works, in future replace 0 with index from kd tree code above 

for edge in bm.edges:
    if edge.verts[0].select = True
        edge.select = True

bm.to_mesh(me)
bm.free()

vert[0].select_set(True)
for edge in bm.edges:
    if edge.verts[0].select:
        edge.select_set(True) #THIS DOES NOT WORK, SINCE ALSO THE NON EDGE LOOP EDGE WOULD BE SELECTED. SO INSTRAD TRY TO GET EDGE LOOP FROM VERTICES

#EDGE LOOP FROM VERTICES ONLY WORKS IF THEY ARE 2 ADJACENT VERTICES
# NEW PLAN: QUERY NUMBER OF VERTICES IN ORIGIN LOOP AND SELECT THAT MANY CLOSEST ONES, SO QUERY N NUMBER OF CLOSEST POINT AND JUST SELECT




bpy.ops.mesh.loop_multi_select(ring=True)
