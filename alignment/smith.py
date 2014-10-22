import numpy as np
import operator
x = 'ACACACTAGAGCTTTA' 
y = 'AGCACACATTAACTAC' 
d = -1
match = +2
transition = -1
transversion = -2
purines = ('A', 'G')
pyrimidines = ('T', 'C')
grid = np.arange((len(x)+1)*(len(y)+1)*2).reshape(len(x)+1, len(y)+1, 2)

def s(i, j):
    if x[i-1] == y[j-1]:
        return match
    else:
        if (x[i-1] in purines and y[j-1] in purines) or (x[i-1] in pyrimidines and y[j-1] in pyrimidines):
            return transition
        else:
            return transversion

def F(i, j):
    if (i, j) == (0, 0):
        grid[i,j] = [0,0]
        return 0
    else:
        if i > 0 and j > 0:
            index, value = max(enumerate([grid[i - 1, j - 1][0] + s(i, j), grid[i-1, j][0] + d, grid[i, j -1][0] + d, 0]), key=operator.itemgetter(1))
            grid[i,j] = [value,index]
            return value
        if i > 0:
            value = grid[i-1, j][0] + d
            if value <= 0:
                grid[i, j] = [0, 3]
            else:
                grid[i,j] = [value,1]
            return value 
        else:
            value = grid[i, j - 1][0] + d
            if value <= 0:
                grid[i, j] = [0, 3]
            else:
                grid[i, j] = [value,2]
            return value 
for i in range(len(x)+1):
    for j in range(len(y)+1):
        F(i,j)

arrows = []
max_coords = (0,0)
max_value = 0

for i in range(len(x)+1):
    for j in range(len(y)+1):
        if grid[i,j][0] > max_value:
            max_value = grid[i, j][0]
            max_coords = (i,j)
print "score:", max_value
(i, j) = max_coords

while((i > 0 or j > 0) and grid[i, j][1] != 3):
    arrows.append(grid[i,j][1])
    if grid[i,j][1] == 0:
        i -= 1
        j -= 1
    elif grid[i,j][1] == 1:
        i -= 1
    elif grid[i,j][1] == 2:
        j -= 1
xout = []
yout = []

for arrow in reversed(arrows):
    if arrow == 0:
        xout.append(x[i])
        yout.append(y[j])
        i += 1
        j += 1
    elif arrow == 2:
        xout.append('-')
        yout.append(y[j])
        j += 1
    elif arrow == 1:
        xout.append(x[i])
        yout.append('-')
        i += 1

for x in xout:
    print x,
print " "
for y in yout:
    print y,
print " "
