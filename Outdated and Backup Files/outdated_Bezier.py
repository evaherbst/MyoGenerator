
def bezier_curve(attachment_centroids, attachment_normals):
    global origin_centroid
    global insertion_centroid
    global origin_normal
    global insertion_normal
    origin_centroid = attachment_centroids[0]
    insertion_centroid = attachment_centroids[1]
    origin_normal = attachment_normals[0]
    insertion_normal = attachment_normals[1]
    lineLength=math.sqrt((insertion_centroid[0] - origin_centroid[0]) ** 2 + (insertion_centroid[1] - origin_centroid[1]) ** 2 + (insertion_centroid[2] - origin_centroid[2]) ** 2)
    scaleFactor = .2*(lineLength)
    origin_normal_unit = origin_normal/origin_normal.length
    insertion_normal_unit = insertion_normal/insertion_normal.length
    bpy.ops.curve.primitive_bezier_curve_add(radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    #Curve becomes active object after creating so can just name here
    bpy.context.active_object.name = Muscle + " curve"
    curve = bpy.context.active_object
    bez_points = curve.data.splines[0].bezier_points
    bez_points[0].co = origin_centroid
    bez_points[0].handle_left = origin_centroid + (origin_normal_unit*scaleFactor)
    #bez_points[0].handle_left = origin_centroid + (origin_normal_unit)
    bez_points[0].handle_right = origin_centroid - (origin_normal_unit*scaleFactor)
    # bez_points[0].handle_right = origin_centroid - (origin_normal_unit)
    bez_points[1].co = insertion_centroid
    bez_points[1].handle_left = insertion_centroid + (insertion_normal_unit*scaleFactor)
    bez_points[1].handle_right = insertion_centroid - (insertion_normal_unit*scaleFactor)
    # bez_points[1].handle_left = insertion_centroid + (insertion_normal_unit)
    # bez_points[1].handle_right = insertion_centroid - (insertion_normal_unit)
    # reset_origin(curve) #doesn't work, get error "'Curve' object has no attribute 'vertices'" but don't need this for new method anyway