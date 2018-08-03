import arcpy


if arcpy.CheckExtension("Spatial") == "Available":
    arcpy.CheckOutExtension('Spatial') #Checkout the extension "Spatial"
else:
    print "no spatial analyst license available" #Checkout if the extension is working


#*****************************
#set environemnt and workspace
#*****************************

myworkspace="D:/Unibern/Geographie/Master/Geodatenanalyse/Projekt/MeineToolbox/ToolData" #Variable for the workspace path
print "Workspace: " + myworkspace
arcpy.env.workspace= myworkspace #Workspace is set
arcpy.env.overwriteOutput = True #Allows to overwrite other files (e.g. to overwrite tables)


#Soil Suitability map and settlment points
Bodeneignungskarte= myworkspace + "/" + "Landcover" + "/" + "Bodeneignungskarte_LV03.shp" #Reading in the soil type map
Settlements = myworkspace + "/" + "Siedlungen" + "/" + "CH_SiedlungenLV03.shp" #Reading in the settlement point shapefile

#********************
#Creating the Buffers
#********************

# Local variables:
Bufferzone100_shp = myworkspace + "/" + "Landcover" + "/" + "Bufferzone100.shp" #Setting the variables for the different buffer distances
Bufferzone500_shp = myworkspace + "/" + "Landcover" + "/" + "Bufferzone500.shp"
Bufferzone1000_shp = myworkspace + "/" + "Landcover" + "/" + "Bufferzone1000.shp"
Bufferzone5000_shp = myworkspace + "/" + "Landcover" + "/" + "Bufferzone5000.shp"

#Buffer for four different distances
arcpy.Buffer_analysis(Settlements, Bufferzone100_shp, "100 Meters", "FULL", "ROUND", "NONE", "", "PLANAR") #Calculating the buffer for different distances
arcpy.Buffer_analysis(Settlements, Bufferzone500_shp, "500 Meters", "FULL", "ROUND", "NONE", "", "PLANAR")
arcpy.Buffer_analysis(Settlements, Bufferzone1000_shp, "1000 Meters", "FULL", "ROUND", "NONE", "", "PLANAR")
arcpy.Buffer_analysis(Settlements, Bufferzone5000_shp, "5000 Meters", "FULL", "ROUND", "NONE", "", "PLANAR")


#************************************
#Calculating the areas of the buffers
#************************************

# Calculate Buffer Area
arcpy.AddGeometryAttributes_management(Bufferzone100_shp, "AREA", "METERS", "SQUARE_METERS", "") #Calculate the area of the buffers in square meters. The area is automatically saved in a newly created field "POLY_AREA"
arcpy.AddGeometryAttributes_management(Bufferzone500_shp, "AREA", "METERS", "SQUARE_METERS", "")
arcpy.AddGeometryAttributes_management(Bufferzone1000_shp, "AREA", "METERS", "SQUARE_METERS", "")
arcpy.AddGeometryAttributes_management(Bufferzone5000_shp, "AREA", "METERS", "SQUARE_METERS", "")


#***************************************************
#intersect the buffers with the soil suitability map
#***************************************************

#Intersect buffer and Bodeneignungskarte

interBoden100 = myworkspace + "/" + "Landcover" + "/" + "interBoden100.shp" #Preparing variables for the intersect function
interBoden500 = myworkspace + "/" + "Landcover" + "/" + "interBoden500.shp"
interBoden1000 = myworkspace + "/" + "Landcover" + "/" + "interBoden1000.shp"
interBoden5000 = myworkspace + "/" + "Landcover" + "/" + "interBoden5000.shp"

# Intersect
arcpy.Intersect_analysis([Bodeneignungskarte, Bufferzone100_shp], interBoden100, "ALL", "", "INPUT") #The intersect function intersects the buffers with the soil suitability map
arcpy.Intersect_analysis([Bodeneignungskarte, Bufferzone500_shp], interBoden500, "ALL", "", "INPUT")
arcpy.Intersect_analysis([Bodeneignungskarte, Bufferzone1000_shp], interBoden1000, "ALL", "", "INPUT")
arcpy.Intersect_analysis([Bodeneignungskarte, Bufferzone5000_shp], interBoden5000, "ALL", "", "INPUT")


#*******************************************************************************************************************
#Adding the field "Percent" and calculate area for the newly created shapefile resulting from the intersect function
#*******************************************************************************************************************

# Add Field "Percent" for later calcuations for the area percentages of the individual polygon areas inside a buffer
arcpy.AddField_management(interBoden100, "Percent", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(interBoden500, "Percent", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(interBoden1000, "Percent", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(interBoden5000, "Percent", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Add Geometry Attributes: Adds the area of the individual polygons inside a buffer
arcpy.AddGeometryAttributes_management(interBoden100, "AREA", "METERS", "SQUARE_METERS", "") #The calculated area is automatically saved in a newly created field named "POLY_AREA"
arcpy.AddGeometryAttributes_management(interBoden500, "AREA", "METERS", "SQUARE_METERS", "")
arcpy.AddGeometryAttributes_management(interBoden1000, "AREA", "METERS", "SQUARE_METERS", "")
arcpy.AddGeometryAttributes_management(interBoden5000, "AREA", "METERS", "SQUARE_METERS", "")


#*****************************************************
#Looking up the area of the different buffer distances
#*****************************************************

#Get the area of the buffer for later calculations
AreaBuff100=arcpy.SearchCursor(Bufferzone100_shp)
for Area100 in AreaBuff100:
    Area100m=Area100.getValue("POLY_AREA") #The value is taken from the field "POLY_AREA" that was created in lines 46 to 49
    print (Area100m) #Prints out the area in the console -> for this buffer it is: 31374,937m2

AreaBuff500=arcpy.SearchCursor(Bufferzone500_shp)
for Area500 in AreaBuff500:
    Area500m=Area500.getValue("POLY_AREA")
    print (Area500m) #Prints out the area in the console -> for this buffer it is: 785191,173m2

AreaBuff1000=arcpy.SearchCursor(Bufferzone1000_shp)
for Area1000 in AreaBuff1000:
    Area1000m=Area1000.getValue("POLY_AREA")
    print (Area1000m) #Prints out the area in the console -> for this buffer it is: 3141177,0m2

AreaBuff5000=arcpy.SearchCursor(Bufferzone5000_shp)
for Area5000 in AreaBuff5000:
    Area5000m=Area5000.getValue("POLY_AREA")
    print (Area5000m) #Prints out the area in the console -> for this buffer it is: 78537724,241m2


#*************************************************************
#Get the percentages of soil suitability categories per buffer
#*************************************************************

# Calculate the field "percent" for different polygons/sections of the soil suitability map inside the buffers
arcpy.CalculateField_management(interBoden100, "Percent", "[POLY_AREA] /31374.937*100", "VB", "") #The Area of the different polygons/different soil suitability categories inside the buffers is divided by the whole buffer area and multiplied by 100 to receive the percentage of coverage per polygon
arcpy.CalculateField_management(interBoden500, "Percent", "[POLY_AREA] /785191.17*100", "VB", "")
arcpy.CalculateField_management(interBoden1000, "Percent", "[POLY_AREA] /3141177*100", "VB", "")
arcpy.CalculateField_management(interBoden5000, "Percent", "[POLY_AREA] /78537724.241*100", "VB", "")


#Variables for table with summarized soil suitabilities per village -> Sometimes in one buffer the same soil suitability can appear in several separated polygons.
#These variables are used later to combine these separated polygons, that the same soil suitability only appears once per village in the table.

SumBuff100 = myworkspace +"/" +"Results" + "/" + "SumBuff100.dbf" #These variables are later used to combine polygons with the same soil suitability.
SumBuff500 = myworkspace +"/" +"Results" + "/" + "SumBuff500.dbf"
SumBuff1000 = myworkspace +"/" +"Results" + "/" + "SumBuff1000.dbf"
SumBuff5000 = myworkspace +"/" +"Results" + "/" + "SumBuff5000.dbf"

#Function for summarizing the soil suitability (along with their percentages of coverage in the buffer area) per village as stated above.
arcpy.Statistics_analysis(interBoden100, SumBuff100, "Percent SUM", "Eignungsei;Fundort")
arcpy.Statistics_analysis(interBoden500, SumBuff500, "Percent SUM", "Eignungsei;Fundort")
arcpy.Statistics_analysis(interBoden1000, SumBuff1000, "Percent SUM", "Eignungsei;Fundort")
arcpy.Statistics_analysis(interBoden5000, SumBuff5000, "Percent SUM", "Eignungsei;Fundort")


#***********************************************
#Calculating the mean and the standard deviation
#***********************************************

#Variables for calculating the mean land coverage in percents per soil suitability per buffer

SoilStats100 = myworkspace + "/" + "Results" + "/" + "SoilStats100.dbf"
SoilStats500 = myworkspace + "/" + "Results" + "/" + "SoilStats500.dbf"
SoilStats1000 = myworkspace + "/" + "Results" + "/" + "SoilStats1000.dbf"
SoilStats5000 = myworkspace + "/" + "Results" + "/" + "SoilStats5000.dbf"


#Calculate the mean percentage and the standard deviation of the  individual soil suitabilities per buffer.
#The mean percentage is not over all settlements/buffers. If a soil suitability category e.g. only appears in 5 settlements the percentage shows what the mean land coverage in percent for those 5 settlements is and not for all 56.

arcpy.Statistics_analysis(SumBuff100, SoilStats100, "SUM_Percen MEAN;SUM_Percen STD", "Eignungsei")
arcpy.Statistics_analysis(SumBuff500, SoilStats500, "SUM_Percen MEAN;SUM_Percen STD", "Eignungsei")
arcpy.Statistics_analysis(SumBuff1000, SoilStats1000, "SUM_Percen MEAN;SUM_Percen STD", "Eignungsei")
arcpy.Statistics_analysis(SumBuff5000, SoilStats5000, "SUM_Percen MEAN;SUM_Percen STD", "Eignungsei")






