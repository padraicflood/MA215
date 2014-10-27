import numpy as np
import operator
#scoring scheme
x = 'ACGT' 
y = 'AGCCG' 
d = -2
match = +1
transition = -1
transversion = -2
purines = ('A', 'G')
pyrimidines = ('T', 'C')
n = 0
grid = np.arange((len(x)+1)*(len(y)+1)*2).reshape(len(x)+1, len(y)+1, 2)
grid[0,0] = [0,0]
def s(i, j):
    if x[i-1] == y[j-1]:
        return match
    else:
        if (x[i-1] in purines and y[j-1] in purines) or (x[i-1] in pyrimidines and y[j-1] in pyrimidines):
            return transition
        else:
            return transversion
def F(i, j):
    global n
    n += 1
    if (i, j) == (0, 0):
        return 0
    else:
        if i > 0 and j > 0:
            index, value = max(enumerate([grid[i - 1, j - 1][1] + s(i, j), grid[i-1, j][1] + d, grid[i, j -1][1] + d]), key=operator.itemgetter(1))
            grid[i,j] = [index, value]
            return value
        if i > 0:
            grid[i,j] = [1, grid[i-1,j][1] + d]
            return  grid[i-1, j][1] + d
        else:
            grid[i, j] = [2, grid[i, j-1][1] + d]
            return grid[i, j - 1][1] + d
for i in range(0, len(x)+1):
    for j in range(0, len(y)+1):
        F(i,j)
print "score: ", grid[len(x),len(y)][1]
arrows = []

i = len(x)
j = len(y)

while(i > 0 or j > 0):
    index = grid[i,j][0]
    arrows.append(index)
    if index == 0:
        i -= 1
        j -= 1
    elif index == 1:
        i -= 1
    elif index == 2:
        j -= 1
xout = []
yout = []
i, j = 0, 0
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
