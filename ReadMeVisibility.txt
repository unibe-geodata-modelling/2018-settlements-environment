Read Me Visibility Analysis

******************************************************************************************
Variablea "myworkspace", "settl", "settlements", "dem" and "visible_area" (several lines):
******************************************************************************************

For the visiblity analysis you have to adjust the variable "myworkspace" (line 16) to your chosen workspace.
The variable "tempdir" (line 17) must also be adjustet to your own temporary directory.

The "Settlements" variable (line 24) is where you read in your point shapefile of settlements and the "dem" 
variable (line 27) is where you read in your DEM. There you have to adjust the path to the directory where your
point shapefile/ DEM is stored.

The "settl" variable (line 34) is where you set your temporary directory.

The "visible_area" variable (line 52) is where you save your results for the visibility analysis for each settlement. You can adjust the path
to where you want to have your results saved. However, the ending ... str(id) +".tif" has to stay, since it allows to save the new raster data sets
separatly and as a tiffs.

The "visarea" variable (line 53) is where you save only the visible area. When the visibility function is conducted there are two values 0 an 1,
0 for non-visible and 1 for visible. This is saved in the "visible_area" variable. In the "visarea" you only have the value 1 -> only the 
visible area. You can adjust the path to where you want to have your results saved. However, the ending ... str(id) +".tif" has to stay, since it
allows to save the new raster data sets separatly and as a tiffs.


*************************************************
Cell size and extention setting (lines 28 and 30)
*************************************************

On the lines 28 to 30 you do not have to change anything. Here the cell size, the extent and the newly produced rasters made during the script
are set to the extent and cell size of the DEM.


**************************************
Add field to attribute table (line 42)
**************************************

On line 41 you can add the field "MaxArea" to your attribute table. If this field already exists in your attribute table you do not
have to use this line and can just put a # before this line.

There are other lines where a field is added, however, the problem stated above should not arise with them since later on fields are only added
to newly created rasters with no previous fields.


********************************
The visiblity function (line 60)
********************************

On line 60 the visiblity function is condcuted. Here you can also adjust some settings. For example you could elevate all your
settlement points a few meters if you wanted to simulate a watchtower or you could also set a maximum limit to the distance where the analysis
should be conducted -> e.g. you could only check the visible area inside a 20 km radius. In this case no elevation or distance limit was added.


*******************************************************
Add field to the new visiblity raster (lines 64 and 65)
*******************************************************

On these to lines the fields "Area" and "ID" are added. Their value is later on determined On the lines 67 and 68. You do not have to change anything here,
since it is a new raster there is not the possibility that these two fields already exist as on line 41.


**************************************************************************************
Field calculation of square meters of visible area and the field "ID" (line 67 and 68)
**************************************************************************************

On line 67 you have the function "arcpy.CalculateField_management()". Here the field "Count"(the number of cells of visible area) is multiplied
by the number of square meters one cell represents. In this case one cell had a size of 200x200 m which means that the field "Count" was multiplied
by 40000. If you have another cell size you have to adjust this number.

On line 68 you use the same function with other inputs to fill out the field/column "ID" (over the str (id)). Here you do not have to change anything. 


******************************************
Extracting only the visible area (line 71)
******************************************

Here only the visible area is extracted from the newly created visibility raster. You do not need to change anything here.


***********************************************************************
Converting the attribute table of the visible area to a dBase (line 73)
***********************************************************************

On line 73 you convert the attribute table of the visible area to a dBase with "arcpy.TableToTable_conversion()". The first input is the input table you
want to have converted, in this case saved in the "visarea" variable. For the first input you do not have to change anything.
The second is the output path. You can adjust the output path if you want, however for the further commands it is important
that you save the output in a folder, where no other dBase or other tables exist. What cannot be changed is the ending of the databeses ... + str(id) + ".dbf"
since this allows to save each table seperatly and as a dBase. Futhermore, on the same line the path that was set for the "visarea" variable from line 53 is used several times. 
Each time this path is written down, you have to adjust it to your path from line 53.


******************************************************************************
Joining the individual tables and the "myworkspace2" variable (lines 82 to 84)
******************************************************************************

On line 82 a second workspace environment is set since the function "listTables" lists all the tables from the set workspace. You have to adjust
this path to the folder where you saved the dBase version of the attribute tables of the visible area rasters -> see also just above "Converting the attribute
table of the visible area to a dBase (line 73).

On line 83 you do not have to change anything.

On line 84 you don't have to change anything either unless you want to change the name of the final table with all the information combined, which is here named as "visiblareajoin.dbf". 
If you do that you will also have to adjust the path/name on line 88 in the function "arcpy.Merge_management(), on line 94 in the function Dbf5() and on line 107 in the arcpy.Statistics_analysis() function.



***********************************************************************************************************
Joining the table of the visible area data with the attribute table of the settlement shapefile (line 88)
***********************************************************************************************************

The first input of the function "arcpy.JoinField_management() is the table to which the join table (in this case the settlement attribute table) will be joined (ArcGIS for Desktop: 2016).
Unless you have chosen another name for the combined visible area table you do not have to change anything. If you have chosen another name you have to replace "visibleareajoin.dbf" with 
the name of your table (see also "Joining the individual tables and the myworksapce 2" table).
For the last input in the brackets (in this case "Name;Gemeinde;Epoche;Zeitstufe;Datierung;Fundort") you can choose which fields/columns of the attribute table of the settlement shapefile are going
to be added to the visiblea area table.

ArcGIS for Desktop (2016). Join Field [online]. "Available at: http://desktop.arcgis.com/en/arcmap/10.3/tools/data-management-toolbox/join-field.htm" [Last accessed: 02.08.2018].


**********************************************
Visualisation in the par plot (line 94 to 102)
**********************************************

Unless you have chosen another name for the combined visible area table you do not have to change anything on lines 94 and 95. If you have chosen another name you have to replace 
 "visibleareajoin.dbf" with the name of your table.
On line 96 you can make adjustments on how many bins/bars you want to have displayed. In this case 56 were chosen, the same amount as there are settlements.
On the lines 97 to 99 you can adjust the labeling of the x- and y-axis as well as the title of the plot.
On line 102 you can adjust the path to your chosen directory.

**********************************************************************
Calculating the mean and the standard deviation (line 107 to line 114)
**********************************************************************
On line 107 you can adjust the first two inputs of the function arcpy.Statistics_analysis(). The first one only has to be adjusted if you chose to give the visible area dBase table another name.
The second input is the output path for the table with the calculated mean and the standard deviation.

On line 109 you have to adjust the path of the Dbf5 function to where you have saved the results from line 107.
You do not have to change anything for the following lines. On line 115 the coefficient of variance is automatically displayed in the console as soon as you run this line. However, it is not saved in any table.


**********************************
**********************************

Lines that are not commented on in this ReadMe do not need to be adjusted.

After the script is run you will have rasters with the visible area for all settlements, as well as a dBase table visibleareajoin.dbf where all the settlements are listed with their
visible area in sqaure meters.