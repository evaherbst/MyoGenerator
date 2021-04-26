
"""
Muscle Analyzer for Blender Files
@author: Eva C. Herbst and Niccolo Fioritti 
Extracts muscle metrics (origin area, insertion area, length, volume) from a Blender file.
Saves as .csv file, which can be imported into Excel to create table where row headers = muscle names, column headers = metrics.

NOTE: for muscle modeling paper, export list with both 3D modeled volume and frustum to compare

NOTE: also want to add in correction factor/option to add in pennation angle if known? Or tell people to add in the calculations later/just publish the volume metrics and not the force etc?

"""

import bpy
import math
from math import sqrt
import bmesh
import os
import csv
import re

# center all origins on the geometry of the object so that location = center of mass
def object_Recenter():
  bpy.ops.object.select_all( action = 'SELECT' )
  bpy.ops.object.origin_set( type = 'ORIGIN_GEOMETRY' ) #need to set origin to geometry, otherwise all muscles will still have same origin as bone


#calculate muscle attachment 
def get_attachment_area(obj):
    
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)  #set scale and rotation = 1 to get correct volume values and apply other transforms, do not set location to 0 because we want object origin set to geometry
    objName=obj.name 
    me = obj.data #get mesh of object
    me.name=objName
    # Get a BMesh representation
    bm = bmesh.new()# create an empty BMesh
    bm.from_mesh(me)# fill it in from a Mesh
    print(objName + " Area")
    area = sum(f.calc_area() for f in bm.faces)
    #bm.clear()
    print(area)
    return area
        


def measure_muscle_volume(obj):
    bpy.ops.object.transform_apply(location = False, scale = True, rotation = True) #set scale and rotation = 1 to get correct volume values and apply other transforms, do not set location to 0 because we want object origin set to geometry
    objName=obj.name 
    me = obj.data
    # Get a BMesh representation
    bm = bmesh.new() # create an empty BMesh
    bm.from_mesh(me) # fill it in from a Mesh
    # triangulate prior makes the difference
    bmesh.ops.triangulate(bm, faces=bm.faces)
    print("Volume")
    volume = bm.calc_volume()
    print(volume)
    return volume

# calculate the muscle length (= distance between the center of mass of the muscle origin and insertion)
# def get_muscle_length(attachment_list):
#     l = []
#     if (isinstance(attachment_list,list)):
#       for item in attachment_list:
#           l.append(item.location)
#       length = sqrt( (l[0][0] - l[1][0])**2 + (l[0][1] - l[1][1])**2 + (l[0][2] - l[1][2])**2)
#       print("Muscle Length")
#       print(length)
#       return length
#     else:
#       print("attachment list needs to be a list")
#       return ("MISSING VALUE")
   

# def vector_to_coord(centroid): #convert from format "Vector <(X,Y,Z)>"" to "(X,Y,Z)"
#   centroid = str(tuple(centroid)) #convert to string
#   centroid = re.sub('Vector', '', centroid) #remove "vector" 
#   return centroid

def main_loop():
  bpy.ops.object.mode_set(mode = 'OBJECT')
  bpy.ops.object.select_all(action='SELECT')
  bpy.ops.object.transform_apply(location = False, scale = True, rotation = True) #set scale and rotation = 1 to get correct volume values and apply other transforms, 
  # do not set location to 0 because we want origin centered based on geometry
  #or add code to make sure all calculations are in global coordinates?
  complete_Muscle_List = []
  complete_Muscle_List_Frustum = []
  muscle_Data = [] #create a list to store muscle data
  muscle_Data_Frustum = []
  attachment_list = [] #create a list of origin and insertion objects
  origin_area=0
  insertion_area=0
  muscle_volume=0
  muscle_length=0
  origin_centroid=0
  insertion_centroid=0
  for obj in bpy.context.selected_objects:
    if obj.type == 'EMPTY':
      muscle_name=obj.name
      children = []
      children = obj.children
      for obj in children:
        if "origin" in obj.name:
          origin_area=get_attachment_area(obj) 
          attachment_list.append(obj)
          origin_centroid=obj.location
          origin_centroid_coords=origin_centroid[:]
          #origin_centroid_coords=str(tuple(origin_centroid))
          #origin_centroid_coords=re.sub('Vector<>', '', origin_centroid_coords)
        elif "insertion" in obj.name:
          insertion_area=get_attachment_area(obj) 
          attachment_list.append(obj)
          insertion_centroid=obj.location
          insertion_centroid_coords=insertion_centroid[:]
          #insertion_centroid_coords=str(tuple(insertion_centroid))
          #insertion_centroid_coords=re.sub('Vector<>', '', insertion_centroid_coords)
        elif "volume" in obj.name:
          muscle_volume=measure_muscle_volume(obj)
        else:
          print("Unproper naming of children. The following object will be ignored: "+obj.name)  
      muscle_length=math.sqrt((insertion_centroid[0] - origin_centroid[0]) ** 2 + (insertion_centroid[1] - origin_centroid[1]) ** 2 + (insertion_centroid[2] - origin_centroid[2]) ** 2)
      frustum_volume=(muscle_length/3)*(origin_area + insertion_area + math.sqrt(origin_area * insertion_area))
      CSA=(frustum_volume)/(muscle_length)
      force_newtons=(0.3)*(CSA)
      #muscle_Data = [muscle_name, origin_area, origin_centroid_coords, insertion_area, insertion_centroid_coords, muscle_length, muscle_volume]
      muscle_Data_Frustum = [muscle_name, origin_area, origin_centroid_coords, insertion_area, insertion_centroid_coords, muscle_length, frustum_volume, CSA, force_newtons]
      #print(muscle_Data)
      #complete_Muscle_List.append((muscle_Data))
      complete_Muscle_List_Frustum.append((muscle_Data_Frustum))
      #print(complete_Muscle_List)
      export(complete_Muscle_List_Frustum)

def export(complete_Muscle_List):
  filepath = bpy.data.filepath
  main_path = os.path.dirname(filepath)
  suffix = '.csv'
  name = 'muscle_metrics_Macrocnemus_April26_frustum'
  print("writing to: " + main_path)
  outputFile = os.path.join(main_path, name) + suffix
  #header = [['muscle_name', ' origin_area', ' origin_centroid', ' insertion_area', ' insertion_centroid', ' length', ' volume']]
  header = [['muscle_name', ' origin_area', ' origin_centroid', ' insertion_area', ' insertion_centroid', ' length', ' frustum_volume', ' CSA', ' force_newtons']]
  with open(outputFile, "w", newline='') as f:
      writer = csv.writer(f)
      writer.writerows(header)
      writer.writerows(complete_Muscle_List)
  return(name)

object_Recenter()
main_loop()

















