
import bpy
import math
import bmesh


def reorder_coords():
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.context.tool_settings.mesh_select_mode = (True, False, False) #vertex select mode
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



def create_boundary()

    name = obj.name

    # keep track of objects in scene to later rename new objects
    scn = bpy.context.scene
    names = [ obj.name for obj in scn.objects]


    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action='SELECT')


    #select outer loop, duplicate, separate
    bpy.ops.mesh.region_to_loop()p
    bpy.ops.mesh.duplicate()
    bpy.ops.mesh.separate(type='SELECTED')

    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all(action='DESELECT') 


    new_objs = [ obj for obj in scn.objects if not obj.name in names]

    #rename new object and select and make active
    """Ideally have user enter a name in the GUI - but for now I just hardcoded it as an example"""
    for obj in new_objs:
        obj.name = obj.name + "boundary"
        obj.data.name = obj.name + "boundary"
        obj.select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects[obj.name+ "boundary"]


    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True) #set transforms to make sure they are in global CS - not sure if necessary but just in case 
    #not sure if the above is applied to all objects or only selected or active



"""Overview of Main Loop:

Assume all muscles with the following parenting and naming systems: (Also see image "example_Blender_hierarchy_image")

Parent: empty with muscle name (e.g. "mAMEP")
Children:
-mAMEP origin (attachment with numerus faces)
-mAMEP insertion (attachment with numerus faces)
-mAMEP volume

For origin and attachment:
-select object, go to edit mode, select edge loop, save as separate object, rename to "[object name (e.g. "AMEM origin" or "AMEM insertion")] + "boundary") 


nice but not necessary: either parent the boundaries to the original muscle parent or delete them 

"""


def main_loop()

for obj in bpy.context.selected_objects:
    if obj.type == 'EMPTY':
      muscle_name=obj.name
      children = []
      children = obj.children
      for obj in children:
        if "origin" in obj.name:
            create_boundary()
            reorder_coords()
            export_coords()
          

        elif "insertion" in obj.name:
            create_boundary()
            reorder_coords()
            export_coords()


        elif "volume" in obj.name:
          """export as .stls - make sure that the orientations for export are the same as in the scene!!!"""



        else:
          print("Unproper naming of children. The following object will be ignored: "+obj.name)  



main_loop()





