Read Me Lake-Land Ratio Analysis


**********************************************************************************************************************
Variables "myworkspace", "lake", "settlements", "BuffLake100" to "BuffLake5000", "interLake100" to "interLake5000" and
"SumLakeBuff100" to "SumLakeBuff5000" (several lines)
**********************************************************************************************************************

For the lake-land ratio analysis you have to adjust the variable "myworkspace" (line 14) to your chosen workspace. 

The "Lake" variable (line 21) is where you read in your lake/hydrography shapefile. You have to adjust
the path to where you have stored your hydrography data. 

The "Settlements" variable (line 24) is where you read in your settlement point shapefile. You have to adjust the path to
where you have stored your settlement shapefile.

"BuffLake100" to "BuffLake5000" (lines 32 to 35). These are the variables for the buffers you set around your settlements. You can adjust the path
to your chosen directory. Since it is no final result you can also use a temporary directory.

The variables "interLake100" to "interLake5000" (lines 61 to 64) are the variables that are used as the output path for the intersect function.  You can adjust the path
to your chosen directory. Since it is no final result you can also use a temporary directory.

Variables "SumLakeBuff100" to "SumLakeBuff5000" (lines 127 to 130): In some buffers there is more than one lake. These variables are later used as the output path in a function
to combine these separated polygons per buffer/settlement. You can adjust the path to your chosen directory.


*******************************************************************************
Buffer function and add geometry to the buffer attirubte table (lines 38 to 53)
*******************************************************************************

Here you can adjust the distance of the buffer/s. In this example 100, 500, 1000 and 5000 meters radii were used. If you want other distances just exchange the number
on the input "100 Meters" or any other of the distances you want to change. If you want fewer buffers, you can simply delete the rows with the distances you do not
want or put a # before the lines. If you do that, you have to do that for every following command.

You do not have to change anything for the "add geometry" function. The results will be automatically saved in a newly created field named "POLY_AREA".


***********************************
Intersect function (lines 67 to 70)
***********************************

No changes are needed for the intersect function.


*********************************************************************
Add field "Percent" and add geometry Attribute "Area"(lines 78 to 87)
*********************************************************************

The added area from the "add geometry" function will be automatically saved in a newly created field "POLY_AREA" and you do not have to adjust anything for
these two lines.


******************************************************************
Getting the area of the buffers in square meters (lines 95 to 113)
******************************************************************

Here you only have to change something if you have chosen other buffer distances than in the original script. If you have done that, you have to write down
the correct amount of sqaure meters for your buffer distance which is displayed in the console via print (Area...m).


*************************************************************************************************************
Calculating the percentage of the lake polygon/s in relation to the respective buffer area (lines 121 to 124)
*************************************************************************************************************

Here you only have to adjust something if you have chosen other buffer distances. If you have done that you have to divide the field "POLY_AREA" by the correct amount of square meters
for your buffer distance. See also just above under "Getting the area of the buffers in sqaure meters (lines 95 to 113)".


***********************************************************************************************************
Statistics analysis - Summarizing lake polygons if there are more than one in one buffer (lines 133 to 136)
***********************************************************************************************************

The function "arcpy.Statistics_analysis() is used to summarize the percentage of the lake polygons if there are several different lakes in the same buffer/around the same settlement.
In the last input in the bracket of the function you have to change the last field name. In this case the field name for the settlments was "Fundort". You have to
replace this with your correspondending field name for the settlements. The field name "Percent_SUM" should be the same since it was newly created in the lines 121 to 124 and you
do not need to change it.


***********************************************
Visualisation in the par plot (line 144 to 184)
***********************************************

The same commands are used four times for the visualition of the different buffer distances. The lines named in the following are for the visualisation of the 100 m radius buffer, however
the remarks are also applicable for the other three "visualiston blocks".
You do not have to change anything in line 144 and 145. 
On line 146 you can make adjustments on how many bins/bars you want to have displayed. In this case 56 were chosen, the same amount as there are settlements.
On the lines 147 to 149 you can adjust the labeling of the x- and y-axis as well as the title of the plot.
On line 151 you can adjust the path to your chosen directory to save the bar plot.


**********************************************************************************************
Calculating the mean, the standard deviation and the coefficient of variance (line 192 to 232)
**********************************************************************************************

The same commands are used four times for the calculation of the mean, the standard deviation and the COV. The lines named in the following are for the first calculation
of the buffer distance of hundert meters, however the remarks are also applicable for the other three "statistic blocks".
On line 192 you can adjust the second input of the function arcpy.Statistics_analysis(). The second input into the bracket is the output path 
for the table with the calculated mean and the standard deviation.
On line 193 you have to adjust the path in the function "Dbf5" to where you have saved the table with the calculated mean and the standard deviation on line 192.
The other lines do not need any adjustments.
To see the coefficient of variance you have to run the line 199 which prints out the COV in the console, however it is not saved in any table.

**********************************
**********************************

Lines that are not commented on in this ReadMe do not need to be adjusted.

After this script is run you will have four dBase (one per buffer distance) tables with the lake coverage in percent per settlement and four (one per buffer distance)
additional dBase files with only the mean and standard deviation over all settlements.