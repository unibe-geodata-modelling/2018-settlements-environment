import arcpy
from arcpy import env
from arcpy.sa import *
from arcpy.sa import Con

if arcpy.CheckExtension("Spatial") == "Available":
    arcpy.CheckOutExtension('Spatial') #Checkout the extension
else:
    print "no spatial analyst license available" #Checkout if the extension is working

#*****************************
#Set environment and workspace
#*****************************

myworkspace="D:/Unibern/Geographie/Master/Geodatenanalyse/Projekt/MeineToolbox/ToolData" #Variable for the workspace path
arcpy.env.workspace= myworkspace #Workspace is set
arcpy.env.overwriteOutput = True #Allows to overwrite other files (e.g. to overwrite tables)

#DEM
dem=arcpy.Raster(myworkspace + "/" + "dem" + "/" + "swiss10.tif") #Reading in the DEM (10x10 m cell size)
arcpy.env.cellSize = dem #Cell size setting
arcpy.env.extent = dem #Setting the extent
arcpy.env.snapRaster = dem #Tools that honor the snap raster environment will adjust the extent of output rasters so that they match the cell alignment of the specified snap raster (ArcGIs for Desktop 2018).
#ArcGIS for Desktop (2018). Snap Raster (Environment setting) [online]. Available at: "http://desktop.arcgis.com/en/arcmap/10.3/tools/environments/snap-raster.htm" [last accessed: 01.08.2018].


#*****************************************
#Mean and standard deviation from the DEM
#*****************************************

#Focal Statistics DEM: calculating the mean for each cell from the 50x50 surrounding cells
arcpy.gp.FocalStatistics_sa(dem, myworkspace + "/" + "Results" + "/" + "tpi10x10mean.tif", "Rectangle 50 50 CELL", "MEAN", "DATA") #Focal statistics function
FocalMean=arcpy.Raster(myworkspace + "/" + "Results" + "/" + "tpi10x10mean.tif") #Reading in the newly created Raster

#Focal Stastics DEM: calculating the standard deviation for each cell from the 50x50 surrounding cells
arcpy.gp.FocalStatistics_sa(dem, myworkspace + "/" + "Results" + "/" + "tpi10x10std.tif", "Rectangle 50 50 CELL", "STD", "DATA") #Focal statistics function
tpi10x10std =arcpy.Raster(myworkspace + "/" + "Results" + "/" + "tpi10x10std.tif") #Reading in the newly created Raster


#**************
#Slope function
#**************

#Determine the slopes in degrees with the arcpy slope function:
arcpy.gp.Slope_sa(dem, myworkspace + "/" + "Results" + "/" + "slope10.tif", "DEGREE", "1") #Slope function
slope10=arcpy.Raster(myworkspace + "/" + "Results" + "/" + "slope10.tif") #Reading in the newly crated slope raster


#*******************************
#TPI and landform classification
#*******************************

#Determine the TPI: difference between the actual elevation from one cell and the average elevation from the surronding cells -> DEM - mean elevation
tpi10m= dem - FocalMean #In Pyhton you work directly with Map Algebra and not the raster calculator.
tpi10m.save(myworkspace + "/" + "Results" + "/" + "tpi10m.tif") #Saving the result
tpi10m =arcpy.Raster(myworkspace + "/" + "Results" + "/" + "tpi10m.tif") #Reading in the newly created Raster

#Dividing the standard deviaton raster by 2 for later use in the classification:
#halftpi10x10std= (tpi10x10std/2) +++++ This steps creates an exit code in Python, however in the arcpy console in ArcGIS and with other IDEs this command works
#halftpi10x10std.save(myworkspace + "/" + "Results" + "/" + "hstd.tif") +++++ This steps creates an exit code in Python, however in the arcpy console in ArcGIS and with other IDEs this command works
halftpi10x10std =arcpy.Raster(myworkspace + "/" + "Results" + "/" + "hstd.tif") #Reading in the newly created Raster

#Classification with Map Algebra using conditional evaluation -> This steps creates an exit code in Python, however in the arcpy console in ArcGIS and with other IDEs this command works
#classification= Con(tpi10m  <  - tpi10x10std,1, Con((- halftpi10x10std > tpi10m) & (tpi10m >=  - tpi10x10std),2, Con((halftpi10x10std >= tpi10m) & (tpi10m >=  - halftpi10x10std) & (slope10  <=  5),3, Con((halftpi10x10std >= tpi10m) & (tpi10m >=  - halftpi10x10std) & (slope10  > 5),4, Con((tpi10x10std >= tpi10m) & (tpi10m> halftpi10x10std),5, Con(tpi10m > tpi10x10std,6))))))
#classification.save(myworkspace + "/" + "Results" + "/" + "classif.tif") ++++++ This steps creates an exit code in Python, however in the arcpy console in ArcGIS and with other IDEs this command works

print "done!"
classification=arcpy.Raster(myworkspace + "/" + "Results" + "/" + "classif.tif") #Reading in the classified raster


#****************************************************************************************************
#Preparing the classified raster and the settlement shapefile for later use in the intersect function
#****************************************************************************************************

#Resample function - coarser resolution of the classified raster
arcpy.Resample_management(classification, myworkspace + "/" + "Results" + "/" + "classif200.tif", "200 200", "NEAREST") #Resampling raster to a coarser resolution (200x200m cell size), because there is an error message if the resulting shapefile exeeds the size of 2 GB, which is the case with the finer resolution.
classification200=arcpy.Raster(myworkspace + "/" + "Results" + "/" + "classif200.tif") #Reading in the resampled raster


#Convert the classified raster to a polygon for later use for the intersect function
classif200= myworkspace + "/" + "Results" + "/" + "classif200.shp" #Preparing the variable for the shapefile output
arcpy.RasterToPolygon_conversion(classification200, classif200 , "SIMPLIFY", "Value") #Raster to polygon function

#Reading in the settlement shapefile for later use in buffer function:
Settlements = myworkspace + "/" + "Siedlungen" + "/" + "CH_SiedlungenLV03.shp" #Reading in the settlement point shapefile


#******************************************************
#Erase function to exclude the lakes from the landforms
#******************************************************

#Reading in the lake shapefile for later use in the erase function:
Lakes= myworkspace + "/" + "Landcover" + "/" + "Seenmerge.shp"

#Preparing variable to save results of the erase function:
classif200land= myworkspace + "/" + "Results" + "/" + "classif200land.shp"

#Erase function: This function is used because the lakes were also classified as a landform. Since only the information of the land is of interest the erase function is used to erase all the lakes from the shapefile with the classified landforms.
arcpy.Erase_analysis(classif200, Lakes, classif200land, "")


#**********************************************
#Setting the buffers and calculating their area
#**********************************************

#Preparing the variables for the buffer function
Buffer500= myworkspace + "/" + "Landcover" + "/" + "Buffer500.shp"
Buffer1000 = myworkspace + "/" + "Landcover" + "/" + "Buffer1000.shp"
Buffer5000 = myworkspace + "/" + "Landcover" + "/" + "Buffer5000.shp"

#Setting the buffer with various radii around the settlements
arcpy.Buffer_analysis(Settlements, Buffer500, "500 Meters", "FULL", "ROUND", "NONE", "", "PLANAR")
arcpy.Buffer_analysis(Settlements, Buffer1000, "1000 Meters", "FULL", "ROUND", "NONE", "", "PLANAR")
arcpy.Buffer_analysis(Settlements, Buffer5000, "5000 Meters", "FULL", "ROUND", "NONE", "", "PLANAR")

#Buffer areas in square meters are determined
arcpy.AddGeometryAttributes_management(Buffer500, "AREA", "METERS", "SQUARE_METERS", "") #Calculation of the area of the buffers in square meters. The area is automatically saved in a newly created field "POLY_AREA"
arcpy.AddGeometryAttributes_management(Buffer1000, "AREA", "METERS", "SQUARE_METERS", "")
arcpy.AddGeometryAttributes_management(Buffer5000, "AREA", "METERS", "SQUARE_METERS", "")


#*****************************************************************
#Intersect function between the landform shapefile and the buffers
#*****************************************************************

#Intersect buffers and the landform shapefile
interland500 = myworkspace + "/" + "Landcover" + "/" + "interland500.shp" #Preparing variables for the intersect function
interland1000 = myworkspace + "/" + "Landcover" + "/" + "interland1000.shp"
interland5000 = myworkspace + "/" + "Landcover" + "/" + "interland5000.shp"

# Intersect
arcpy.Intersect_analysis([classif200land, Buffer500], interland500, "ALL", "", "INPUT") #The intersect function intersects the buffers with the classified landform shapefile
arcpy.Intersect_analysis([classif200land, Buffer1000], interland1000, "ALL", "", "INPUT")
arcpy.Intersect_analysis([classif200land, Buffer5000], interland5000, "ALL", "", "INPUT")


#************************************************************************************
#Preparing commands for the calculation of the percentages of the different landforms
#************************************************************************************

#Add Field "Percent" for later calcuations for the area percentages of the individual polygon/landform areas inside a buffer
arcpy.AddField_management(interland500, "Percent", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(interland1000, "Percent", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(interland5000, "Percent", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

#Add Geometry Attributes: Adds the area of the individual landform classes inside a buffer
arcpy.AddGeometryAttributes_management(interland500, "AREA", "METERS", "SQUARE_METERS", "") #The calculated area is automatically saved in a newly created field/column named "POLY_AREA"
arcpy.AddGeometryAttributes_management(interland1000, "AREA", "METERS", "SQUARE_METERS", "")
arcpy.AddGeometryAttributes_management(interland5000, "AREA", "METERS", "SQUARE_METERS", "")


#Get the area of the buffer for later calculations
AreaBuff500=arcpy.SearchCursor(Buffer500)
for Area500 in AreaBuff500:
    Area500m=Area500.getValue("POLY_AREA") #The value is taken from the field "POLY_AREA" that was created in lines 118 to 120
    print (Area500m) #Prints out the area in the console -> for this buffer it is: 785191,173 m2

AreaBuff1000=arcpy.SearchCursor(Buffer1000)
for Area1000 in AreaBuff1000:
    Area1000m=Area1000.getValue("POLY_AREA")
    print (Area1000m) #Prints out the area in the console -> for this buffer it is: 3141177 m2

AreaBuff5000=arcpy.SearchCursor(Buffer5000)
for Area5000 in AreaBuff5000:
    Area5000m=Area5000.getValue("POLY_AREA")
    print (Area5000m) #Prints out the area in the console -> for this buffer it is: 78537724,241 m2


#Calculate field "percentage" for the different landform classes inside the buffers
arcpy.CalculateField_management(interland500, "Percent", "[POLY_AREA] /785191.17*100", "VB", "")#The Area of the different landform classes inside the buffer is divided by the whole buffer area and multiplied by 100 to receive the percentage of coverage per polygon/landform
arcpy.CalculateField_management(interland1000, "Percent", "[POLY_AREA] /3141177*100", "VB", "")
arcpy.CalculateField_management(interland5000, "Percent", "[POLY_AREA] /78537724.241*100", "VB", "")


#Variables for table with summarized landform classes per settlement -> Sometimes in one buffer the same landform class can appear in several separated polygons.
#These variables are used later to combine these separated polygons, that the same landform only appears once per settlement in the dBase table.
SumBuffLand500 = myworkspace +"/" +"Results" + "/" + "SumBuffLand500.dbf" #These variables are later used to combine polygons with the same landform class.
SumBuffLand1000 = myworkspace +"/" +"Results" + "/" + "SumBuffLand1000.dbf"
SumBuffLand5000 = myworkspace +"/" +"Results" + "/" + "SumBuffLand5000.dbf"

#Function for summarizing the landform classes (along with their percentages of coverage in the buffer area) per settlement as stated above.
arcpy.Statistics_analysis(interland500, SumBuffLand500, "Percent SUM", "GRIDCODE;Fundort")
arcpy.Statistics_analysis(interland1000, SumBuffLand1000, "Percent SUM", "GRIDCODE;Fundort")
arcpy.Statistics_analysis(interland5000, SumBuffLand5000, "Percent SUM", "GRIDCODE;Fundort")


#Variables for the calculation of the mean surface coverage in percents per landform per buffer
LandStats500 = myworkspace + "/" + "Results" + "/" + "LandStats500.dbf"
LandStats1000 = myworkspace + "/" + "Results" + "/" + "LandStats1000.dbf"
LandStats5000 = myworkspace + "/" + "Results" + "/" + "LandStats5000.dbf"


#Calculation of the mean percentage (and the standard deviation) of land coverage of the  individual landforms.
#The mean percentage is not over all settlements/buffers. If a landform e.g. only appears in 5 settlements the percentage shows what the mean coverage for those 5 settlements is and not for all 56.
arcpy.Statistics_analysis(SumBuffLand500, LandStats500, "SUM_Percen MEAN;SUM_Percen STD", "GRIDCODE")
arcpy.Statistics_analysis(SumBuffLand1000, LandStats1000, "SUM_Percen MEAN;SUM_Percen STD", "GRIDCODE")
arcpy.Statistics_analysis(SumBuffLand5000, LandStats5000, "SUM_Percen MEAN;SUM_Percen STD", "GRIDCODE")
