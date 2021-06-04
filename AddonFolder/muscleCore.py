# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 12:47:46 2021

@author: evach
this script enables generation of muscle empties. 
These can then be used as parents for muscle origins and insertions, 
to run the Niva_Muscle_Analyzer script
"""
import bpy


def make_empty(Muscle):
	bpy.ops.object.mode_set(mode = 'OBJECT')
	o = bpy.data.objects.new(Muscle, None)
	bpy.context.scene.collection.objects.link( o )
	o.empty_display_size = 2
	o.empty_display_type = 'PLAIN_AXES'   

#make_muscle_empties()

