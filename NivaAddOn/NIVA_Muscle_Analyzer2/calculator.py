
# -*- coding: utf-8 -*-
# pylint: skip-file
import bpy
from math import sqrt
import bmesh
import os
import csv

class MainCalculator():

    def __init__(self,targetPath,newFileName):
        self.targetPath =''
        self.newFileName=''
    
    # center all origins on the geometry of the object so that location = center of mass
    def object_Recenter():
    
        bpy.ops.object.select_all( action = 'SELECT' )
        bpy.ops.object.origin_set( type = 'ORIGIN_GEOMETRY' )


    #calculate muscle attachment 
    def get_attachment_area(obj):
        
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)  #set scale = 1 to get correct area values
        objName=obj.name 
        me = obj.data
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
        bpy.ops.object.transform_apply(location = False, scale = True, rotation = False) #set scale = 1 to get correct volume values
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
        #bm.clear()

    # calculate the muscle length (= distance between the center of mass of the muscle origin and insertion)
    def get_muscle_length(attachment_list):
        l = []
        if (isinstance(attachment_list,list)):
            for item in attachment_list:
                #print(item)
                l.append(item.location)
            length = sqrt( (l[0][0] - l[1][0])**2 + (l[0][1] - l[1][1])**2 + (l[0][2] - l[1][2])**2)
            print("Muscle Length")
            print(length)
            return length
        else:
            print("attachment list needs to be a list")
            return ("MISSING VALUE")



    
    def export(complete_Muscle_List, outputPath, fileName):
  
        fileNameConv = fileName+'.csv'
        main_path = os.sep.join([outputPath, fileNameConv])
        print("writing to: " + main_path)
        outputFile=main_path
        #os.mkdir(outputFile)
        header = [['muscle_name', ' origin_area', ' insertion_area', ' length', ' volume']]
        with open(outputFile, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(header)
            writer.writerows(complete_Muscle_List)


    def main_loop(self):
        print(self.targetPath + " SAVINGPATH")
        complete_Muscle_List = []
        muscle_Data = [] #create a list to store muscle data
        attachment_list = [] #create a list of origin and insertion objects
        origin_area=0
        insertion_area=0
        muscle_volume=0
        muscle_length=0
        for obj in bpy.context.selected_objects:
            print(obj)
           # if obj.type == 'EMPTY':
            if obj.type == 'EMPTY':
                muscle_name=obj.name
                print("enteredLoop")
                print(muscle_name)
                children = []
                children = obj.children
                for obj in children:
                    if "origin" in obj.name:
                        origin_area=self.get_attachment_area(obj) 
                        attachment_list.append(obj)
                    elif "insertion" in obj.name:
                        insertion_area=self.get_attachment_area(obj) 
                        attachment_list.append(obj)
                    elif "volume" in obj.name:
                        muscle_volume=self.measure_muscle_volume(obj)
                    else:
                        print("Unproper naming of children. The following object will be ignored: "+obj.name)  
                muscle_length=self.get_muscle_length(attachment_list)
                #muscle_Data.extend((muscle_name, origin_area, insertion_area, muscle_length, muscle_volume))
                muscle_Data = [muscle_name, origin_area, insertion_area, muscle_length, muscle_volume]
                print(muscle_Data)
                complete_Muscle_List.append((muscle_Data))
                print(complete_Muscle_List)
                self.export(complete_Muscle_List,self.targetPath,self.newFileName)
    

