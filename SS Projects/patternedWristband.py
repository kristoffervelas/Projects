"""
A wristband can have 4 patterns:

horizontal: each item in a row is identical.
vertical: each item in each column is identical.
diagonal left: each item is identical to the one on its upper left or bottom right.
diagonal right: each item is identical to the one on its upper right or bottom left.


Write a function that returns True if the section can be correctly classified into one of the 4 types, and False otherwise.

ex:

["A", "B"],
["A", "B"],
["A", "B"]
"""

#checks if all the elements in the same row are the same.
def horizontalCheck(wristband):
    for row in wristband:
        if(len(set(row)) == 1):
            return True

#checks if all the elements in the same column are the same
def verticalCheck(wristband):
    for col in range(len(wristband[0])):
        column = []
        for row in wristband:
            column.append(row[col])
        if(len(set(column)) == 1):
            return True

#does same as below but polarized.
def diagonalLeftCheck(wristband):
    for row in range(len(wristband)):
        for col in range(len(wristband[row])):
            if wristband[row][col] == wristband[row + 1][col + 1]:
                return True
            else: 
                return False

#compares every iteration to the element on the next row and next column.
def diagonalRightCheck(wristband):
    for row in range(len(wristband)):
        for col in range(len(wristband[row])):
            if wristband[row][col] == wristband[row - 1][col - 1]:
                return True
            else:
                return False

#applies all the check functions at once to the 2d list.
def checkPattern(wristband):
    if (horizontalCheck(wristband) == True) or (verticalCheck(wristband) == True) or (diagonalLeftCheck(wristband) == True) or (diagonalRightCheck(wristband) == True):
        print("True")
    else:
        print("False")

test1 = [["V", "B", "C"],
         ["G", "A", "B"],
         ["C", "G", "A"]]


test2 = [["A", "B", "C"],
         ["G", "A", "B"],
         ["C", "G", "A"]]


checkPattern(test1)
checkPattern(test2)

#problem is in line 37 and 46 because you need to get the index of the iterator row and col since they are not integer, but instead they are letters. Find a way to get the index of the iterators.

#https://edabit.com/challenge/grorumaEjyFDmZQCx
