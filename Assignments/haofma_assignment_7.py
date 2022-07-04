###################################################################### 
# Edit the following function definition, replacing the words
# 'name' with your name and 'hawkid' with your hawkid.
# 
# Note: Your hawkid is the login name you use to access ICON, and not
# your firsname-lastname@uiowa.edu email address.
# 
# def hawkid():
#     return(["Caglar Koylu", "ckoylu"])
###################################################################### 
def hawkid():
    return(["Haofeng Ma", "haofma"])

##################################################################################################### 
# 100 Points Total
#
# Given a linear shapefile (roads) and a point shapefile representing facilities(schools),
# this function should generate either a time-based (1-,2-,3- minute) or road network distance-based (200-, 400-, 600-, .. -2000 meters)
# concentric service areas around facilities and save the results to a layer file on an output geodatabase.
# Although you are not required to map the result, make sure to check your output service layer feature.
# The service area polygons can be used to visualize the areas that do not have adequate coverage from the schools. 

# Each parameter is described below:

# inFacilities: The name of point shapefile (schools)     
# roads: The name of the roads shapefile
# workspace: The workspace folder where the shapefiles are located. 

# Below are suggested steps for your program. More code may be needed for exception handling
# and checking the accuracy of the input values.

# 1- Do not hardcode any parameters or filenames in your code.
#    Name your parameters and output files based on inputs. 
# 2- Check all possible cases where inputs can be in wrong type, different projections, etc. 
# 3- Create a geodatabase using arcpy and import all initial shapefiles into feature classes. All your processes and final output should be saved into
#    the geodatabase you created. Therefore, set the workspace parameter to the geodatabase once it is created.
# 4- Using the roads linear feature class, create and build a network dataset. Check the Jupyter notebook shared on ICON,
#    which covers the basics of how to create and build a network dataset from scratch. 
# 5- Use arcpy's MakeServiceAreaLayer function in the link below:
#    https://pro.arcgis.com/en/pro-app/tool-reference/network-analyst/make-service-area-layer.htm
#    Specify the following options while creating the new service area layer. Please make sure to read all the parameters needed for the function. 
#       If you use "length" as impedance_attribute, you can calculate concentric service areas using 200, 400, 600, .. 2000 meters for break values.
#       Feel free to describe your own break values, however, make sure to include at least three of them. 
#       Generate the service area polygons as rings, so that anyone can easily visualize the coverage for any given location if needed.
#       Use overlapping polygons to determine the number of facilities (schools) that cover a given location.
#       Use hierarchy to speed up the time taken to create the polygons.
#       Use the following values for the other parameters:
#       "TRAVEL_FROM", "DETAILED_POLYS", "MERGE"
#################################################################################################################### 
import arcpy

def calculateNetworkServiceArea(inFacilities, roads, workspace):
    # Check if the input shapefile names have an extension
    if ".shp" in roads:
        roads = roads[ :-4]
    else:
        pass
    
    if ".shp" in inFacilities:
        inFacilities = inFacilities[ :-4]
    else:
        pass
    
    arcpy.env.workspace = workspace
    arcpy.env.overwriteOutput = True
    
    roads_shp = workspace + "/" + roads + ".shp"
    inFacilities_shp = workspace + "/" + inFacilities + ".shp"
    
    # Acquire the spatial reference
    spatial_reference = arcpy.Describe(roads_shp).spatialReference
    
    # Create geodatabase
    arcpy.management.CreateFileGDB(workspace, "geodatabase")
    
    # Create a feature dataset
    arcpy.CreateFeatureDataset_management(workspace + "/geodatabase.gdb", "feature_dataset", spatial_reference)
    
    # Copy files into the geodatabase created
    arcpy.CopyFeatures_management(roads_shp, workspace + "/geodatabase.gdb/feature_dataset/" + roads)
    arcpy.CopyFeatures_management(inFacilities_shp, workspace + "/geodatabase.gdb/feature_dataset/" + inFacilities)
    
    # Set the workspace to the geodatabase created
    workspace = workspace + "/geodatabase.gdb/feature_dataset"
    
    # Create a network dataset
    arcpy.na.CreateNetworkDataset(workspace, "roads_ND", [roads])
    
    # Build Network
    arcpy.BuildNetwork_na(workspace + "/roads_ND")
    
    # Make service layer
    serviceL = arcpy.na.MakeServiceAreaLayer(workspace + "/roads_ND", "network_service_area", 
                                "length", "TRAVEL_FROM", "200 400 600 2000", "DETAILED_POLYS", 
                                "MERGE", "RINGS", "TRUE_LINES",
                                "OVERLAP")
######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
