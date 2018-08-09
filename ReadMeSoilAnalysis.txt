Read Me Soil Suitability Analysis


**********************************************************************************************************************************************
Variables "myworkspace", "Bodeneignungskarte", "settlements", "Bufferzone100_shp" to "Bufferzone5000_shp", "interBoden100" to "interBoden5000",
"SumBuff100" to "SumBuff5000" and "SoilStats100" to "SoilStats5000"
**********************************************************************************************************************************************

For the soil analysis you have to adjust the variable "myworkspace" (line 14) to your chosen workspace. 

The "Bodeneignungskarte" variable (line 21) is where you read in your shapefile of your soil suitablity map. You have to adjust
the path to where you have stored your soil suitability map. 

The "Settlements" variable (line 22) is where you read in your settlement point shapefile. You have to adjust the path to
where you have stored your settlement shapefile.

"Bufferzone100_shp" to "Bufferzone5000_shp" (lines 29 to 32): These are the variables for the buffers you set around your settlements. You can adjust the path
to your chosen directory. Since it is no final result you could also use a temporary directory.

The variables "interBoden100" to "interBoden5000" (lines 58 to 61) are the variables that are used as the output path of the intersect function.  You can adjust the path
to your chosen directory. Since it is no final result you could also use a temporary directory.

Variables "SumBuff100" to "SumBuff5000" (lines 127 to 130): Sometimes in one buffer the same soil suitability can appear in several separated polygons. 
These variables are later used as the output path in the function that combines these separated polygons.
You can adjust the path to your chosen directory. Since it is no final result you could also use a temporary directory.

Variables "SoilStats100" to "SoilStats5000" (lines 145 to 148): These variables are later used as the output path of the analysis function where the mean and standard deviation is determined (lines 154 to 157).
You can adjust the path to your chosen directory.


*******************************************************************************
Buffer function and add geometry to the buffer attirubte table (lines 35 to 49)
*******************************************************************************

Here you can adjust the distance of the buffer/s. In this example 100, 500, 1000 and 5000 meters radii were used. If you want other distances just exchange the number
on the input "100 Meters" or on any of the other distances you want to change. If you want fewer buffers, you can simply delete the rows with the distances you do not
want or put a # before the lines. If you do that, you have to do this for every following command.

You do not have to change anything for the "add geometry" function. The results will automatically be saved in a newly created field named "POLY_AREA".


***********************************
Intersect function (lines 64 to 67)
***********************************

No changes are needed for the intersect function.


*********************************************************************
Add field "Percent" and add geometry Attribute "Area"(lines 75 to 84)
*********************************************************************

The added area from the "add geometry" function will be automatically saved in a newly created field "POLY_AREA" and you do not have to adjust anything for
these two lines.


******************************************************************
Getting the area of the buffers in square meters (lines 92 to 110)
******************************************************************

Here you only have to change something if you have chosen other buffer distances than in the original script. If you have done that, you have to write down
the correct amount of sqaure meters for your buffer distance. The area in square meters is displayed in the console via print (Area...m).


***********************************************************************************************************************************
Calculating the percentage of the different sections/polygons (=different soil suitabilities) inside the buffers (lines 118 to 121)
***********************************************************************************************************************************

Here you only have to adjust something if you have chosen other buffer distances. If you have done that you have to divide the field "POLY_AREA" by the correct amount of square meters
for your buffer distance. See also just above under "Getting the area of the buffers in sqaure meters (lines 92 to 110)".


*****************************************************************************************************************************
Statistics analysis - Summarizing the polygons with the same soil suitability along with their percentages (lines 133 to 136)
*****************************************************************************************************************************

The function "arcpy.Statistics_analysis() is used to summarize the same categories of soil suitabilies (along with their percentages of land coverage in the buffer area) per settlement.
You have to change the field names for the last input in the bracket. In this case the field name for the soil suitability was "Eignungsei" and for the settlement names "Fundort".
You have to replace this with your correspondending field names.


**********************************************************************************************************************************************************
Statistics  analysis - Calculating the mean land coverage and the standard deviation per settlment/buffer per soil suitability category (line 154 and 157)
**********************************************************************************************************************************************************

The function "arcpy.Statistics_analysis() is used to calculate the mean percantage of land coverage per settlement/buffer of the individual soil suitabilities.
However, the mean percentage is not determined over all settlements/buffers. If a category of soil suitability e.g. only appears in 5 settlements the percentage shows the mean coverage
of this soil suitability for those 5 settlements and not for all 56.
On the last input in the bracket of the function you have to change the field name. In this case the field name for the soil suitability was "Eignungsei". You have to
replace this with your correspondending field name.


**********************************
**********************************

After this script is run you will have four dBase files with the frequency and the mean land coverage in percent for the the different soil suitbaility categories per buffer.

The visualisation itself was done in Excel.

Lines that are not commented on do not need to be adjusted.