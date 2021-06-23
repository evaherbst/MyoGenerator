def reset_origin(curve): #GIVES ERROR CURVE HAS NO ATTRIBUTE VERTICES
    offset = origin_centroid - curve.location
    me = curve.data
    for v in me.vertices:
        v.co = v.co - offset
    me.update()
    curve.location = curve.location + offset
