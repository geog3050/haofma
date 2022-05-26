"""
GEOG:5050 Geospatial Programming
Spring 2022
Quiz 2, Question 1

Haofeng Ma
"""

myletter = input('Enter a letter: ').lower() # user enter a letter, not case sensitive
mystr = input('Enter a string: ').lower() # user enter a script, not case sensitive

occurrence = False # a condition variable to be used in the below loop to judge the letter occurrence 
        
for i in mystr: 
    if i == myletter: # judge the occurence for each letter of the script
        occurrence = True
        break # if the letter has occured, change the condition to "True" and the future loop is no longer needed

# print the resuly by condition
if occurrence == True:
    print('Yes (The letter occurs in the text)')
else:
    print('No (The letter does not occur in the text)')