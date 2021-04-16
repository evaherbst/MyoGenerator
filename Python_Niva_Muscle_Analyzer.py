
"""
Muscle Analyzer for Blender Files
@author: Eva C. Herbst and Niccolo Fioritti 
Extracts muscle metrics (origin area, insertion area, length, volume) from a Blender file.
Saves as .csv file, which can be imported into Excel to create table where row headers = muscle names, column headers = metrics.

"""

import bpy
from math import sqrt
import bmesh
import os
import csv

# center all origins on the geometry of the object so that location = center of mass
def object_Recenter():
  
    bpy.ops.object.select_all( action = 'SELECT' )
    bpy.ops.object.origin_set( type = 'ORIGIN_GEOMETRY' )


#calculate muscle attachment 
def get_attachment_area(obj):
    
    bpy.ops.object.transform_apply(location=True rotation=True, scale=True)  #set transforms = 1 to get correct area values and apply other transforms
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
    bpy.ops.object.transform_apply(location = True, scale = True, rotation = True) #set transforms = 1 to get correct volume values and apply other transforms
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
def get_muscle_length(attachment_list):
    l = []
    if (isinstance(attachment_list,list)):
      for item in attachment_list:
          l.append(item.location)
      length = sqrt( (l[0][0] - l[1][0])**2 + (l[0][1] - l[1][1])**2 + (l[0][2] - l[1][2])**2)
      print("Muscle Length")
      print(length)
      return length
    else:
      print("attachment list needs to be a list")
      return ("MISSING VALUE")
   

def main_loop():
  bpy.ops.object.select_all(action='SELECT')
  bpy.ops.object.transform_apply(location = True, scale = True, rotation = True) #set transforms = 1 to get correct volume values and apply other transforms
  complete_Muscle_List = []
  muscle_Data = [] #create a list to store muscle data
  attachment_list = [] #create a list of origin and insertion objects
  origin_area=0
  insertion_area=0
  muscle_volume=0
  muscle_length=0
  for obj in bpy.context.selected_objects:
    if obj.type == 'EMPTY':
      muscle_name=obj.name
      children = []
      children = obj.children
      for obj in children:
        if "origin" in obj.name:
          origin_area=get_attachment_area(obj) 
          attachment_list.append(obj)
        elif "insertion" in obj.name:
          insertion_area=get_attachment_area(obj) 
          attachment_list.append(obj)
        elif "volume" in obj.name:
          muscle_volume=measure_muscle_volume(obj)
        else:
          print("Unproper naming of children. The following object will be ignored: "+obj.name)  
      muscle_length=get_muscle_length(attachment_list)
      muscle_Data = [muscle_name, origin_area, insertion_area, muscle_length, muscle_volume]
      print(muscle_Data)
      complete_Muscle_List.append((muscle_Data))
      print(complete_Muscle_List)
      export(complete_Muscle_List)
 

def export(complete_Muscle_List):
  filepath = bpy.data.filepath
  main_path = os.path.dirname(filepath)
  print("writing to: " + main_path)
  outputFile = main_path + '\muscle metrics.csv' #save output to same folder as blender file
  header = [['muscle_name', ' origin_area', ' insertion_area', ' length', ' volume']]
  with open(outputFile, "w", newline='') as f:
      writer = csv.writer(f)
      writer.writerows(header)
      writer.writerows(complete_Muscle_List)


object_Recenter() 
main_loop()
