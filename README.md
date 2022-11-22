#  MyoGenerator Blender Add-On
Blender add-on to create volumetric muscles   
*created by Eva C. Herbst and Niccolo Fioritti*  
Note that this add-on has been tested and works on v. 2.91.0 - 2.93.0 of Blender. Older or newer versions may break the code.


:pencil:  Please read our [paper](https://doi.org/10.1098/rsos.220519), which we wrote with Luke E. Meade, Stephan
Lautenschlager, and Torsten M. Scheyer. If you use this method, please cite our paper (Herbst et al. 2022) and the doi of the most recent Github release:
[![DOI](https://zenodo.org/badge/355606184.svg)](https://zenodo.org/badge/latestdoi/355606184)

:video_camera: A video tutorial can be found on [Dryad](doi.org/10.5061/dryad.qjq2bvqk2).

## Note about Release 1.1 
Release 1.1 fixes a small bug. Previously, updating muscle volumes also reformatted data and removed "vector" string for centroids. However, this caused an error when recalculating muscle volumes if "vector" was already removed. Release 1.1 fixes this.

## 

## Output of Add-On
- muscle volume mesh, origin area, insertion area, origin boundary loop, insertion boundary loop
- .csv file with all of the muscle metrics (name, origin area, insertion area, origin centroid, insertion centroid, linear length, muscle length, muscle volume). Linear length is calculated as the Euclidean distance between origin and insertion centroids, muscle length is calculated as the length of the curve of the Blender muscle (sum of edge lengths constituting the curve). Headers are included, and multiple muscles are written to the same file as rows.
- The add-on automatically organizes your muscle components (attachment areas and volume) under an empty whose name is equal to the muscle name.

## Note about Release 1.1 
Release 1.1 fixes a small bug. Previously, updating muscle volumes also reformatted data and removed "vector" string for centroids. However, this caused an error when recalculating muscle volumes if "vector" was already removed. Release 1.1 fixes this.

## 


## Notes for User
- Start with a new Blender file, and import your bone meshes.
- Do not rename the collections. The default Blender collection is named "Collection" and the muscle hierarchies will be created as part of this collection. The bone meshes you import should also automatically be part of this collection.
- Ensure bone meshes are clean (manifold, no intersecting edges and faces) and of suitably high resolution to be able to select attachment areas with the desired precision
- Make sure each bone mesh is one object (not several disconnected meshes - separate out things like sclerotic rings initially). This is necessary because the code relies on duplicating sections and separating them out by loose parts, and so if you have other floating bits in your bone mesh, that will cause issues.
- Ensure that the model in your scene is at the correct scale (i.e. if you took a measurement tool, the resulting dimensions would be correct). This is necessary because the add-on will apply scaling to the muscle areas etc, in other words it assumes the geometry as visible in the scene is the correct dimension. At the beginning of the add-on, the scale, rotation, and location of all objects is applied (setting scale = 1, and rotations and locations = to 0).
- Ensure that your face orientation (e.g. normals) is correct. You can check this by selecting Overlay > Geometry > Face orientation. You can change normals in Edit Mode with Mesh > Normals > Recalculate outside
- Make sure a continuous area is selected for your muscle attachments (no accidental unselected faces in the general attachment area, no faces only connected to other faces by single vertex)
- For attachment select, we recommend using the lasso tool, which can be accessed by left clicking on the select box and selecting the lasso tool
- Note that attachment areas, centroids, boundaries, and muscle curve lengths are calculated during the muscle creation. Therefore, excessive changes to the muscle structure after meshing and joining the muscle may result in a mistmatch between the original attachments and curve length and the final muscle. We therefore recommend to model the muscle as accurately as possible, and if attachment areas are used in analysis, to check afterwards whether the final muscle corresponds to the initially selected areas (a good rule of thumb is to not change the attachment vertices through proportional editing and sculpting). To enable muscle anatomy adjustments after muscle meshing while maintaining the initial curvature and attachment, our method creates a muscle mesh that consits of edge loops that can easily be selected to adjust cross sections via scaling without changing the central curvature of the muscle or the origin and insertion areas.
- *Do not click the next buttons too quickly!* The code needs time to run before the next step can happen. This is especially the case if you get an error with the "duplicate" function context being incorrect when pressing "create muscle curve" too quickly after "match attachment vertex counts". So please do not click these buttons too quickly in a row - if the error comes up re-pressing "create muscle curve" has worked successfully to solve it, or restrat.
- *Do not reformat your csv file in Excel until everything is finalized. You can reformat it to view data, but do not save this reformatted version, because then the program will try to write to write the muscle metrics to this reformatted file, which breaks the data structures.*
- All objects must be visible for the muscle volume updating to work!


## Summary of Add-on Steps

![AddOn](https://github.com/evaherbst/MyoGenerator/blob/main/Myogenerator_Addon_Fig_lowres.png)

1. User enters folder and file name for saving data.
2. User enters muscle name
3. Code creates empty with that muscle name
4. User selects bone on which muscle originates
5. Bone becomes active object, code switches to edit mode
6. User draws on muscle origin by selecting faces, submits 
7. Code duplicates these faces, separates from bone to create new object representing attachment area, renames this object as “[muscle name] origin”. Then, code selects outer edges, duplicates, makes new object to create boundary loop of attachment, renames this as “[muscle name] origin boundary”. Objects are parented to muscle empty.
8. Repeat steps 4-6 for insertion
9. Code matches counts in boundary loops
10. Curve is created by making a nurbs path between the centroids of the origin and insertion attachment sites. Curve is beveled with the origin boundary loop as a cross section. To do so, the origin boundary loop is first duplicated and reoriented so that the largest dimensions are aligned with the XY plane, so that it maintains most of its shape when projected into 2D, then this reoriented loop is converted to a curve. This reorientation ensures that regardless of the mesh orientation in space, the bevel shape remains the same. The curve template has 5 points: beginning and end points at centroids of origins and insertion, 2 points along average normal of origin and insertion (1 per attachment, at a distance of .2L from centroid, where L is linear distance between centroids), and a 5th point between the points along the normals.
11. *If necessary*, the user mirrors the cross section to match the origin. Mirroring is only *sometimes* required (the code reorients the origin boundary to the XY plane (see above) and depending on the position of the origin boundary in global space, sometimes the cross section is mirrored during this reorientation). **Note: Steps 10-14 can be done in any order, and iterative adjustments in the tilt, bevel, and curvature can be made until the curve is finalized in step 17.
12. The user adjusts tilt of curve, making sure the cross section shape aligns with the origin shape.
13. User adjusts bevel extent (goal is to have the end loops of curve volume lined up with origin and insertion so that the vertices can be connected with new faces without any intersections).  
14. User adjusts points of curve to get desired curvature (do not move endpoints!)
15. Code converts curve to mesh
16. User scales edge loops to get muscle shape (e.g. taper or expand insertion, change muscle belly size, etc). If the insertion does not have a similar size and shape to the origin this is especially important, since we need to match the insertion end of the muscle tube template to the actual insertion so they can be bridged nicely. Muscle size and shape adjustments can be done quite nicely by selecting an edge loop (select one edge, then go to Select > Edge loop, or use ALT + RMB) and then using [proportional editing](https://docs.blender.org/manual/en/latest/editors/3dview/controls/proportional_editing.html). 
17. Code joins muscle curve volume and boundary loops, bridges edge loops, duplicates origin and insertion areas, joins with muscle curve volume to cap ends, removes duplicate edges at join seams, renames to “[muscle name] volume”. Code also removes T-junctions (created from resampling boundary loops and then merging with original areas).
18. Code resets add-on so that user can create new muscle.
19. User can adjust muscle meshes iteratively - e.g., once a second muscle is made, the first muscle belly can be scaled to meet the second muscle, etc.
20. Code calculates volumes of all muscles in scene, adds metric to .csv file. Volumes can be updated at any point. If you change a muscle (e.g. scale the muscle belly etc), click "calculate volumes" again and the volumes in your .csv file will update
21.  **Extra steps if your muscle has a very flat attachment (I.e. muscle is more parallel rather than perpendicular to bone) and you are unable to line up boundary loops:**
  - Make sure bevel goes all the way to the end on the side of the muscle that has the flat attachment.
  - *If you can still align one end nicely:* perform all steps including “join muscle”. This will result in one nice end and one messy one. Now go and delete the vertices up to the edge loop where you ended your muscle volume to get rid of messy geometry. Then, select this edge loop (select one edge, then go to Select > Edge loop, or use ALT + RMB) and then press F to cap the end. Move and scale the end so that the muscle end intersects completely with the bone. Preferably, don’t let it point out the other side. If it does, make sure that piece is separate from the actual muscle mesh you want to keep (not connected around the side of the bone). Once the muscle end completely intersects the bone, recalculate your normals (they might have gotten flipped in the process) by selecitng all vertices, Mesh > Normals > Recalculate Outside. Then, in object mode, with the muscle active, go to to modifiers > Boolean > Boolean Difference. Select the bone with the eyedropper tool in the “object” field. Click apply. If there is a piece of muscle mesh that jutted out the other side of the bone, delete this in edit mode. 
  - *If both ends are “flat”:* perform all steps except “join muscle”. Then perform steps listed above, starting with selecting the open end loops and filling them. 
  - *In both cases*: You will probably end up with many sided faces where the two objects intersected. We recommend triangulating the mesh to get even triangles (can also test "merge by distance" as long as geometry is not altered too much, same goes for remeshing methods).

**Note:** If you aligned the muscle nicely with the bevels and curvature there should not be any issues with messy geometry (e.g. edges crossing each other). However, if you have a very tight curve in your muscle, or if you used Boolean difference operations, you could end up with messy geometry. Using Mesh > Clean Up > Merge by distance and playing around with the slider can help clean this up, but be careful because it can smooth over some of the geometry. You can also use Voxel remeshing or FloodFill in Sculpt mode to get a better mesh (since the Boolean intersection operation can result in faces with different number of edges). Again, ensure that the remeshing is not overly smoothing your geometry.

 
## Add-on Installation
 
 The add-on currently works for versions 2.91.0 - 2.93.0. Blender can be installed [here](https://www.blender.org/).
 
 To install the add-on, download this repository, extract all, zip the Add-on folder, and then follow the instructions [here](https://docs.blender.org/manual/en/latest/editors/preferences/addons.html), selecting the zipped Add-on Folder
 
 ## Troubleshooting Errors
 
 - Note that you need to close the .csv file with the muscle metrics before more information can be written to it. Otherwise you will get an error.
 - If you do not have permissions to write and read and edit files in the folder you designated, this will throw an error. This could be a problem in university settings where researchers do not always have admin accounts (although for some of us it has worked without admin rights, so it probably depends on the exact permissions you have). We recommend testing on another computer with admin rights if possible or contacting your IT department. 
 
## Notes about File Management
- It is possible to work on a Blender muscle file, save, then open in another computer and update volumes (tested 15.11).
- Note that if working on several muscle models, make sure the folders that the data is saved to have distinct file names (the same file name should technically be possible if saving in different folders, but this is not recommended, because your file name should include specifics of the model that the muscle metrics were obtained from=.
