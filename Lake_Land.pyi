import arcpy
import pandas
import matplotlib.pyplot as plt
from simpledbf import Dbf5

if arcpy.CheckExtension("Spatial") == "Available":
    arcpy.CheckOutExtension('Spatial') #Checkout the extension
else:
    print "no spatial analyst license available" #Checkout if the extension is working

#*******************************
#set environemnt and workspace
#*******************************
myworkspace="D:/Unibern/Geographie/Master/Geodatenanalyse/Projekt/MeineToolbox/ToolData" #Variable for the workspace path
print "Workspace: " + myworkspace
arcpy.env.workspace= myworkspace #Workspace is set
arcpy.env.overwriteOutput = True #Allows to overwrite other files (e.g. to overwrite tables)


#Lake Shapefile
Lake= myworkspace + "/" + "Seen_einzeln_merge.shp" #Reading in the lake shapefile

#Settlement shapefile:
Settlements = myworkspace + "/" + "Siedlungen" + "/" + "CH_SiedlungenLV03.shp" #Reading in the settlement shapefile


#********************
#Creating the Buffers
#********************

#Preparing variables for the buffer function:
BuffLake100= myworkspace + "/" + "Landcover" + "/" + "BuffLake100.shp"
BuffLake500 = myworkspace + "/" + "Landcover" + "/" + "BuffLake500.shp"
BuffLake1000 = myworkspace + "/" + "Landcover" + "/" + "BuffLake1000.shp"
BuffLake5000 = myworkspace + "/" + "Landcover" + "/" + "BuffLake5000.shp"

#Buffer function for four different distances:
arcpy.Buffer_analysis(Settlements, BuffLake100, "100 Meters", "FULL", "ROUND", "NONE", "", "PLANAR")
arcpy.Buffer_analysis(Settlements, BuffLake500, "500 Meters", "FULL", "ROUND", "NONE", "", "PLANAR")
arcpy.Buffer_analysis(Settlements, BuffLake1000, "1000 Meters", "FULL", "ROUND", "NONE", "", "PLANAR")
arcpy.Buffer_analysis(Settlements, BuffLake5000, "5000 Meters", "FULL", "ROUND", "NONE", "", "PLANAR")



#************************************
#Calculating the areas of the buffers
#************************************

#Add Geometry function: The area of the buffers is determined in square meters:
arcpy.AddGeometryAttributes_management(BuffLake100, "AREA", "METERS", "SQUARE_METERS", "") #The area is automatically saved in a newly created field "POLY_AREA"
arcpy.AddGeometryAttributes_management(BuffLake500, "AREA", "METERS", "SQUARE_METERS", "")
arcpy.AddGeometryAttributes_management(BuffLake1000, "AREA", "METERS", "SQUARE_METERS", "")
arcpy.AddGeometryAttributes_management(BuffLake5000, "AREA", "METERS", "SQUARE_METERS", "")


#***************************************************
#intersect the buffers with the soil suitability map
#***************************************************

#Preparing variables for the intersect function:
interLake100 = myworkspace + "/" + "Landcover" + "/" + "interLake100.shp"
interLake500 = myworkspace + "/" + "Landcover" + "/" + "interLake500.shp"
interLake1000 = myworkspace + "/" + "Landcover" + "/" + "interLake1000.shp"
interLake5000 = myworkspace + "/" + "Landcover" + "/" + "interLake5000.shp"

#Intersect function: The buffers are intersected with the lake shapefiles
arcpy.Intersect_analysis([Lake, BuffLake100], interLake100, "ALL", "", "INPUT")
arcpy.Intersect_analysis([Lake, BuffLake500], interLake500, "ALL", "", "INPUT")
arcpy.Intersect_analysis([Lake, BuffLake1000], interLake1000, "ALL", "", "INPUT")
arcpy.Intersect_analysis([Lake, BuffLake5000], interLake5000, "ALL", "", "INPUT")


#*******************************************************************************************************************
#Adding the field "Percent" and calculate area for the newly created shapefile resulting from the intersect function
#*******************************************************************************************************************

#Add Field "Percent" for later calculations for the land-lake-ratio:
arcpy.AddField_management(interLake100, "Percent", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(interLake500, "Percent", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(interLake1000, "Percent", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(interLake5000, "Percent", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

#Add Geometry: Adds the areas of the lake polygon or polygons (if there is more than one lake) inside a buffer:
arcpy.AddGeometryAttributes_management(interLake100, "AREA", "METERS", "SQUARE_METERS", "") #The area is automatically saved in a newly created field "POLY_AREA"
arcpy.AddGeometryAttributes_management(interLake500, "AREA", "METERS", "SQUARE_METERS", "")
arcpy.AddGeometryAttributes_management(interLake1000, "AREA", "METERS", "SQUARE_METERS", "")
arcpy.AddGeometryAttributes_management(interLake5000, "AREA", "METERS", "SQUARE_METERS", "")


#*****************************************************
#Looking up the area of the different buffer distances
#*****************************************************

#Get the area of the buffer for later calculations
AreaBuff100=arcpy.SearchCursor(BuffLake100)
for Area100 in AreaBuff100:
    Area100m=Area100.getValue("POLY_AREA") #The value is taken from the field "POLY_AREA" that was created in lines 50 to 53
    print (Area100m) #Prints out the area in the console -> for this buffer it is: 31374,937m2

AreaBuff500=arcpy.SearchCursor(BuffLake500)
for Area500 in AreaBuff500:
    Area500m=Area500.getValue("POLY_AREA")
    print (Area500m) #Prints out the area in the console -> for this buffer it is: 785191,173m2

AreaBuff1000=arcpy.SearchCursor(BuffLake1000)
for Area1000 in AreaBuff1000:
    Area1000m=Area1000.getValue("POLY_AREA")
    print (Area1000m) #Prints out the area in the console -> for this buffer it is: 3141177,0m2

AreaBuff5000=arcpy.SearchCursor(BuffLake5000)
for Area5000 in AreaBuff5000:
    Area5000m=Area5000.getValue("POLY_AREA")
    print (Area5000m) #Prints out the area in the console -> for this buffer it is: 78537724,241m2


#*************************************************************
#Get the percentages of soil suitability categories per buffer
#*************************************************************

#Calculate percentages of the lake polygon/s inside a buffer in relation to the whole buffer area
arcpy.CalculateField_management(interLake100, "Percent", "[POLY_AREA] /31374.937*100", "VB", "") #The Area of the lake polygon or polygons inside the buffers is divided by the whole buffer area and multiplied by 100 to receive the percentage of coverage per polygon
arcpy.CalculateField_management(interLake500, "Percent", "[POLY_AREA] /785191.17*100", "VB", "")
arcpy.CalculateField_management(interLake1000, "Percent", "[POLY_AREA] /3141177*100", "VB", "")
arcpy.CalculateField_management(interLake5000, "Percent", "[POLY_AREA] /78537724.241*100", "VB", "")

#Preparing variables for the statistics function to summarize the lake surfaces (if there are several lakes per settlement) in percent per settlement in a dBase file
SumLakeBuff100 = myworkspace +"/" +"Results" + "/" + "SumLakeBuff100.dbf"
SumLakeBuff500 = myworkspace +"/" +"Results" + "/" + "SumLakeBuff500.dbf"
SumLakeBuff1000 = myworkspace +"/" +"Results" + "/" + "SumLakeBuff1000.dbf"
SumLakeBuff5000 = myworkspace +"/" +"Results" + "/" + "SumLakeBuff5000.dbf"

#Function for summarizing the percentages of the lake polygons per buffer/settlement as stated above.
arcpy.Statistics_analysis(interLake100, SumLakeBuff100, "Percent SUM", "Fundort")
arcpy.Statistics_analysis(interLake500, SumLakeBuff500, "Percent SUM", "Fundort")
arcpy.Statistics_analysis(interLake1000, SumLakeBuff1000, "Percent SUM", "Fundort")
arcpy.Statistics_analysis(interLake5000, SumLakeBuff5000, "Percent SUM", "Fundort")


#*****************************
# visualisation in a bar plot
#*****************************

#Visualisation in a bar plot for the 100 m buffer
LakeAreadbf100= Dbf5(SumLakeBuff100) #Convert dBase-File into a data frame
dfLakeArea100= LakeAreadbf100.to_dataframe() #Convert dbf-File into a data frame
plt.hist(dfLakeArea100["SUM_Percen"],bins=56) #Command for a histogramm and how many bars you want to have displayed. In this case 56 were chosen because there are 56 settlements.
plt.xlabel("%") #The name of the x-axis
plt.ylabel ("number of villages") #The name of the y-axis
plt.title("Lake area per village, 100 m") #The title of the figure
plt.show() #Pop-up of the figure
plt.savefig(myworkspace + "/" +"Results" + "/" + "histolakerea100.png") #Saving the figure as a png


#Visualisation in a bar plot for the 500 m buffer
LakeAreadbf500= Dbf5(SumLakeBuff500) #Convert dBase-File into a data frame
dfLakeArea500= LakeAreadbf500.to_dataframe() #Convert dbf-File into a data frame
plt.hist(dfLakeArea500["SUM_Percen"],bins=56) #Command for a histogramm and how many bars you want to have displayed. In this case 56 were chosen because there are 56 settlements.
plt.xlabel("%") #The name of the x-axis
plt.ylabel ("number of villages") #The name of the y-axis
plt.title("Lake area per village, 500 m") #The title of the figure
plt.show() #Pop-up of the figure
plt.savefig(myworkspace + "/" +"Results" + "/" + "histolakerea500.png") #Saving the figure as a png


#Visualisation in a bar plot for the 1000 m buffer
LakeAreadbf1000= Dbf5(SumLakeBuff1000) #Convert dbf-File into a data frame
dfLakeArea1000= LakeAreadbf1000.to_dataframe() #Convert dbf-File into a data frame
plt.hist(dfLakeArea1000["SUM_Percen"],bins=56) #Command for a histogramm and how many bars you want to have displayed. In this case 56 were chosen because there are 56 settlements.
plt.xlabel("%") #The name of the x-axis
plt.ylabel ("number of villages") #The name of the y-axis
plt.title("Lake area per village, 1000 m") #The title of the figure
plt.show() #Pop-up of the figure
plt.savefig(myworkspace + "/" +"Results" + "/" + "histolakerea1000.png") #Saving the figure as a png


#Visualisation in a bar plot for the 5000 m buffer
LakeAreadbf5000= Dbf5(SumLakeBuff5000) #Convert dbf-File into a data frame
dfLakeArea5000= LakeAreadbf5000.to_dataframe() #Convert dbf-File into a data frame
plt.hist(dfLakeArea5000["SUM_Percen"],bins=56) #Command for a histogramm and how many bars you want to have displayed. In this case 56 were chosen because there are 56 settlements.
plt.xlabel("%") #The name of the x-axis
plt.ylabel ("number of villages") #The name of the y-axis
plt.title("Lake area per village, 5000 m") #The title of the figure
plt.show() #Pop-up of the figure
plt.savefig(myworkspace + "/" +"Results" + "/" + "histolakerea5000.png") #Saving the figure as a png


#****************************************************************************
#Calculating the mean, the standard deviation and the coefficient of variance
#****************************************************************************

#For the 100 m buffer
arcpy.Statistics_analysis(SumLakeBuff100, myworkspace +"/" + "Results" + "/" + "StatisticsLake100.dbf", "SUM_Percen MEAN;SUM_Percen STD", "") #Function for calculation of the mean and the standard deviation
statisticsLake100dbf= Dbf5(myworkspace + "/" + "Results" + "/" "StatisticsLake100.dbf") #Convert dBase-File into a data frame
statisticsLake100= statisticsLake100dbf.to_dataframe() #Convert dBase-File into a data frame
statisticsLake100mean= statisticsLake100["MEAN_SUM_P"] #Setting variable of the mean
statisticsLake100std= statisticsLake100["STD_SUM_Pe"] #Setting variable of the standard deviation

COVLake100= statisticsLake100std*100/statisticsLake100mean #Coefficient of variance
print COVLake100


#For the 500 m buffer
arcpy.Statistics_analysis(SumLakeBuff500, myworkspace +"/" + "Results" + "/" + "StatisticsLake500.dbf", "SUM_Percen MEAN;SUM_Percen STD", "") #Function for calculation of the mean and the standard deviation
statisticsLake500dbf= Dbf5(myworkspace + "/" + "Results" + "/" "StatisticsLake500.dbf") #Convert dBase-File into a data frame
statisticsLake500= statisticsLake500dbf.to_dataframe() #Convert dBase-File into a data frame
statisticsLake500mean= statisticsLake500["MEAN_SUM_P"] #Setting variable of the mean
statisticsLake500std= statisticsLake500["STD_SUM_Pe"] #Setting variable of the Standard deviation

COVLake500= statisticsLake500std*100/statisticsLake500mean #Coefficient of variance
print COVLake500


#For the 1000 m buffer
arcpy.Statistics_analysis(SumLakeBuff1000, myworkspace +"/" + "Results" + "/" + "StatisticsLake1000.dbf", "SUM_Percen MEAN;SUM_Percen STD", "") #function for calculation of the mean and the standard deviation
statisticsLake1000dbf= Dbf5(myworkspace + "/" + "Results" + "/" "StatisticsLake1000.dbf") #Convert dBase-File into a data frame
statisticsLake1000= statisticsLake1000dbf.to_dataframe() #Convert dBase-File into a data frame
statisticsLake1000mean= statisticsLake1000["MEAN_SUM_P"] #Setting variable of the mean
statisticsLake1000std= statisticsLake1000["STD_SUM_Pe"] #Setting variable of the Standard deviation

COVLake1000= statisticsLake1000std*100/statisticsLake1000mean #Coefficient of variance
print COVLake1000


#For the 5000 m buffer
arcpy.Statistics_analysis(SumLakeBuff5000, myworkspace +"/" + "Results" + "/" + "StatisticsLake5000.dbf", "SUM_Percen MEAN;SUM_Percen STD", "") #function for calculation of the mean and the standard deviation
statisticsLake5000dbf= Dbf5(myworkspace + "/" + "Results" + "/" "StatisticsLake5000.dbf")  #Convert dBase-File into a data frame
statisticsLake5000= statisticsLake5000dbf.to_dataframe() #Convert dBase-File into a data frame
statisticsLake5000mean= statisticsLake5000["MEAN_SUM_P"] #Setting variable of the mean
statisticsLake5000std= statisticsLake5000["STD_SUM_Pe"] #Setting variable of the Standard deviation

COVLake5000= statisticsLake5000std*100/statisticsLake5000mean #Coefficient of variance
print COVLake5000
