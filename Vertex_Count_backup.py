
#maybe a for loop to get all objects with "Muscle" in name, then for both origin boundary and insertion, do the following:





def reorder_coords(obj):
#to use for getting origin and insertion vertex numbers the same
    
#make sure correct object is active!

	bpy.ops.object.mode_set(mode = 'OBJECT') 
	bpy.ops.object.select_all(action='DESELECT')
	obj.select_set(True) #selects boundary
	bpy.context.view_layer.objects.active = bpy.data.objects[obj.name] #sets boundary as active mesh
	bpy.ops.object.mode_set(mode = 'EDIT')
	bpy.context.tool_settings.mesh_select_mode = (True, False, False) #vertex select mode
	bpy.ops.mesh.select_all(action='SELECT') #select all vertices

	#somehow the above section and the below section run well separately but not if I run them together as one chunk..
	me = bpy.context.object.data
	bm = bmesh.from_edit_mesh(me)

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




#then count vertices, find object with fewer vertices, add vertices



bpy.ops.mesh.subdivide()
