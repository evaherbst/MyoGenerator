#  Muscle_Volume_Sculptor
 Blender add-on to create volumetric muscles 
 
 
## NOTES FOR USE:** 
- Ensure bone meshes are clean (manifold) and of suitably high res to be able to select attachment areas with the desired precision
- Before entering the muscle name, make sure an object in the scene (does not matter which one) is selected. Otherwise you will get the error:
RuntimeError: Operator bpy.ops.object.mode_set.poll() failed, context is incorrect**
- Make sure a continuous area is selected for your muscle attachments (no accidental unselected faces in the general attachment area, no faces only conected to other faces by single vertex)
- For attachment select, we recommend using the lasso tool, which can be accessed by left clicking on the select box and selecting the lasso tool
- Ensure meshes are clean (manifold) and of suitably high res to be able to select attachment areas with the desired precision


## Summary of Add-on Steps**

1. User enters muscle name
2. Code creates empty with that muscle name
3. User selects bone on which muscle originates
4. Bone becomes active object, code switches to edit mode
5. User draws on muscle origin by selecting faces, submits 
6. Code duplicates these faces, separates from bone to create new object representing attachment area, renames this object as “[muscle name] origin”. Then, code selects outer edges, duplicates, makes new object to create boundary loop of attachment, renames this as “[muscle name] origin boundary”. Objects are parented to muscle empty.
7. Repeat steps 4-6 for insertion
8. Curve is created by making a nurbs path between the centroids of the origin and insertion attachment sites. Curve is beveled with the origin boundary loop as a cross section (origin boundary loop is first duplicates and reoriented so that it maintains most of its shape when projected into 2D 
9. The curve template has 5 points - beginning and end at centroids of origins and insertions , then points along average normal of origin and insertion, at a distance of .2L from centroid, where L is linear distance between centroids. The 5th point is generated between the points along the normals.
10. The user adjusts tilt of curve, making sure the cross section shape aligns with the origin shape.
11. User adjusts points of curve to get desired curvature (do not move endpoints!)
12. User adjusts bevel extent (goal is to have the end loops of curve volume lined up with origin and insertion so that the vertices can be connected with new faces without any intersections). 
13. Code converts curve to mesh
14. User scales edge loops to get muscle shape (e.g. taper or expand insertion, change muscle belly size, etc)
15. Code joints muscle curve volume and boundary loops, bridges edge loops, duplicates origin and insertion areas, joins with muscle curve volume to cap ends, removes duplicate edges at join seams, renames to “[muscle name] volume”
16. Extra steps if your muscle has a very flat attachment (I.e. muscle is more parallel rather than perpendicular to bone) and you are unable to line up boundary loops.
  - Make sure bevel goes all the way to the end on the side of the muscle that has the flat attachment.
  - *If you can still align one end nicely:* perform all steps including “join muscle”. This will result in one nice end and one messy one. Now go and delete the vertices up to the edge loop where you ended your muscle volume (see SI Figure #) to get rid of messy geometry. Then, select this edge loop (add instructions) and press F to cap the end. Move and scale the end so that the muscle end intersects completely with the bone. Preferably, don’t let it point out the other side. If it does, make sure that piece is separate from the actual muscle mesh you want to keep (not connected around the side of the bone). Once the muscle end completely intersects the bone, with the muscle active, go to to modifiers > Boolean > Boolean intersection. Select the bone with the eyedropper tool in the “object” field. Click apply. If there is a piece of muscle mesh that jutted out the other side of the bone, delete this in edit mode. 
  - *If both ends are “flat”:* perform all steps except “join muscle”. Then perform steps listed above, starting with selecting the open end loops and filling them. 





**adjusting muscle tilt:**
Tab (to get to edit mode) - A to select all points - Item > Mean Tilt


 
# Niva Muscle Analyzer
 This add-on exports muscle metrics 
 Note that for this add-on to work, muscles need to follow a specific naming system and parent-child hierarchy. 
 This naming and hierachy are automatically generated when using the Muscle_Volume_Sculptor add-on.
 If using only the Niva Muscle Analyzer in isolation, make sure that each muscle is grouped and named as follows:
 ![alt text](https://github.com/evaherbst/-Muscle_Volume_Sculptor/blob/main/example_Blender_hierarchy_image.PNG)
 
# Add-on Installation
 
 The add-on currently works for versions 2.91.0 - 2.93.0. Blender can be installed [here](https://www.blender.org/).
 
 To install the add-on, download the Add-on Folder from this repository (make sure it is zipped) and then follow the instructions [here](https://docs.blender.org/manual/en/latest/editors/preferences/addons.html).
 
 Please 
