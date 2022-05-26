"""
GEOG:5050 Geospatial Programming
Spring 2022
Quiz 2, Question 2

Haofeng Ma
"""

mynum = eval(input('Enter a list of numbers, separated by a comma: ')) # user enter a list of numbers

mylist = [] # an empty list used to collect numbers

for i in mynum:
    mylist.append(i) # collect each number into the list variable

mylist = sorted(mylist) # sort the list by the numeric order

print('The second-largest number you entered is: ', mylist[-2]) # the second to last element in the list is the second-largest number


