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

######################################################################
# Problem 1 (30 Points)
#
# Given a polygon feature class in a geodatabase, a count attribute of the feature class(e.g., population, disease count):
# this function calculates and appends a new density column to the input feature class in a geodatabase.

# Given any polygon feature class in the geodatabase and a count variable:
# - Calculate the area of each polygon in square miles and append to a new column
# - Create a field (e.g., density_sqm) and calculate the density of the selected count variable
#   using the area of each polygon and its count variable(e.g., population)
#
# 1- Check whether the input variables are correct(e.g., the shape type, attribute name)
# 2- Make sure overwrite is enabled if the field name already exists.
# 3- Identify the input coordinate systems unit of measurement (e.g., meters, feet) for an accurate area calculation and conversion
# 4- Give a warning message if the projection is a geographic projection(e.g., WGS84, NAD83).
#    Remember that area calculations are not accurate in geographic coordinate systems.
#
######################################################################
import arcpy
import os

def calculateDensity(fcpolygon, attribute, geodatabase):
    arcpy.env.workspace = geodatabase
    featureclasses = arcpy.ListFeatureClasses()
    arcpy.env.overwriteOutput = True

    # Check if the input fcpolygon is correct.
    try:
        fcpolygon_desc = arcpy.Describe(geodatabase + "/" + fcpolygon)
    except OSError:
        print('The input fcpolygon is not valid.')
        return # If the name of input fcpolygon is incorrect, print the warning and exit the function here.

    if fcpolygon_desc.shapeType != 'Polygon':
        print('The shape type of the input fcpolygon must be polygon.') # If the type of the input fcpolygon is incorrect, print the warning and skip the below lines here.
    else:

        # Check if the input attribute is correct.
        fields = arcpy.ListFields(fcpolygon)

        field_name = [] # A list to collect the names of fields
        for field in fields:
            field_name.append(field.name)

        if attribute not in field_name: # Check if the input attribute exists in the input fcpolygon.
            print('The input attribute does not exist in the input fcpolygon.')  # If the input attribute is incorrect, print the warning and skip the below lines here.
        else:

            # Identify the projection and measurement units of the input fcpolygon.
            fcpolygon_reference = fcpolygon_desc.spatialReference
            fcpolygon_projection = fcpolygon_reference.GCS.Name

            if 'WGS' in fcpolygon_projection or 'NAD' in fcpolygon_projection:
                print('The projection is a geographic projection and therefore the area calculaton is not accurate.')
            else:
                pass

            fcpolygon_unit = fcpolygon_reference.linearUnitName

            converter = 1 # A unit converter to mile
            if fcpolygon_unit == 'Meter':
                converter = 0.00062137119224
            else:
                pass

            # Add a new field of area in squared miles
            arcpy.AddField_management(fcpolygon, 'Shape_Area_Squared_Miles', 'FLOAT')

            # Add a new field of the density of the input attribute
            attribute_density_name = attribute + "_density"
            arcpy.AddField_management(fcpolygon, attribute_density_name, 'FLOAT')

            # Calculate the polygon area in squared miles, and then calculate the density of the input attribute
            try:
                with arcpy.da.UpdateCursor(fcpolygon, ['Shape_Area', 'Shape_Area_Squared_Miles', attribute, attribute_density_name]) as cursor:
                    for row in cursor:
                        row[1] = row[0] * converter * converter # Caculate the area in squared miles
                        row[3] = row[2]/row[1]
                        cursor.updateRow(row)
            except TypeError: # If the input attribute is not numeric, print the warning and delete the density field.
                print('Density cannot be calculated. Possible reason might be that the input attribute is not numeric.')
                arcpy.management.DeleteField(geodatabase + '/' + fcpolygon, [attribute_density_name])
######################################################################
# Problem 2 (40 Points)
#
# Given a line feature class (e.g.,river_network.shp) and a polygon feature class (e.g.,states.shp) in a geodatabase,
# id or name field that could uniquely identify a feature in the polygon feature class
# and the value of the id field to select a polygon (e.g., Iowa) for using as a clip feature:
# this function clips the linear feature class by the selected polygon boundary,
# and then calculates and returns the total length of the line features (e.g., rivers) in miles for the selected polygon.
#
# 1- Check whether the input variables are correct (e.g., the shape types and the name or id of the selected polygon)
# 2- Transform the projection of one to other if the line and polygon shapefiles have different projections
# 3- Identify the input coordinate systems unit of measurement (e.g., meters, feet) for an accurate distance calculation and conversion
#
######################################################################
def estimateTotalLineLengthInPolygons(fcLine, fcClipPolygon, polygonIDFieldName, clipPolygonID, geodatabase):
    arcpy.env.workspace = geodatabase
    featureclasses = arcpy.ListFeatureClasses()
    arcpy.env.overwriteOutput = True

    # Check if the input fcpolygon is correct.
    try:
        fcClipPolygon_desc = arcpy.Describe(geodatabase + "/" + fcClipPolygon)
    except OSError:
        print('The input fcClipPolygon is not valid.')
        return # If the name of input fcClipPolygon is incorrect, print the warning and exit the function here.

    if fcClipPolygon_desc.shapeType == 'Polygon':
        pass
    else:
        print('The shape type of the input fcClipPolygon must be polygon.')
        return # If the type of the input fcClipPolygon is incorrect, print the warning and skip the below lines here.

    # Check if the input fcLine is correct.
    try:
        fcLine_desc = arcpy.Describe(geodatabase + "/" + fcLine)
    except OSError:
        print('The input fcLine is not valid.')
        return # If the name of input fcLine is incorrect, print the warning and exit the function here.

    if fcLine_desc.shapeType == 'Polyline':
        pass
    else:
        print('The shape type of the input fcLine must be polyline.') # If the type of the input fcLine is incorrect, print the warning and skip the below lines here.
        return

    # Check if the ID field of the input fcClipPolygon is correct.
    fields_fcClipPolygon = arcpy.ListFields(fcClipPolygon)

    field_fcClipPolygon_name = [] # A list to collect the names of the fields of fcClipPolygon
    for field in fields_fcClipPolygon:
        field_fcClipPolygon_name.append(field.name)

    if polygonIDFieldName not in field_fcClipPolygon_name: # Check if the input polygonIDFieldName exists in the input fcClipPolygon.
        print('The input polygonIDFieldName does not exist in the input fcClipPolygon.')  # If the input polygonIDFieldName is incorrect, print the warning and skip the below lines here.
        return
    else:
        pass

    # Check if the ID value of the input fcClipPolygon is correct.
    with arcpy.da.SearchCursor(fcClipPolygon, [polygonIDFieldName]) as cursor:
        polygonIDFieldName_value = [] # A list to collect the values of the ID field
        for row in cursor:
            polygonIDFieldName_value.append(row[0])

    if clipPolygonID not in polygonIDFieldName_value: # Check if the input clipPolygonID exists in the input polygonIDFieldName.
        print('The input clipPolygonID is not a value of the input polygonIDFieldName.')  # If the input clipPolygonID is incorrect, print the warning and skip the below lines here.
        return
    else:
        pass

    # Identify the projection of the input fcClipPolygon.
    fcClipPolygon_reference = fcClipPolygon_desc.spatialReference
    fcClipPolygon_projection = fcpolygon_reference.GCS.Name

    # Identify the projection of the input fcLine.
    fcLine_reference = fcLine_desc.spatialReference
    fcLine_projection = fcLine_reference.GCS.Name

    # Transform the projection of the input fcLine to that of the input fcClipPolygon if they are not the same
    if fcLine_projection != fcClipPolygon_projection:
        fcLine_reprojected = fcLine + '_' + fcClipPolygon_projection
        arcpy.Project_management(fcLine, fcLine_reprojected, fcClipPolygon_reference)
        fcLine_name = fcLine # Keep the original input polyline name
        fcLine = fcLine_reprojected
        arcpy.management.Delete(fcLine_reprojected)
    else:
        pass

    # Identify the measurement units of the input fcClipPolygon
    # Since here the projection for both the polygon and the polyline should already be the same
    fcClipPolygon_unit = fcClipPolygon_reference.linearUnitName

    converter = 1 # A unit converter to mile
    if fcClipPolygon_unit == 'Meter': # If the linear unit is missing, the default should be meter
        converter = 0.00062137119224
    else:
        pass

    # Select the polygon feature by the input ID value
    where_clause = "\"" + polygonIDFieldName + "\"" + ' = '  + "\'" + clipPolygonID + "\'"
    arcpy.Select_analysis(fcClipPolygon, clipPolygonID, where_clause)

    # Clip the linear feature class by the selected polygon boundary
    fcClipped = fcLine + '_Clipped_by_' + clipPolygonID
    arcpy.analysis.Clip(fcLine, clipPolygonID, fcClipped)

    # Calculate the total length of the input fcLine
    with arcpy.da.SearchCursor(fcClipped, ['Shape_Length']) as cursor:
        length = 0
        for row in cursor:
            length += row[0] * converter

    return('The total length of ' + fcLine_name + ' within the polygon ' + clipPolygonID + ' is ' + str(round(length, 2)) + ' miles.')


######################################################################
# Problem 3 (30 points)
#
# Given an input point feature class, (i.e., eu_cities.shp) and a distance threshold and unit:
# Calculate the number of points within the distance threshold from each point (e.g., city),
# and append the count to a new field (attribute).
#
# 1- Identify the input coordinate systems unit of measurement (e.g., meters, feet, degrees) for an accurate distance calculation and conversion
# 2- If the coordinate system is geographic (latitude and longitude degrees) then calculate bearing (great circle) distance
#
######################################################################
def countObservationsWithinDistance(fcPoint, distance, distanceUnit, geodatabase):
    pass

######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
    print('### Otherwise, the Autograder will assign 0 points.')
