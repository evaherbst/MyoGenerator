# pylint: skip-file
import bpy
import os

from bpy.types import Operator
from . calculator import MainCalculator
#from bpy.props import *

class MUSCLE_MEASURE_OT_All_Op(Operator):

    bl_idname = "object.analyze_all"
    bl_label = "Analyze"
    bl_description = "Click here to extract values from selected muscles"

 

    @classmethod
    def poll(cls, context):
        obj = context.object

        if obj is not None:
            if obj.mode =="OBJECT":
                return True
        return False

    def execute(self, context):

        

        scene = bpy.context.scene
        print(bpy.path.abspath(scene.conf_path) + "HERE")
        MainCalculator.targetPath = bpy.path.abspath(scene.conf_path)
        #newCalculator.targetPath = bpy.path.abspath(scene.conf_path)
        fileName = scene.file_name

        #newCalculator = MainCalculator(bpy.path.abspath(scene.conf_path),fileName)

        if(len(fileName)<1):
            self.report({"ERROR"}, "MUSCLE ANALYZER: MISSING_FILENAME")
            return
        else:
            MainCalculator.newFileName=fileName
            MainCalculator.object_Recenter()
            MainCalculator.main_loop(MainCalculator)
            #newCalculator.newFileName=fileName
            #newCalculator.object_Recenter()
            #newCalculator.main_loop()


        self.report({'INFO'}, bpy.path.abspath(scene.conf_path) )
        return{'FINISHED'}