

#NOTE- make sure centroids are calculated based on centroids of muscle attachment and not of bone - need to test this at end to make sure

#NOW add beveling - need to set bounds, also need to convert origin boundary to curve, and at end convert it back and convert muscle curve to mesh


def curve_creator(attachment_centroids,attachment_normals):
    global origin_centroid
    global insertion_centroid
    global origin_normal
    global insertion_normal
    origin_centroid = attachment_centroids[0]
    insertion_centroid = attachment_centroids[1]
    origin_normal = attachment_normals[0]
    insertion_normal = attachment_normals[1]
    origin_normal = Vector(origin_normal)
    origin_normal_unit = origin_normal/origin_normal.length
    insertion_normal = Vector(insertion_normal)
    insertion_normal_unit = insertion_normal/insertion_normal.length
    bpy.ops.curve.primitive_nurbs_path_add(radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1)) #makes nurbs path with 5 points 
    spline = bpy.data.objects["NurbsPath"].data.splines[0] #need to change name later
    origin_centroid_tup = origin_centroid[0],origin_centroid[1],origin_centroid[2] #convert origin centroid data from vector to tuple
    insertion_centroid_tup = insertion_centroid[0],insertion_centroid[1],insertion_centroid[2]
    scaleFactor = .3
    point1 = origin_centroid + (origin_normal_unit*scaleFactor)
    point3 = insertion_centroid + (insertion_normal_unit*scaleFactor)
    spline.points[0].co = [origin_centroid[0],origin_centroid[1],origin_centroid[2],1] #4th number is nurbs weight, currently set to =1
    spline.points[1].co = [point1[0],point1[1],point1[2],1]
    #spline.points[2].co = .. though about setting this to midpoint of origin and insertion but don't want that bc it would mess up curve (e.g. be straight line), so leave default for now
    spline.points[3].co = [point3[0],point3[1],point3[2],1]
    spline.points[4].co = [insertion_centroid[0],insertion_centroid[1],insertion_centroid[2],1]













