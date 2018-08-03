import arcpy
import pandas
import matplotlib.pyplot as plt
from simpledbf import Dbf5

if arcpy.CheckExtension("Spatial") == "Available":
    arcpy.CheckOutExtension('Spatial') #Checkout the extension
else:
    print "no spatial analyst license available" #Checkout if the extension is working



#*******************************
#Set environemnt and workspace
#*******************************
myworkspace="D:/Unibern/Geographie/Master/Geodatenanalyse/Projekt/MeineToolbox/ToolData"
print "Workspace: " + myworkspace
arcpy.env.workspace= myworkspace #Workspace is set
arcpy.env.overwriteOutput = True #Allows to overwrite other files (e.g. to overwrite tables)


#*********************************************
#Reading in the settlment and river shapefiles
#*********************************************

#Settlement shapefile:
Settlements = myworkspace + "/" + "Siedlungen" + "/" + "CH_SiedlungenLV03.shp" #Reading in the settlement shapefile
Settldbf = myworkspace + "/" + "Siedlungen" + "/" + "CH_SiedlungenLV03.dbf" #Reading in the settlement dBase file

#River shapefile:
Rivers= myworkspace + "/" + "Landcover" + "/" + "Fluesse.shp" #Reading in the river shapefile


#**********************************************************
#Near function -> determine the nearest distance to a river
#**********************************************************

#This function determines which is the nearest river to each settlment and also saves the distance in the attribute table of the settlement shapefile.
arcpy.Near_analysis(Settlements, Rivers, "", "NO_LOCATION", "NO_ANGLE", "PLANAR")


#*****************************
# visualisation in a bar plot
#*****************************

Riverdbf= Dbf5(Settldbf) #Convert dBase file into a data frame
dfRiver= Riverdbf.to_dataframe() #Convert dBase file into a data frame
plt.hist(dfRiver["NEAR_DIST"],bins=56) #Command for a histogramm and how many bars you want to have displayed. In this case 56 were chosen because there are 56 settlments.
plt.xlabel("m") #Here you set your name for the x-axis
plt.ylabel ("number of villages") #Here you set your name for the y-axis
plt.title("Distance to nearest river") #Title of the plot
plt.show() #Pop-up of the figure
plt.savefig(myworkspace + "/" +"Results" + "/" + "historiver.png") #Saving the plot as a png


#*******************************************************************************************
#Calculate the mean, the standard deviation and the COV of the distance to the nearest river
#*******************************************************************************************

arcpy.Statistics_analysis(Settldbf, myworkspace +"/" + "Results" + "/" + "StatisticsRivers.dbf", "NEAR_DIST MEAN;NEAR_DIST STD", "") #Function for calculation of the mean and the standard deviation

statisticsRiversdbf= Dbf5(myworkspace + "/" + "Results" + "/" "StatisticsRivers.dbf") #Convert dBase file into a data frame
statisticsRivers= statisticsRiversdbf.to_dataframe() #Convert dBase file into a data frame
statisticsRiversmean= statisticsRivers["MEAN_NEAR_"] #Setting variable of the mean
statisticsRiversstd= statisticsRivers["STD_NEAR_D"] #Setting variable of the Standard deviation

coefficientRivers=statisticsRiversstd*100/statisticsRiversmean #Coefficient of variance
print coefficientRivers
