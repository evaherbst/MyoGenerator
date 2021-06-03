# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 12:47:46 2021

@author: evach
this script enables generation of muscle empties. 
These can then be used as parents for muscle origins and insertions, 
to run the Niva_Muscle_Analyzer script
"""
import bpy


def make_muscle_empties():
	#enter your list of muscles here
	muscle_List = ["mPT", "mLPt", "mPPt","mPSTs", "mPSTp", "mAMEP", "mAMEM", "mAMES", "mAMP", "mDM"]
	for i in muscle_List:
		print(i)
		o = bpy.data.objects.new(i, None)
		bpy.context.scene.collection.objects.link( o )
	  # empty_draw was replaced by empty_display
		o.empty_display_size = 2
		o.empty_display_type = 'PLAIN_AXES'   
		 

#make_muscle_empties()

