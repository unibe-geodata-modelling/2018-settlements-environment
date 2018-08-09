Read Me Topographic Position Index Analysis

***********************************************************************************************************************
Variables "myworkspace", "dem", "Settlements", "Lakes", "Buffer500" to "Buffer5000", "interland500" to "interland 500",
"classif200land", "SumBuffLand500" to "SumBuffLand5000" and "LandStats500" to "LandStats5000" (several lines):
***********************************************************************************************************************

For the TPI analysis you have to adjust the variable "myworkspace" (line 15) to your chosen workspace.

The "dem" variable (line 20) is where you read in your DEM. There you have to adjust the path to the directory where your
DEM is stored.

The settlement shapefile is read in on line 85. You have to adjust the path to where you have saved your settlement shapefile.

The lake shapfile is read in on line 93. You have to adjust the path to where you have stored your lake shapefile.

The "classif200land" variable (line 96) is used as the output of the erase function. You have to adjust
the path to your chosen directory.

"Buffer100" to "Buffer5000" (lines 107 to 109): These are the variables for the buffers you set around your settlements. You can adjust the path
to your chosen directory. Since it is no final result you can also use a temporary directory.

The variables "interland500" to "interland5000" (lines 127 to 129) are the variables that are used as the ouptut path of the intersect function.
You can adjust the path to your chosen directory. Since it is no final result you can also place it in a temporary directory.

Variables "SumBuff500" to "SumBuff5000" (lines 177 to 179): Sometimes in one buffer the same landform can appear in several separated polygons. 
These variables are later used as the output path in the function that combines these separated polygons.
You can adjust the path to your chosen directory. Since it is no final result you can also place it in a temporary directory.

Variables "LandStats500" to "Landstats5000" (lines 188 to 190): These variables are later used as the output path of the statistical analysis function 
where the mean and standard deviation is calculated (see also lines 195 to 197).


*************************************************
Cell size and extention setting (lines 20 and 23)
*************************************************

On the lines 20 to 23 you do not have to change anything. Here the cell size, the extent and the newly produced rasters made during the script
are set to the extent and cell size of the DEM.


***********************************************************************************************************************************
Focal Statistics Function - calculating the mean and standard deviation of the surrounding cells of the DEM Raster (lines 32 to 37)
***********************************************************************************************************************************

To determine the TPI you need the mean elevation of the surrounding cells as well as the standard deviation derived from the DEM.
On line 32 the mean is determined and on line 36 the standard deviation. For both you just have to adjust the output path (second input in the brackets), to your chosen
directory. On the lines 33 and 37 you read in the newly created mean and standard deviation file. You have to adjust the path to where you have saved
them in the functions from the lines 32 and 36.


************************************
The slope function (lines 45 and 46)
************************************

For the slope function you only have to adjust the path where you want to save the result (second input into the bracket on line 45) and use the same path for line
46 to read in the newly created slope raster. The slope is given in degrees, you should not change that since this is important for the classification of the
different landforms later on.


**************************************************************************
Getting the TPI and 0.5 STD Raster for the classification (lines 54 to 61)
**************************************************************************

The TPI is simply the difference between the DEM and the mean elevation raster that was determined on the lines 32-37.
You do not have to change anything of the equation on the line 54. On Line 55 you save the result from line 54. Here you
can adjust the path to your chosen directory and on line 56 you have to use the same path to read in the newly created raster.

In the classification (lines 64 to 68) half the value from the standard deviation raster (created on the lines 36 to 37) is used several times. To make the writing 
of the classification a bit easier, a separate raster is created for this instead of dividing the standard deviation in the classification itself.
This is done on the line 59 and on line 60 the new raster is saved. You can adjust the path to your chosen directry. This command creates an exit code in pycharm.
However, it works in the Python console in ArcGIS or in other IDEs.
On line 61, which works again in Python, you read in the newly created raster. You have to adjust the path to where you have saved your raster from line 60. 


*****************************************************************
Landform classification - Conditional Evaluation (lines 64 to 68)
*****************************************************************

Weiss (2001) suggested in his poster presentation six classifications for the landforms which are displayed on line 64. On line 64 a conditional statement is used for the 
classification, and on line 65 you would save the newly classifeid raster. However, as with the half standard deviation raster this creates an exit code in Pycharm. It works 
again in the Python console in ArcGIS or with other IDEs. In any case, on line 65 you have to adjust the output path to your chosen directory.
On line 68, which works again in Python, you read in the newly created raster. You have to adjust the path to where you have saved your raster from line 65. 


************************************************
Resample the classified Raster (lines 76 and 77)
************************************************

The classified Raster has to be converted into a shapefile for later use for the intersect function. In this case the raster first had to be resampled into a 
coarser resolution. With the original 10x10 m cell size the output shapefile from the function "raster to polygon" would have exceeded the size of 2 GB which creates
an error. Another workaround would be to save the polygon in a geodatabase. You can skip this step/ put a # before these command lines if you already have a coarser 
resolution that does not lead to a shapefile of that size. If you do not skip this step you have to adjust the path on line 76 (second input in the bracket of the function)
to your chosen directory and use the same path on line 77 to read in the newly created coarser raster. Furthermore, you can adjust the new cell size, which is the second last input in 
the bracket of the function. In this case 200 200 was chosen -> a resolution of 200x200 m.

If you skip this step you have to be aware that you have to put in the variable "classification" and not "classification200" on line 82 as the first input into the brackets.


**************************************************************
Convert the classified raster to a shapefile (lines 81 and 82)
**************************************************************

To use the different landform classes in the intersect function you have to transform the raster to a polygon shapefile. On line 81 the variable for
the new shapefile is prepared, here you have to adjust the path to your chosen directory. For the function itself, line 82, you do not have to change
anything unless you skiped the resample function from the lines 76 and 77. If you have done that you need to replace the variable "classification200"
with the varaibale "classification" in the brackets of the function.


***************************************************************************
Erase function to extract the lakes from the classified landforms (line 99)
***************************************************************************

This function is used to erase the lakes from the classified landform shapefile, so that they can not influence the end results.
You do not need to change anything here.


*********************************************************************************
Buffer function and add geometry to the buffer attirubte table (lines 112 to 119)
*********************************************************************************

Here you can adjust the distance of the buffer/s. In this example 500, 1000 and 5000 meters radii were used. If you want other distances just exchange the number
on the input "500 Meters" or any other of the distances you want to change. If you want fewer buffers, you can simply delete the rows with the distances you do not
want or put a # before the lines. If you do that, you have to do that for every following command.

You do not have to change anything for the "add geometry" function (lines 117 to 119). The results will be automatically saved in a newly created field named "POLY_AREA".


*************************************
Intersect function (lines 132 to 134)
*************************************

No adjustments are needed for this function.


***********************************************************************
Add field "Percent" and add geometry Attribute "Area"(lines 142 to 149)
***********************************************************************

The added area from the "add geometry" function will be automatically saved in a newly created field "POLY_AREA" and you do not have to adjust anything for
these two lines.


*******************************************************************
Getting the area of the buffers in square meters (lines 153 to 166)
*******************************************************************

Here you only have to change something if you have chosen other buffer distances than in the original script. If you have done that, you have to write down
the correct amount of sqaure meters for your buffer distance which is displayed in the console via print (Area...m).


********************************************************************************************************************************************
Calculating the percentage of the different polygons (=landforms) of the classified landform shapefile inside the buffers (lines 170 to 172)
********************************************************************************************************************************************

Here you only have to adjust something if you have chosen other buffer distances. If you have done that you have to divide the field "POLY_AREA" by the correct amount of square meters
for your buffer distance. See also just above under "Getting the area of the buffers in sqaure meters (lines 153 to 166)".


*****************************************************************************************
Statistichs analysis - Summarizing the polygons with the same landform (lines 182 to 184)
*****************************************************************************************

The function "arcpy.Statistics_analysis() is used to summarize the same landform classes (along with their percentages of land coverage in the buffer area) per settlement, because sometimes the same
landform can appear several times in the same buffer.
You have to change the last field name of the last input in the bracket. In this case the field name for the settlement names was "Fundort". You have to replace this with your correspondending field name. 
The field name "GRIDCODE" does not need to be changed since this field was automatically created with the classified raster and has therefore always the same name.



*************************************************************************************************************
Statistics  analysis - Calculating the mean land coverage per settlment/buffer per landform (line 194 to 197)
*************************************************************************************************************

The function "arcpy.Statistics_analysis() is used to calculate the mean percantage of land coverage of the individual landforms per settlement/buffer.
However, the mean percentage is not determined over all settlements/buffers. If a landform e.g. only appears in 5 settlements the percentage shows the mean coverage
of this landform for those 5 settlements and not for all 56.
You do not need to change anything here.


**********************************
**********************************

When you have run the script you have four dBase files (one per buffer distance) with the frequency and mean land coverage in percent per landform class
per buffer.

The visualisation itself was done in Excel.

Lines that are not commented on in this ReadMe do not need to be adjusted.


**********
Literature
**********

Weiss, A.D. (2001). Topographic Position and Landforms Analysis. Poster presentation, ESRI User Conference, San Diego, CA.