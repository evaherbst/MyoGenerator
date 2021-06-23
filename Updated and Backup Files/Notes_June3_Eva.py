# Once you have origin and insertions with same numbers, need to select origin

# duplicate

# rename to Muscle + "Volume"

# array modifier

# have user make adjustments

# apply array modifier

# duplicate insertion loop, rename as Muscle + "insertion boundary duplicate"

#deselect all

# select "[Muscle] insertion boundary duplicate" and "[Mucle] + volume"

# join
bpy.ops.object.join()

# edit mode, select all

bpy.ops.object.mode_set(mode = 'EDIT')
bpy.context.tool_settings.mesh_select_mode = (True, False, False) #vertex select mode
bpy.ops.mesh.select_all(action='SELECT')

#bridge edge loops
bpy.ops.mesh.bridge_edge_loops()





#RESET ORIGINS OF ARRAY BEFORE USING CURVE MODIFIER:
# set geometric origin of array mesh the muscle origin attachment centroid



import bpy
import mathutils
from mathutils import Vector

obj = bpy.context.active_object

coord = [-1, -1.5, -3]
#trasformare la lista delle coordinate in vettore
#per poter eseguire la sotrazione con le coordinate dell'oggetto
coord = Vector(coord)
offset = coord - obj.location

me = obj.data
#sposto tutti i vertici rispetto all'origine dell'oggetto
for v in me.vertices:
          v.co = v.co - offset

me.update()
#sposto l'oggetto della stessa quantità, ma dalla parte opposta
#così i vertici tornano al loro posto mentre l'origine si è spostata
obj.location = obj.location + offset


#reset transforms for all objects at end again before running muscle analyzer
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True) #set transforms to make sure they are in global CS 
#I checked this, it works on all selected objects!

