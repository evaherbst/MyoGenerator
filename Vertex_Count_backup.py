import bpy
import bmesh
import math

def change_vertex_number(originCount,insertionCount):

  print("OriginCount = ", originCount," InsCount =", insertionCount)
  
  vertexDiff = 2
  #vertexDiff=abs(originCount-insertionCount)
  print ("vert Diff", vertexDiff)
  counter = 0

  if(originCount>insertionCount):
    
    print("ORIGIN > INSERTION")
    #need to divide "random" edges vertexDiff times
    # insertionCount-1 / vertexDiff = how many times to jump
    #check if number vertexDiff < vertexCount
    #pick indexes to subdivide (int(vertexCount/vertexDiff))
    # for i in
    
    increment = math.floor((insertionCount)/vertexDiff) #rounds down to nearest whole number increment
    
    insertion_boundary_obj.select_set(True)
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.context.tool_settings.mesh_select_mode = (False, True, False) #edge select mode
    
    for x in range(0, insertionCount-1, increment):


      if(counter< vertexDiff):
        counter+=1 
        insertion_boundary_obj.select_set(True)
        #edgeList [ x ] . subdivide
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode = 'OBJECT')
        obj.data.edges[x].select = True
        bpy.ops.object.mode_set(mode = 'EDIT') 
        bpy.ops.mesh.subdivide()

    #  else:
    #    break
  
  if (originCount < insertionCount):
    print("ORIGIN < INSERTION")
    increment = math.floor((originCount)/vertexDiff) #rounds down 

    origin_boundary_obj.select_set(True)
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.context.tool_settings.mesh_select_mode = (False, True, False) #edge select mode
    
    for x in range(0, originCount-1, increment):

      if(counter< vertexDiff):
        counter+=1        
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode = 'OBJECT')
        obj.data.edges[x].select = True
        bpy.ops.object.mode_set(mode = 'EDIT') 
        bpy.ops.mesh.subdivide()

    #  else:
    #    break

  if (originCount == insertionCount):

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
    # index of the start vertex
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

# reorder_coords(bpy.context.view_layer.objects.active)




Muscle = "Muscle"

bpy.ops.object.mode_set(mode = 'OBJECT') 
bpy.ops.object.select_all(action='SELECT')

for obj in bpy.context.selected_objects:
  if Muscle in obj.name and "boundary" in obj.name:
    print(obj)
    if "origin" in obj.name:
      origin_boundary_obj = obj
      originVertexCount = reorder_coords(obj)
      print("reordering origin")
    if "insertion" in obj.name:
      insertionVertexCount = reorder_coords(obj)
      insertion_boundary_obj = obj
      print("reordering insertion")

print(insertionVertexCount, " ORIGINVERTEXCOUNT")

change_vertex_number(originVertexCount,insertionVertexCount)


