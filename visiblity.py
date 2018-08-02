import arcpy
import numpy
import os
import pandas
import matplotlib.pyplot as plt
from simpledbf import Dbf5

if arcpy.CheckExtension("Spatial") == "Available":
    arcpy.CheckOutExtension('Spatial') #Checkout the extension "Spatial"
else:
    print "no spatial analyst license available" #checkout if the extension is working

#*******************************
#set environemnt and workspace
#*******************************
myworkspace="D:/Unibern/Geographie/Master/Geodatenanalyse/Projekt/MeineToolbox/ToolData"
tempdir="D:/temp" #data that you don't need at the end
print "Workspace: " + myworkspace
arcpy.env.workspace= myworkspace #workspace is set
arcpy.env.overwriteOutput = True #allows to overwrite other files (e.g. to overwrite tables)


#settlements shapefile
settlements=myworkspace + "/" + "Siedlungen" + "/" + "CH_SiedlungenLV03.shp" #reading in shapefile of settlement points

#dem
dem=arcpy.Raster(myworkspace + "/" + "dem" + "/" + "swiss200") #reading in the dem
arcpy.env.cellSize = dem #cellsize setting
arcpy.env.extent = dem #extent setting/environnment setting)
arcpy.env.snapRaster = dem #"Tools that honor the Snap Raster environment will adjust the extent of output rasters so that they match the cell alignment of the specified snap raster" (ArcGIs for Desktop 2018).
#ArcGIS for Desktop (2018). Snap Raster (Environment setting) [online]. Available at: "http://desktop.arcgis.com/en/arcmap/10.3/tools/environments/snap-raster.htm" [last accessed: 01.08.2018].


#Set the temporary directory
settl=tempdir+"/"+"settlement.shp"


#***********************************************************************************************************************
#Add Field to the settlement shapefile Use only if these fields do not exist in the attribute table already!
#***********************************************************************************************************************

#arcpy.AddField_management(settlements, "MaxArea", "FLOAT", "16", "5", "", "", "NULLABLE", "NON_REQUIRED", "") #Adds the field "MaxArea" to the settlement shapefile. Use only if these fields do not exist in the attribute table already!


#**************************************************************************************************
#Loop for the visibility function - the area for each settlement is calculated and saved seperatly
#**************************************************************************************************

cursor = arcpy.da.UpdateCursor(settlements, ["FID", "MaxArea"]) #a cursor is made -> same as selecting a row. In the square brackets the fields/columns that you want selected are put in. In this case "FID" the identification number and "MaxArea" where the visible area will be written in.
for row in cursor: #for each row in this shapefile following commands apply:
    id = row[0] #row with index 0 is the first row
    visible_area= os.path.join(myworkspace + "/" + "Results" + "/" + "Viewshed" + "/" "visib" + str (id) + ".tif") #os path join is used, that the visible area of each area is saved separately with its ID number at the end of the name. The str (id) coincides with the real FID of the settlements in the settlement shapefile
    visarea= os.path.join(myworkspace + "/" + "Results" + "/" + "Viewshed" + "/" "visarea" + str (id) + ".tif") #variable is later used to only extract the count of visible area/cells (the output of the visiblity anlysis gives out an attribute table with two classes: visible and non-visible)
    print "processing FID: " + str(id)
    where_clause = '"FID" = ' + str(id) # This variable will be used for the function arcpy.Select_analysis() to select which settlement is being processed
    arcpy.Select_analysis(settlements,settl, where_clause) #extract 1 single settlement point from all points
    #calculate visbility:
    useEarthCurvature= "CURVED_EARTH" #variable preperation for the visiblity analysis. "Curved_EARTH" is a standard setting
    refractivityCoefficient = 0.13 #variable preperation for the visibility analysis. 0.13 is a standard setting
    arcpy.gp.Visibility_sa(dem, settl, visible_area, "", "FREQUENCY", "ZERO", "1", "FLAT_EARTH", "0.13", "", "", "", "", "", "", "", "", "") #visibility function

	#add field for area calculation
    # Process: Add Field
    arcpy.AddField_management(visible_area, "Area", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "") #the field "Area" is added to the newly created raster
    arcpy.AddField_management(visible_area, "ID", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "") #the field "ID" is added to the newly created raster
    # Process: Calculate Field
    arcpy.CalculateField_management(visible_area, "Area", "[Count]*40000", "VB", "") #Calculation of the area in square meters. The count has to be multiplied by 40000 since one cell is an area of 200x200 m
    arcpy.CalculateField_management(visible_area, "ID", str (id), "VB", "") #str (id) is used to fill out the field "ID" for each settlement.

    # extract only the visible area to a new raster:
    arcpy.gp.ExtractByAttributes_sa(visible_area, "\"OID\" =1", visarea) #1 stands in this case for the visible area (0 would be non-visible)
    #convert attribute tables to dBase and save them. The ID is added to the name as with the rasterfiles before, so that they can be saved separatly:
    arcpy.TableToTable_conversion(visarea, myworkspace + "/" + "Results" + "/" + "Tables", "visarea" + str (id) + ".dbf", "", "Value \"Value\" false true false 10 Long 0 10 ,First,#,D:\\Unibern\\Geographie\\Master\\Geodatenanalyse\\Projekt\\MeineToolbox\\ToolData\\Results\\Viewshed\\visarea + str (id) +.tif\\Band_1,Value,-1,-1;Count \"Count\" false true false 19 Double 0 0 ,First,#,D:\\Unibern\\Geographie\\Master\\Geodatenanalyse\\Projekt\\MeineToolbox\\ToolData\\Results\\Viewshed\\visarea + str (id) +.tif\\Band_1,Count,-1,-1;Area \"Area\" true true false 10 Long 0 10 ,First,#,D:\\Unibern\\Geographie\\Master\\Geodatenanalyse\\Projekt\\MeineToolbox\\ToolData\\Results\\Viewshed\\visarea + str (id) +.tif\\Band_1,Area,-1,-1;ID \"ID\" true true false 5 Short 0 5 ,First,#,D:\\Unibern\\Geographie\\Master\\Geodatenanalyse\\Projekt\\MeineToolbox\\ToolData\\Results\\Viewshed\\visarea + str (id) +.tif\\Band_1,ID,-1,-1", "")
    cursor.updateRow(row) #the cursor goes to the next row/next settlement
del row #you don't have to do that, but if you create another cursor it is sometimes better to delete the old one
del cursor # ""
print "done!"

#********************************************************
#Joining the visible area tables to the settlement table
#********************************************************
myworkspace2= arcpy.env.workspace = "D:/Unibern/Geographie/Master/Geodatenanalyse/Projekt/MeineToolbox/ToolData/Results/Tables" #setting a new workspace to list the tables
listTable = arcpy.ListTables() #lists the tables that are in the workspace
arcpy.Merge_management(listTable, myworkspace2 +"/" + "visiblareajoin.dbf") #join the individual visible area tables to one single table
print "done!"

# Process: Join Field
arcpy.JoinField_management(myworkspace2 +"/" + "visiblareajoin.dbf", "ID", settlements, "ID", "Name;Gemeinde;Epoche;Zeitstufe;Datierung;Fundort") #join the table of the visible area to the settlement table over the field "ID"

#*****************************
# visualisation in a bar plot
#*****************************

visblareadbf= Dbf5(myworkspace2 + "/" + "visiblareajoin.dbf") #convert dbf-File into a data frame
dfvisarea= visblareadbf.to_dataframe() #convert dbf-File into a data frame
plt.hist(dfvisarea["Area"],bins=56) #command for a histogramm and how many bars you want to have displayed. In this case 56 were chosen because there are 56 settlements.
plt.xlabel("m2") #here you set your label for the x-axis
plt.ylabel ("number of villages") #here you set your label for the y-axis
plt.title("Visible area per village") #title of the plot
plt.show() #pop-up of the figure
plt.savefig(myworkspace + "/" +"Results" + "/" + "histovisarea.png") #saving the plot as a png

#*******************************************************************
#Calculate the mean and the standard deviation of the visible area
#*******************************************************************

arcpy.Statistics_analysis(myworkspace2 +"/" + "visiblareajoin.dbf", myworkspace +"/" + "Results" + "/" + "StatisticsVIS.dbf", "Area MEAN;Area STD", "") #function for calculation of the mean and the standard deviation

statisticsVISdbf= Dbf5(myworkspace + "/" + "Results" + "/" "StatisticsVIS.dbf") #Convert dbf-File into a data frame
statisticsVIS= statisticsVISdbf.to_dataframe() #Convert dbf-File into a data frame
statisticsVISmean= statisticsVIS["MEAN_Area"] #Setting variable of the mean
statisticsVISstd= statisticsVIS["STD_Area"] #Setting variable of the Standard deviation

COV=statisticsVISstd*100/statisticsVISmean #calculating the coefficient of variance
print COV
