# # -*- coding: utf-8 -*-
"""

@authors: Eva C. Herbst and Niccolo Fioritti
this add-on enables generation of 3D muscles based on user selected origin and insertion areas and an adjustable muscle path
"""
from AddonFolder import myoGenerator_op
import bpy
import mathutils
from mathutils import Vector, Matrix
import math
import bmesh
import csv
from operator import itemgetter


origin_centroid = mathutils.Vector()
insertion_centroid = mathutils.Vector()
origin_normal = mathutils.Vector()
insertion_normal = mathutils.Vector()
origin_centroid = 0
origin_normal = 0
insertion_centroid = 0
insertion_normal = 0

muscleName = ''


def make_empty(Muscle):

    from AddonFolder import globalVariables

    global muscleName
    globalVariables.muscleName = Muscle
    muscleName = Muscle

    globalVariables.allMuscleParameters[muscleName] = [
        0, 0, 0, 0, 0, 0, 0]  # assigning to dict()

    try:
        bpy.ops.object.mode_set(mode='OBJECT')
    except BaseException:
        pass
    o = bpy.data.objects.new(Muscle, None)
    o.empty_display_size = 2
    o.empty_display_type = 'PLAIN_AXES'
    # make sure all created objects are in the same collection, named "Collection"
    # Set target collection to a known collection
    coll_target = bpy.context.scene.collection.children.get("Collection")
    # If target found and object list not empty
    for coll in o.users_collection:
        # Unlink the object
        coll.objects.unlink(o)
    # Link each object to the target collection
    coll_target.objects.link(o)
    bpy.ops.object.select_all(action='SELECT')
    for obj in bpy.context.selected_objects:
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.object.select_all(action='DESELECT')
    


# function creates attachment as new object, parents to muscle empty
def create_attachment(index, Muscle):
    # also contains functions to recenter object, create boundary, and
    # calculate centroids and normals
    from AddonFolder import globalVariables

    attachmentNames = [' origin', ' insertion']
    attachmentName = attachmentNames[index]
    scn = bpy.context.scene
    # keep track of objects in scene to later rename new objects (#can't just
    # rename active object bc duplicated object doesn't automatically become
    # active)
    names = [obj.name for obj in scn.objects]
    # select faces, duplicate, separate
    bpy.ops.mesh.duplicate()
    bpy.ops.mesh.separate(type='LOOSE')
    bpy.ops.object.mode_set(mode='OBJECT')
    # make sure one random object is selected in scene (necessary so code runs
    # smoothly, if none are selected deselect won't work)
    random_obj = bpy.context.scene.objects[0]
    random_obj.select_set(True)
    bpy.ops.object.select_all(action='DESELECT')
    new_objs = [obj for obj in scn.objects if obj.name not in names]
    # rename new object and select and make active
    for obj in new_objs:
        obj.name = Muscle + attachmentName
        obj.data.name = obj.name  # set mesh name to object name
        obj.select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + attachmentName]
    # Parent to the muscle empty
    # This works!
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle]
    bpy.data.objects[Muscle].select_set(True)
    bpy.ops.object.parent_set(keep_transform=True)
    # make sure only origin is selected  #DOUBLE CHECK
    bpy.data.objects[Muscle].select_set(False)
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + attachmentName]
    obj = bpy.context.view_layer.objects.active
    object_Recenter(obj)
    norm = get_normal(obj)
    globalVariables.attachment_normals[index] = norm
    bpy.ops.object.mode_set(mode='OBJECT')
    att = calculate_centroid(obj)
    globalVariables.attachment_centroids[index] = att
    create_boundary(obj)

    area = get_attachment_area(obj)

    if(index == 0):
        centroidIdx = 2
        areaIdx = 0
    else:
        centroidIdx = 3
        areaIdx = 1

    # Store the centroid values int the dictionary.
    globalVariables.allMuscleParameters[globalVariables.muscleName][centroidIdx] = att
    globalVariables.allMuscleParameters[globalVariables.muscleName][areaIdx] = area

    if(index == 1):  # calculate linear length only once both centroids are calculated
        a = globalVariables.allMuscleParameters[globalVariables.muscleName][2]
        b = globalVariables.allMuscleParameters[globalVariables.muscleName][3]
        linearLength = math.sqrt(
            (a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2)
        globalVariables.allMuscleParameters[globalVariables.muscleName][4] = linearLength
        print("a = ", a)
        print("b = ", b)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')


# calculate muscle attachment
def get_attachment_area(obj):

    # set scale = 1 to get correct area values
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    objName = obj.name
    me = obj.data
    me.name = objName
    # Get a BMesh representation
    bm = bmesh.new()  # create an empty BMesh
    bm.from_mesh(me)  # fill it in from a Mesh
    area = sum(f.calc_area() for f in bm.faces)
    print("area = " + str(area))
    return area


# region GENERAL FUNCTIONALITIES:
def set_edit_mode():  # sets edit mode
    # go to edit mode and face select mode, clear selection
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.context.tool_settings.mesh_select_mode = (False, False, True)
    bpy.ops.mesh.select_all(action='DESELECT')

# region SPECIFIC FOR create_attachment


def object_Recenter(obj):
    # center origin of object on center of mass
    # make sure nothing else in scene is selected
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)  # select obj only
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')


def create_boundary(obj):  # makes boundary, parents to attachment area area

    name = obj.name
    # keep track of objects in scene to later rename new objects
    scn = bpy.context.scene
    names = [obj.name for obj in scn.objects]
    bpy.context.view_layer.objects.active = bpy.data.objects[name]
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    # select outer loop, duplicate, separate
    bpy.ops.mesh.region_to_loop()
    bpy.ops.mesh.duplicate()
    bpy.ops.mesh.separate(type='LOOSE')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    new_objs = [obj for obj in scn.objects if obj.name not in names]
    # rename new object and select and make active
    for item in new_objs:
        print(item.name + " is a new item")
        item.name = name + " boundary"
        item.data.name = item.name  # set mesh name to object name
        item.select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects[name]
        bpy.data.objects[name].select_set(True)
        # parents new loop to the attachment area
        bpy.ops.object.parent_set(keep_transform=True)
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = bpy.data.objects[name + " boundary"]
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.context.tool_settings.mesh_select_mode = (False, False, True)
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.delete(type='ONLY_FACE')
        boundary = bpy.context.view_layer.objects.active
    bpy.ops.object.mode_set(mode='OBJECT')
    return boundary


def get_normal(obj):
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.context.tool_settings.mesh_select_mode = (False, False, True)
    bpy.ops.mesh.select_all(action='SELECT')
    bm = bmesh.from_edit_mesh(obj.data)
    # Reference selected face indices
    bm.faces.ensure_lookup_table()
    selFaces = [f.index for f in bm.faces if f.select]
    # Calculate the average normal vector
    avgNormal = Vector()
    for i in selFaces:
        avgNormal += bm.faces[i].normal
    avgNormal = avgNormal / len(selFaces)
    normal = avgNormal

    return normal


def calculate_centroid(obj):
    centroid = obj.location
    return centroid

# endregion


def curve_creator(attachment_centroids, attachment_normals, Muscle):

    global origin_centroid
    global insertion_centroid
    global origin_normal
    global insertion_normal
    origin_centroid = attachment_centroids[0]
    insertion_centroid = attachment_centroids[1]
    origin_normal = attachment_normals[0]
    insertion_normal = attachment_normals[1]
    lineLength = math.sqrt((insertion_centroid[0] -
                            origin_centroid[0]) ** 2 +
                           (insertion_centroid[1] -
                            origin_centroid[1]) ** 2 +
                           (insertion_centroid[2] -
                            origin_centroid[2]) ** 2)
    scaleFactor = .1 * (lineLength)
    origin_normal = Vector(origin_normal)
    print("origin normal is " + str(origin_normal))
    origin_normal_unit = origin_normal / origin_normal.length
    insertion_normal = Vector(insertion_normal)
    insertion_normal_unit = insertion_normal / insertion_normal.length
    bpy.ops.curve.primitive_nurbs_path_add(
        radius=1, enter_editmode=False, align='WORLD', location=(
            0, 0, 0), scale=(
            1, 1, 1))  # makes nurbs path with 5 points
    curve = bpy.context.view_layer.objects.active
    curve.name = Muscle + " curve"
    spline = bpy.data.objects[curve.name].data.splines[0]
    point1 = origin_centroid + (origin_normal_unit * scaleFactor)
    point3 = insertion_centroid + (insertion_normal_unit * scaleFactor)
    point2 = (point1[0] + point3[0]) / 2, (point1[1] +
                                           point3[1]) / 2, (point1[2] + point3[2]) / 2
    spline.points[0].co = [
        origin_centroid[0],
        origin_centroid[1],
        origin_centroid[2],
        1]  # convert vector to tuple, 4th number is nurbs weight, set to =1
    spline.points[1].co = [point1[0], point1[1], point1[2], 1]
    spline.points[2].co = [point2[0], point2[1], point2[2], 1]
    spline.points[3].co = [point3[0], point3[1], point3[2], 1]
    spline.points[4].co = [
        insertion_centroid[0],
        insertion_centroid[1],
        insertion_centroid[2],
        1]
    # add two more points for more refined control
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.curve.select_all(action='DESELECT')
    curve.data.splines.active.points[1].select = True
    curve.data.splines.active.points[2].select = True
    bpy.ops.curve.subdivide()
    bpy.ops.object.mode_set(mode='EDIT')
    # note this changes the numbers so now need to select 3 and 4
    bpy.ops.curve.select_all(action='DESELECT')
    curve.data.splines.active.points[3].select = True
    curve.data.splines.active.points[4].select = True
    bpy.ops.curve.subdivide()

    # now create cross section for muscle from muscle origin

    bpy.ops.object.editmode_toggle()
    bpy.ops.object.select_all(action='DESELECT')
    # select origin boundary loop for that particular muscle
    # make active
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle +
                                                             " origin" + " boundary"]
    bpy.data.objects[Muscle + " origin" + " boundary"].select_set(True)
    bpy.ops.object.duplicate()
    # duplicated objects now becomes selected and active
    #rename and unparent
    cross_section = bpy.context.view_layer.objects.active
    cross_section.name = Muscle + " cross section template"
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')

    # take cross section and move main dimension to XY plane, so that
    # projection on curve is correct, also converts to curve
    align_with_XY(Muscle)
    # Bevel nurbs path with origin boundary curve
    bpy.ops.object.mode_set(mode='OBJECT')  
    bpy.ops.object.select_all(action='DESELECT')

    cross_section = bpy.context.view_layer.objects.active
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
    bpy.data.objects[Muscle + " cross section template"].select_set(True)
    bpy.ops.object.convert(target='CURVE')

    bpy.ops.object.mode_set(mode='OBJECT')  
    bpy.ops.object.select_all(action='DESELECT')

    # make curve active
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " curve"]
    bpy.data.objects[Muscle + " cross section template"].select_set(True)
    # bevel
    bpy.context.object.data.bevel_mode = 'OBJECT'
    bpy.context.object.data.bevel_object = bpy.data.objects[cross_section.name]
    bpy.context.object.data.bevel_factor_start = 0  # user can adjust this in add-on
    bpy.context.object.data.bevel_factor_end = 1
    bpy.context.object.data.use_fill_caps = False
    bpy.ops.object.select_all(action='DESELECT')
    # make curve active
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " curve"]


def align_with_XY(Muscle):
    #orients cross section to be as parallel as possible to XY plane, to make sure that regardless of initial origin orientation in scene, muscle cross section will be the 
    # largest planar projection of that origin area
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    # make active
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle +
                                                             " cross section template"]
    bpy.data.objects[Muscle + " cross section template"].select_set(True)
    bpy.data.objects[Muscle + " origin" + " boundary"].select_set(False)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.context.tool_settings.mesh_select_mode = (
        False, True, False)   # edge selection mode
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.edge_face_add()  # add face
    bpy.context.tool_settings.mesh_select_mode = (
        False, False, True)  # face selection mode
    bpy.ops.mesh.select_all(action='SELECT')
    me = bpy.context.edit_object.data
    # get bmesh (Object needs to be in Edit mode)
    bm = bmesh.from_edit_mesh(me)
    if hasattr(bm.faces, "ensure_lookup_table"):
        bm.faces.ensure_lookup_table()
    bm.select_history.add(bm.faces[0])
    context = bpy.context
    ob = context.edit_object
    me = ob.data
    bm = bmesh.from_edit_mesh(me)
    face = bm.select_history.active
    o = face.calc_center_median()
    face.normal_update()
    edges = sorted(
        (e for e in face.edges),
        key=lambda e: abs(
            (e.verts[1].co -
             e.verts[0].co).dot(
                face.normal)))
    e = edges[0]
    T = Matrix.Translation(-o)
    up = Vector((0, 0, 1))
    R = face.normal.rotation_difference(up).to_matrix()
    bmesh.ops.transform(bm, verts=bm.verts, matrix=R, space=T)
    forward = Vector((0, 1, 0))
    R = (
        e.verts[1].co -
        e.verts[0].co).rotation_difference(forward).to_matrix()
    bmesh.ops.transform(bm, verts=bm.verts, matrix=R, space=T)
    T = Matrix.Translation(face.calc_center_median() - o)
    bmesh.ops.transform(bm, verts=bm.verts, matrix=T)
    bmesh.update_edit_mesh(me)

def mirror_bevel(Muscle):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    # make active
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " cross section template"]
    bpy.data.objects[Muscle + " cross section template"].select_set(True)
    #flip X axis to mirror object
    bpy.context.object.scale[0] = -1
    #apply scale transform
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " curve"]
    bpy.data.objects[Muscle + " curve"].select_set(True)
    bpy.data.objects[Muscle + " cross section template"].select_set(False)
    bpy.ops.object.mode_set(mode='EDIT')



def Transform_to_Mesh(Muscle):

    try:
        bpy.ops.object.mode_set(mode='OBJECT')
    except BaseException:
        pass
    bpy.ops.object.select_all(action='DESELECT')

    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " curve"]
    bpy.data.objects[Muscle + " curve"].select_set(True)
    bpy.ops.object.convert(target="MESH")







def duplicate_boundaries(Muscle):
    bpy.ops.object.select_all(action='DESELECT')
    # make active
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle +
                                                             " origin" + " boundary"]
    bpy.data.objects[Muscle + " origin" + " boundary"].select_set(True)
    bpy.ops.object.duplicate()
    bpy.context.view_layer.objects.active.name = str(
        Muscle + " origin_merge_with_volume")
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
    bpy.ops.object.select_all(action='DESELECT')
    # make active
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle +
                                                             " insertion" + " boundary"]
    bpy.data.objects[Muscle + " insertion" + " boundary"].select_set(True)
    bpy.ops.object.duplicate()
    bpy.context.view_layer.objects.active.name = str(
        Muscle + " insertion_merge_with_volume")
    bpy.data.objects[Muscle + " insertion_merge_with_volume"].select_set(True)
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
    # select items to join
    bpy.ops.object.select_all(action='DESELECT')


def duplicate_attachment_areas(Muscle):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    # make active
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " origin"]
    bpy.data.objects[Muscle + " origin"].select_set(True)
    bpy.ops.object.duplicate()
    bpy.context.view_layer.objects.active.name = str(
        Muscle + " origin_area_merge_with_volume")
    bpy.data.objects[Muscle +
                     " origin_area_merge_with_volume"].select_set(True)
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
    bpy.ops.object.select_all(action='DESELECT')
    # make active
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " insertion"]
    bpy.data.objects[Muscle + " insertion"].select_set(True)
    bpy.ops.object.duplicate()

    bpy.context.view_layer.objects.active.name = str(
        Muscle + " insertion_area_merge_with_volume")
    bpy.data.objects[Muscle +
                     " insertion_area_merge_with_volume"].select_set(True)
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
    # select items to join
    bpy.ops.object.select_all(action='DESELECT')


def join_muscle(Muscle):
    boundaryNames = [' origin_merge_with_volume',
                     ' insertion_merge_with_volume']
    
    duplicate_boundaries(Muscle)

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')

    #delete cross section template
    bpy.data.objects[Muscle + " cross section template"].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " cross section template"]
    bpy.ops.object.delete()


    #make origin boundary active and select
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle +
                                                             boundaryNames[0]]
    bpy.data.objects[Muscle + boundaryNames[0]].select_set(True)

    # get center of origin loop
    boundary = bpy.context.view_layer.objects.active
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY',
                              center='BOUNDS')  # set object origin to geometry
    loc_origin = boundary.location
    print("boundary center" + str(loc_origin))

    #select muscle volume, select end loops, duplicate and separate (to bridge with origin and insertion loops)
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " curve"]
    bpy.data.objects[Muscle + " curve"].select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.context.tool_settings.mesh_select_mode = (
        True, False, False)  # vertex select mode
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_non_manifold()
    # duplicate
    bpy.ops.mesh.duplicate()
    bpy.ops.mesh.separate(type='LOOSE')
    bpy.ops.object.mode_set(mode='OBJECT')
    tube_ends = []
    bpy.data.objects[Muscle + " curve"].select_set(False)
    for obj in bpy.context.selected_objects:
        bpy.ops.object.origin_set(
            type='ORIGIN_GEOMETRY',
            center='BOUNDS')  # set object origin to geometry
        center = obj.location
        distance_to_origin = math.sqrt((center[0] - loc_origin[0]) ** 2 + (
            center[1] - loc_origin[1]) ** 2 + (center[2] - loc_origin[2]) ** 2)
        tube_ends.append([obj.name, distance_to_origin])
    print("tube ends list " + str(tube_ends))
    distance_list_ascending = sorted((tube_ends), key=itemgetter(1))
    print("distances list ascending is " + str(distance_list_ascending))
    origin_side = distance_list_ascending[0][0]
    insertion_side = distance_list_ascending[1][0]
    print("origin object is " + str(origin_side))

    #bridge origin side
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[origin_side].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[origin_side]
    bpy.data.objects[Muscle + boundaryNames[0]].select_set(True)
    bpy.ops.object.join()
    # bridge edge loops
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.bridge_edge_loops()

    #bridge insertion side
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[insertion_side].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[insertion_side]
    bpy.data.objects[Muscle + boundaryNames[1]].select_set(True)
    bpy.ops.object.join()
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.bridge_edge_loops()

    #merge bridged ends with muscle volume
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.data.objects[Muscle + " curve"].select_set(True)
    bpy.data.objects[origin_side].select_set(True)
    bpy.data.objects[insertion_side].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " curve"]
    bpy.ops.object.join()
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles()

    #rename, parent, merge with origin and attachment areas
    bpy.ops.object.mode_set(mode='OBJECT')
    muscle_volume = bpy.context.view_layer.objects.active
    muscle_volume.name = Muscle + " volume"
    # parent to empty
    muscle_volume.select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle]
    bpy.data.objects[Muscle].select_set(True)
    bpy.ops.object.parent_set(keep_transform=True)
    # deselect empty
    bpy.data.objects[Muscle].select_set(False)
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " volume"]
    # then duplicate origin and insertions (with faces) and merge
    duplicate_attachment_areas(Muscle)
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[str(Muscle + " volume")].select_set(True)
    # make active
    bpy.context.view_layer.objects.active = bpy.data.objects[Muscle + " volume"]
    bpy.data.objects[str(
        Muscle + " origin_area_merge_with_volume")].select_set(True)
    bpy.data.objects[str(
        Muscle + " insertion_area_merge_with_volume")].select_set(True)
    bpy.ops.object.join()
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles()  # get rid of edge duplicates
    bpy.ops.mesh.normals_make_consistent(
        inside=False)  # recalculate outside normals
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.shade_flat()
    #get rid of T junctions by connecting edges and vertices by creating faces where the holes are (holes are hidden at T junction)
    #once connected via faces, remove 0 area faces with degenerate dissolve, then select whole mesh and triangulate
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_non_manifold()
    bpy.ops.mesh.edge_face_add()
    bpy.ops.mesh.dissolve_degenerate()
    #bpy.ops.mesh.select_all(action='SELECT')
    #bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
    bpy.ops.object.mode_set(mode='OBJECT')


def get_length():

    from AddonFolder import globalVariables
    length = 0
    try:
        bpy.ops.object.mode_set(mode='OBJECT')
    except BaseException:
        pass
    bpy.context.view_layer.objects.active = bpy.data.objects[globalVariables.muscleName + " curve"]
    bpy.data.objects[globalVariables.muscleName + " curve"].select_set(True)
    bpy.ops.object.duplicate()
    bpy.context.view_layer.objects.active.name = "curve_copy"
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = bpy.data.objects["curve_copy"]
    bpy.data.objects["curve_copy"].select_set(True)
    bpy.context.object.data.bevel_object = None
    bpy.ops.object.convert(target="MESH")

    obj = bpy.data.objects["curve_copy"]  # particular object by name
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)  # selects obj
    # sets obj as active mesh
    bpy.context.view_layer.objects.active = bpy.data.objects[obj.name]
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.context.tool_settings.mesh_select_mode = (
        False, True, False)  # edges select mode
    bpy.ops.mesh.select_all(action='DESELECT')  # select all edges
    bpy.ops.mesh.select_all(action='SELECT')  # select all edges
    me = bpy.context.object.data
    bm = bmesh.from_edit_mesh(me)
    if hasattr(bm.verts, "ensure_lookup_table"):
        bm.edges.ensure_lookup_table()
    for i in bm.edges:
        length += i.calc_length()
    print(length)

    try:
        bpy.ops.object.mode_set(mode='OBJECT')
    except BaseException:
        pass
    bpy.ops.object.delete()
    globalVariables.allMuscleParameters[globalVariables.muscleName][5] = length
    print(globalVariables.allMuscleParameters[globalVariables.muscleName])

    dir = globalVariables.csvDir

    DictionaryExporter(globalVariables.allMuscleParameters, dir)


def DictionaryExporter(d, dir):
    import csv
    import os
    directory = dir
    rows = []
    print(rows)
    with open(directory, "a", newline='') as f:

        writer = csv.writer(f)

        for key in d:
            row = []
            row.append(key)
            row = row + d[key]
            writer.writerow(row)


def measure_muscle_volume(obj):
    import bmesh
    # set scale = 1 to get correct volume values
    bpy.ops.object.transform_apply(location=False, scale=True, rotation=False)
    me = obj.data
    # Get a BMesh representation
    bm = bmesh.new()  # create an empty BMesh
    bm.from_mesh(me)  # fill it in from a Mesh
    # triangulate prior makes the difference
    bmesh.ops.triangulate(bm, faces=bm.faces)
    print("Volume")
    volume = bm.calc_volume()
    print(volume)
    return volume
    # bm.clear()


def updateVolumes():
    from AddonFolder import globalVariables

    try:
        bpy.ops.object.mode_set(mode='OBJECT')
    except BaseException:
        pass
    bpy.ops.object.select_all(action='DESELECT')
    directory = globalVariables.csvDir
    print("File name that muscle outputs are written to is:" + directory)
    muscleMetrics = {}
    # Open the file in read mode
    with open(directory, mode='r') as infile:
        # Open a reader to the csv
        reader = csv.reader(infile, delimiter=',')
    # Read into the dictionary using dictionary comprehension, key is the
    # first column and row are rest of the columns
        for row in reader:
            print(row)
            if row[3].startswith("<Vector"): #check if you already removed Vector string, if not, do so
                    row[3] = row[3].replace("<Vector (", "")
                    row[3] = row[3].replace(")>", "")
                    row[4] = row[4].replace("<Vector (", "")
                    row[4] = row[4].replace(")>", "")
                # create dictionary where key = muscle name, value = all values
            muscleMetrics[row[0]] = row[1:]
    print("muscle metrics from csv: " + str(muscleMetrics))
    bpy.ops.object.select_all(action='SELECT')
    # now calculate muscle volumes for all volumes in scence
    for obj in bpy.context.selected_objects:
        print(obj)
        if obj.type == 'EMPTY':
            muscleName = obj.name
            print(type(muscleName))
            print(muscleName)
            children = []
            children = obj.children
            for obj in children:
                if "volume" in obj.name:
                    muscleVolume = measure_muscle_volume(obj)
                    muscleMetrics[muscleName][6] = muscleVolume
                # make dictionary with key = muscleName and value =
                # muscle_volume
            print("updated values: " + str(muscleMetrics))
    header = [
        'muscle_name',
        'origin_area',
        'insertion_area',
        'origin_centroid',
        'insertion_centroid',
        'linear_length',
        'muscle_length',
        'muscle_volume']

    d_new = muscleMetrics

    with open(directory, "w", newline='') as f:
        writer = csv.writer(f)
        if d_new.get("muscle_name"):
            # header will already exist *if* volumes were already calculated,
            # this checks and only writes if header doesn't exist
            print("header already written")
        else:
            writer.writerow(header)
        for key in d_new:
            row = []
            row.append(key)
            row = row + d_new[key]
            writer.writerow(row)
