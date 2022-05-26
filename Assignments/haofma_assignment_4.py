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
# Problem 1 (20 points)
#
# Given an input point feature class (e.g., facilities or hospitals) and a polyline feature class, i.e., bike_routes:
# Calculate the distance of each facility to the closest bike route and append the value to a new field.
#
######################################################################
import arcpy
import os

def calculateDistanceFromPointsToPolylines(input_geodatabase, fcPoint, fcPolyline):
    try:
        arcpy.env.workspace = input_geodatabase
        featureclasses = arcpy.ListFeatureClasses()
        arcpy.env.overwriteOutput = True

        out_table = 'distance_' + fcPoint + '_near_' + fcPolyline

        # Calculate the distance of each point feature to the closest line feature and generate a table.
        arcpy.GenerateNearTable_analysis(fcPoint, fcPolyline, out_table)

        # Join the distance table as a field to the point feature's attribute table.
        arcpy.management.JoinField(fcPoint, 'OBJECTID', out_table, 'OBJECTID')

    except:
      print('At least one input feature is not valid, or the database path is wrong.')
######################################################################
# Problem 2 (30 points)
#
# Given an input point feature class, i.e., facilities, with a field name (FACILITY) and a value ('NURSING HOME'), and a polygon feature class, i.e., block_groups:
# Count the number of the given type of point features (NURSING HOME) within each polygon and append the counts as a new field in the polygon feature class
#
######################################################################
def countPointsByTypeWithinPolygon(input_geodatabase, fcPoint, pointFieldName, pointFieldValue, fcPolygon):
    try:
        arcpy.env.workspace = input_geodatabase
        featureclasses = arcpy.ListFeatureClasses()
        arcpy.env.overwriteOutput = True

        # define variables that are required for using SummarizeWithin method
        count_feature_class = pointFieldName + '_within_' + fcPolygon
        count_table = 'count_table_' + pointFieldName + '_within_' + fcPolygon

        # Count the number of fcPoint within each fcPolygon using the attribute pointFieldName for grouping.
        # This will make ArcGis count the number of fcPoint seperately for each value of the attribute pointFieldName.
        # The count will be stored in the table which name is defined by the variable "count_table" above.
        arcpy.analysis.SummarizeWithin(fcPolygon, fcPoint, count_feature_class, 'KEEP_ALL', '#', 'ADD_SHAPE_SUM', '#', pointFieldName, '#', '#', count_table)


        # Use update cursor to keep only the count records for pointFieldValue (i.e., the specified value of pointFieldName).
        with arcpy.da.UpdateCursor(count_table, [pointFieldName]) as cursor:
            # Delet the record (row) if the value of pointFieldName is not the specified one
            for row in cursor:
                if row[0] != pointFieldValue:
                    cursor.deleteRow()

        # Join the count of pointFieldValue as a field to the polygon feature's attribute table.
        arcpy.management.JoinField(fcPolygon, 'OBJECTID', count_table, 'Join_ID', [pointFieldName, 'Point_Count'])

        # Rename the relevant polygon fileds to make them be descriptive and unique,
        # but only if the names have not been renamed (in case the function has already been executed more than once).
        polygon_fields = arcpy.ListFields(input_geodatabase + "/" + fcPolygon)

        # Rename the name attribute of the type of point feature if the name has not been taken
        name_type_point_field_new_name = pointFieldName + '_' + pointFieldValue[: 3].replace(' ', '_')
        if name_type_point_field_new_name in polygon_fields_names:
            pass
        else:
            arcpy.management.AlterField(input_geodatabase + "/" + fcPolygon, pointFieldName, name_type_point_field_new_name)

        # Rename the count attribute of the type of point feature if the name has not been taken
        count_type_point_field_new_name = 'Point_Count_' + pointFieldValue[: 3].replace(' ', '_')
        if count_type_point_field_new_name in polygon_fields_names:
            pass
        else:
            arcpy.management.AlterField(input_geodatabase + "/" + fcPolygon, 'Point_Count', count_type_point_field_new_name)

        # Collect the names of the attributes in the polygon fearure class
        polygon_fields_names = []
        for field in polygon_fields:
        polygon_fields_names.append(field.name)

        # Delete the temorary layers and tables that are no longer needed.
        arcpy.management.Delete(count_table)
        arcpy.management.Delete(count_feature_class)

    except:
        print('At least one input feature, or the feature value, is not valid.')
######################################################################
# Problem 3 (50 points)
#
# Given a polygon feature class, i.e., block_groups, and a point feature class, i.e., facilities,
# with a field name within point feature class that can distinguish categories of points (i.e., FACILITY);
# count the number of points for every type of point features (NURSING HOME, LIBRARY, HEALTH CENTER, etc.) within each polygon and
# append the counts to a new field with an abbreviation of the feature type (e.g., nursinghome, healthcenter) into the polygon feature class

# HINT: If you find an easier solution to the problem than the steps below, feel free to implement.
# Below steps are not necessarily explaining all the code parts, but rather a logical workflow for you to get started.
# Therefore, you may have to write more code in between these steps.

# 1- Extract all distinct values of the attribute (e.g., FACILITY) from the point feature class and save it into a list
# 2- Go through the list of values:
#    a) Generate a shortened name for the point type using the value in the list by removing the white spaces and taking the first 13 characters of the values.
#    b) Create a field in polygon feature class using the shortened name of the point type value.
#    c) Perform a spatial join between polygon features and point features using the specific point type value on the attribute (e.g., FACILITY)
#    d) Join the counts back to the original polygon feature class, then calculate the field for the point type with the value of using the join count field.
#    e) Delete uncessary files and the fields that you generated through the process, including the spatial join outputs.
######################################################################
def countCategoricalPointTypesWithinPolygons(fcPoint, pointFieldName, fcPolygon, workspace):
    try:
        arcpy.env.workspace = workspace
        featureclasses = arcpy.ListFeatureClasses()
        arcpy.env.overwriteOutput = True

        # Use a search cursor to collect the values of the attribute pointFieldName
        with arcpy.da.SearchCursor(fcPoint, [pointFieldName]) as cursor:
            type_point_field = []
            for row in cursor:
                type_point_field.append(row[0])

        # Remove the repetitive values and get a clear list
        type_point_field = list(set(type_point_field))

        # For each value of the attribute pointFieldName, execute the function countPointsByTypeWithinPolygon
        for thistype in type_point_field:
            input_geodatabase = workspace
            pointFieldValue = thistype
            countPointsByTypeWithinPolygon(workspace, fcPoint, pointFieldName, pointFieldValue, fcPolygon)
            # Delete the unnecessary attribute "Join_ID"
            arcpy.DeleteField_management(input_geodatabase + "/" + fcPolygon, ['Join_ID'])
    except:
        print('At least one input feature, or the feature value, is not valid.')

######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
