#update local axes so Z = normal of face


#initially, go into transform orientation edit:
bpy.context.scene.tool_settings.use_transform_data_origin = True



#then, once local axes adjusted, leave transform orientation edit:
bpy.context.scene.tool_settings.use_transform_data_origin = False
