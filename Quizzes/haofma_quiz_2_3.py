"""
GEOG:5050 Geospatial Programming
Spring 2022
Quiz 2, Question 3

Haofeng Ma
"""

mynum = eval(input('Enter a list of numbers, separated by a comma: ')) # user enter a list of numbers

mylist = [] # an empty list used to collect all numbers entered
mylist_unique = [] # an empty list used to collect unqiue numbers only

for i in mynum:
    mylist.append(i) # collect each number into the list for all numbers
    if i not in mylist_unique: # if the number is not in the unique list
        mylist_unique.append(i) # then collect it into the list for unique numbers

if mylist == mylist_unique:
# if the list for all numbers are the same with the list for unique numbers
# it necessarily means that there is no duplicate value
    print('The list provided does not contain duplicate values')
else:
# or else, it necessarily means that at least one value appears more than one time
    print('The list provided contains duplicate values')


