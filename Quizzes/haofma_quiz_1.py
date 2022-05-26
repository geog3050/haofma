"""
GEOG:5050 Geospatial Programming
Spring 2022
Quiz 1

Haofeng Ma
"""

def thermotropic(): # define as a function, no argument needed

    climate = input('Please input the type of climate: ') # user inputs climate as a string
    
    climate = climate.lower() # convert climate to all lowercases
    
    temperature_input = str(input('Please input temperatures, separated by a comma: '))
    # the temperature input is stored as a string
    # but user can input either as a list, or as a string consists of values seperated by commas
    
    
    temperature_list = temperature_input.replace('[', '').replace(']', '').split(',')
    # remove brackets in case user input as a list, after which convert the string to a list
    
    temperature_list_float = [] # a list used to collect temperatures as floats
    
    for i in temperature_list:
        i = float(i)
        temperature_list_float.append(i)
    # this for loop coverts each element of the list "temperature_list" to a float
    # and then append the float-type temperature to the list "temperature_list_float"
    
    print('\n') # print a line to separate the input and the output part
    print('The status of the plant\'s leaves are: ') # print the titleline of output
    
    for i in temperature_list_float: # the below for loop is to judge the status of plants' leaves for each temperature input
        if climate == 'tropical': # if the climate input is tropical
            if i > 30: # and the temperature input is above the threshold of this type of climate
                print('F') # then plants' leaves are folded
            else:
                print('U') # otherwise they are unfolded       
        if climate == 'continental':  # if the climate input is continental
            if i > 25: # and the temperature input is above the threshold of this type of climate
                print('F') # then plants' leaves are folded
            else:
                print('U') # otherwise they are unfolded 
        if climate != 'tropical' and climate != 'continental' : # if the climate input is neither tropical nor continental
            if i > 18: # and the temperature input is above the threshold of this type of climate
                print('F') # then plants' leaves are folded
            else:
                print('U') # otherwise they are unfolded 