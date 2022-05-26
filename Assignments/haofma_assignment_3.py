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
# Problem 1 (10 Points)
#
# This function reads all the feature classes in a workspace (folder or geodatabase) and
# prints the name of each feature class and the geometry type of that feature class in the following format:
# 'states is a point feature class'

###################################################################### 
import arcpy
import os

def printFeatureClassNames(workspace):
    try:
        # set the working environment directory
        arcpy.env.workspace = workspace
        
        # collect featureclass
        featureclasses = arcpy.ListFeatureClasses()
        
        # for each featureclass
        for fc in featureclasses:
            # describe the shape of the featureclass
            desc = arcpy.Describe(fc)
            # print the name and the shape of the featureclass
            print('{0} is a {1} feature class'.format(fc, desc.shapeType))
    except TypeError:
        return 'TypeError raised.'
    except:
        return 'Error raised.'

###################################################################### 
# Problem 2 (20 Points)
#
# This function reads all the attribute names in a feature class or shape file and
# prints the name of each attribute name and its type (e.g., integer, float, double)
# only if it is a numerical type

###################################################################### 
def printNumericalFieldNames(inputFc, workspace):
    try:
        # set the working environment directory
        arcpy.env.workspace = workspace
        
        # collect field list
        fields = arcpy.ListFields(inputFc)
        
        # for each field, print the name and type if the type is numeric (including "Integer", "Double", "Single", and "SmallInteger")
        for field in fields:
            if field.type == 'Integer' or field.type == 'Double' or field.type == 'Single' or field.type == 'SmallInteger':
                print('The type of arrtibute {0} is {1} '.format(field.name, field.type))    
    except TypeError:
        return 'TypeError raised.'
    except:
        return 'Error raised.'

###################################################################### 
# Problem 3 (30 Points)
#
# Given a geodatabase with feature classes, and shape type (point, line or polygon) and an output geodatabase:
# this function creates a new geodatabase and copying only the feature classes with the given shape type into the new geodatabase

###################################################################### 
def exportFeatureClassesByShapeType(input_geodatabase, shapeType, output_geodatabase):
    try:
        # extract output geodatabase name from the function input
        outgdb_name = os.path.basename(output_geodatabase)
        
        # extract output directory path from the function input
        out_dir_path = os.path.dirname(os.path.realpath(output_geodatabase))
        
        # set the working environment directory
        arcpy.env.workspace = input_geodatabase
        
        # collect featureclass
        featureclasses = arcpy.ListFeatureClasses()
        
        outgdb = arcpy.CreateFileGDB_management(out_dir_path, outgdb_name)
        
        for fc in featureclasses:
            desc = arcpy.Describe(fc)
            if desc.shapeType == shapeType:
                arcpy.conversion.FeatureClassToGeodatabase(fc, outgdb)
        
        print('Done')
    
    except TypeError:
        return 'TypeError raised.'
    except:
        return 'Error raised.'

###################################################################### 
# Problem 4 (40 Points)
#
# Given an input feature class or a shape file and a table in a geodatabase or a folder workspace,
# join the table to the feature class using one-to-one and export to a new feature class.
# Print the results of the joined output to show how many records matched and unmatched in the join operation. 

###################################################################### 
def exportAttributeJoin(inputFc, idFieldInputFc, inputTable, idFieldTable, workspace):    
    try:
    # extract input table name from the function input
        inputTable_name = os.path.basename(inputTable)
        
        # set the working environment directory
        arcpy.env.workspace = workspace
        
        joined_table = arcpy.AddJoin_management(inputFc, idFieldInputFc, inputTable, idFieldTable, "KEEP_ALL")
        
        # Copy the layer to a new permanent feature class
        arcpy.CopyFeatures_management(joined_table, 'joined_feature_class')
        
        # a searchcursor to obtain id list in the input feature class
        cursor = arcpy.da.SearchCursor('joined_feature_class', idFieldInputFc)
        idFieldInputFc_unique = []
        for row in cursor:
            idFieldInputFc_unique.append(row[0])
        del row
        del cursor
        idFieldInputFc_unique = list(set(idFieldInputFc_unique))
        
        # a searchcursor to obtain id list in the new feature class
        merged_id_name = inputTable_name.replace('.', '_') + '_' + idFieldTable
        cursor = arcpy.da.SearchCursor('joined_feature_class', merged_id_name)
        
        merged_id_unique = []
        total = 0
    
        for row in cursor:
            merged_id_unique.append(row[0])
            total += 1
            
        del row
        del cursor
        merged_id_unique = list(set(merged_id_unique))
    
        # compare two id lists to identify the numbers of matched and unmatched records
        matched = 0
        
        for i in merged_id_unique:
            if i in idFieldInputFc_unique:
                matched += 1
        
        unmatched = total - matched
        print(matched, 'records matched and', unmatched, 'records unmatched.')
    
    except TypeError:
        return 'TypeError raised.'
    except:
        return 'Error raised.'

######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
