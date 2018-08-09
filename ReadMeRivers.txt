Read Me River Analysis

********************************************************************************
Variables "myworkspace", "settlements", "Settldbf" and "Rivers" (several lines):
********************************************************************************

For the river analysis you have to adjust the variable "myworkspace" (line 16) to your chosen workspace.

The "Settlements" variable (line 27) is where you read in your settlement point shapefile. There you have to adjust the path to the directory where your
settlement point shapefile is stored.

The "Settldbf" variable (line 28) is where your dBase file of the settlment data is stored. It should be the exact same path with the difference of the ending 
being .dbf instead of .shp.

The "Rivers" variable (line 31) is where you read in your polyline shapefile of the rivers. You have to adjust the path to the directory where you have stored
your river shapefile.


**************************************************
Near function -> determine nearest river (line 39)
**************************************************

This function determines which is the nearest river to each settlement and also saves the distance in meters in the settlement attribute table.
No adjustments are needed.


*********************************************
Visualisation in the par plot (line 46 to 53)
*********************************************

Lines 46 and 47 need no adjustments.
On line 48 you can make adjustments on how many bins you want to have maximally displayed. In this case 56 were chosen, the same amount as there are settlements.
On the lines 49 to 51 you can adjust the labeling of the x- and y-axis as well as the title of the plot.
On line 53 you can adjust the path to your chosen directory to where you want to save the resulting figure.


********************************************************************************************
Calculating the mean, the standard deviation and the coefficient of variance (line 60 to 68)
********************************************************************************************
On line 60 you can adjust the second input of the function arcpy.Statistics_analysis(). The second input is the output path for the table with the calculated
mean and the standard deviation. You can adjust it to your chosen directory.

On line 62 you have to adjust the path in the function "Dbf5" to where you have saved the table with the calculated mean and the standard deviation from line 60.
On the following lines you should not have to adjust anything. The field names "MEAN_NEAR_" and "STD_NEAR_D" were created automatically and should always be the same.

When line 68 is run it will print out the coefficient of variance in the console, however the COV is not saved in any table.

**********************************
**********************************

Lines that are not commented on in this ReadMe do not need to be adjusted.

After you run the script you will have the distances to the nearest river attached to the attribute table of the settlement shapefile,
and the mean and standard devaition will be saved in the dBase file stastisticsRivers.dbf.