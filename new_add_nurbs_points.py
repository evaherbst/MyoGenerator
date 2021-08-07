    bpy.ops.curve.primitive_nurbs_path_add(radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1)) #makes nurbs path with 5 points 
    curve = bpy.context.view_layer.objects.active
    curve.name = Muscle + " curve"
    spline = bpy.data.objects[curve.name].data.splines[0]
    point1 = origin_centroid + (origin_normal_unit*scaleFactor) #
    point3 = insertion_centroid + (insertion_normal_unit*scaleFactor)
    point2 = (point1[0]+point3[0])/2,(point1[1]+point3[1])/2,(point1[2]+point3[2])/2
    spline.points[0].co = [origin_centroid[0],origin_centroid[1],origin_centroid[2],1] #convert vector to tuple, 4th number is nurbs weight, currently set to =1
    spline.points[1].co = [point1[0],point1[1],point1[2],1]
    spline.points[2].co = [point2[0],point2[1],point2[2],1]
    spline.points[3].co = [point3[0],point3[1],point3[2],1]
    spline.points[4].co = [insertion_centroid[0],insertion_centroid[1],insertion_centroid[2],1]
    # add two more points for more refined control 
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.curve.select_all(action='DESELECT')
    curve.data.splines.active.points[1].select = True
    curve.data.splines.active.points[2].select = True
    bpy.ops.curve.subdivide()
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.curve.select_all(action='DESELECT') #note this changes the numbers so now need to select 3 and 4
    curve.data.splines.active.points[3].select = True
    curve.data.splines.active.points[4].select = True 