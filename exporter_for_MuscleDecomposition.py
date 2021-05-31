
import bpy
import math
import bmesh
import re
import os
import csv
import re


def reorder_coords(obj):
    
#Do I need to deselect all here, and then make this object active? or is it enough to just have the obj argument?
#Do I need to make the object active? or is it fine with the input argument? #Test!
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

	
def export_coords():

#Do I need to deselect all here, and then make this object active? or is it enough to just have the obj argument?
#Do I need to make the object active? or is it fine with the input argument? #Test!
name = obj.name
filepath = bpy.data.filepath
main_path = os.path.dirname(filepath)
suffix = '.vtk'
print("writing to: " + main_path)
outputFile = os.path.join(main_path, name) + suffix
print(outputFile)


#How to make this actually add the name and not write out "name"?
#and should we use os.path.join(dir_name, base_filename + "." + filename_suffix) for all our code to make it compatible for all OS?

bpy.ops.object.mode_set(mode = 'OBJECT')
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True) # I think the locations need to be set to 0/global (as in done in line 34) to make sure vertices are in global space - otherwise will be in local (relative to object origin)
#bc the object acts as a "parent" to the vertices so need to make sure that parent's transforms are zeroed
bpy.ops.object.mode_set(mode = 'EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.context.tool_settings.mesh_select_mode = (True, False, False) #vertex select mode
obj = bpy.context.object

# Get the active mesh
obj = bpy.context.edit_object
me = obj.data
# Get a BMesh representation
bm = bmesh.from_edit_mesh(me)
bm.faces.active = None
pointsList=[]
for v in bm.verts:
    if v.select:
        # print(v.co)
        coords = str(tuple(v.co))
        coords = re.sub('[(),]', '', coords)
        pointsList.append(coords)
    print(pointsList)

pointsCount = len(pointsList)
print(pointsCount)



with open(outputFile,'w') as of:
    header = str('# vtk DataFile Version 3.0\nvtk output\nASCII\nDATASET POLYDATA\nPOINTS %d float\n' %pointsCount) 
    of.write(header)
    for point in pointsList:
        of.write(point +'\n')
# file.close()





def create_boundary(obj): #this works well - makes boundary, parents to attachment area area

name = ""

#Do I need to deselect all here, and then make this object active? or is it enough to just have the obj argument?
#Do I need to make the object active? or is it fine with the input argument? #Test!
name = obj.name

# keep track of objects in scene to later rename new objects
scn = bpy.context.scene
names = [ obj.name for obj in scn.objects]


bpy.ops.object.mode_set(mode = 'EDIT')
bpy.ops.mesh.select_all(action='SELECT')


#select outer loop, duplicate, separate
bpy.ops.mesh.region_to_loop()
bpy.ops.mesh.duplicate()
bpy.ops.mesh.separate(type='SELECTED')

bpy.ops.object.mode_set(mode = 'OBJECT')
bpy.ops.object.select_all(action='DESELECT') 


new_objs = [ obj for obj in scn.objects if not obj.name in names]

#rename new object and select and make active
for obj in new_objs:
    obj.name = name + " boundary"
    obj.data.name = obj.name #set mesh name to object name
    obj.select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[name]
    bpy.data.objects[name].select_set(True)
    bpy.ops.object.parent_set(keep_transform=True) #parents new loop to the attachment area - need to double check that the transforms are all global 
    bpy.context.view_layer.objects.active = bpy.data.objects[name + " boundary"]
return obj








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


def main_loop():
    
    #[ADD SELECTION OF ALL OBJECTS!]
    for obj in bpy.context.selected_objects:
        if obj.type == 'EMPTY':
            muscle_name=obj.name
            children = []
            children = obj.children
            for obj in children:
                if "origin" in obj.name:
                    #need to maybe deselect all, then select this object, and make active?
                    create_boundary(obj) #makes boundary and sets boundary as active object



                

                # elif "insertion" in obj.name:
                #     create_boundary()
                #     #parent boundary to empty
                #     for "boundary" in obj.name:
                #         reorder_coords()
                #         export_coords()

                elif "volume" in obj.name:
                """export as .stls - make sure that the orientations for export are the same as in the scene!!!"""

        if "boundary" in obj.name 
                reorder_coords(obj) 
                export_coords(obj) 


                # else:
                # print("Unproper naming of children. The following object will be ignored: "+obj.name)  

main_loop()





