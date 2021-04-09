# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 13:36:03 2021

@author: utente
"""

"""
TXT TO VTK FILE EXPORTER
"""


import re

filename = 'exported_coord.txt'

converted = 'converted.vtk'


pointsList=[]


with open (filename) as file:
    
   
    
    pointsCount =0
    for x in file:
        x=x.rstrip()
        x = re.sub('[(),]', '' , x)
       
        pointsList.append(x)
       
  
    
with open(converted,'w') as c:
    pointsCount=len(pointsList)   
 
    header =str('# vtk DataFile Version 3.0\nvtk output\nASCII\nDATASET POLYDATA\nPOINTS %d float\n' %pointsCount)
    c.write (header)
    for point in pointsList:
        c.write(point +'\n')
    
   # print(pointsCount)
   # file = re.sub('[()]', '' , file)
