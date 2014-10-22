import numpy as np
import operator
x = 'GAATTCCGTTA' 
y = 'GGATCGA' 
#scoring scheme:
o = -2
e = -1
match = +2
transition = -1
transversion = -1
purines = ('A', 'G')
pyrimidines = ('T', 'C')
#grid of arrows and values
grid = np.arange((len(x)+1)*(len(y)+1)*6).reshape(len(x)+1,len(y)+1,6)
# 0 M index, 1 M value
# 2 Ix index, 3 Ix value
# 4 Iy index, 5 Iy value
letter_to_num = {'C': 0, 'T': 1, 'A': 2, 'G': 3}
scoring_matrix = [
        [match, transition, transversion, transversion],#C 
        [transition, match, transversion, transversion],#T
        [transversion, transversion, match, transition],#A
        [transversion, transversion, transition, match] #G
        ]
def s(i, j):
    return scoring_matrix[letter_to_num[x[i-1]]][letter_to_num[y[j-1]]]
def Ix(i, j):
    if (i,j) == (0, 0):
        return [3,0]
    if i == 0:
        return [3,-999999]
    return max(enumerate([grid[i-1, j, 1] + o, grid[i-1, j, 3] + e]), key = operator.itemgetter(1))

def Iy(i, j):
    if (i, j) == (0, 0):
        return [3,0]
    if j == 0:
        return [3,-999999]
    index, value = max(enumerate([grid[i, j-1, 1] + o, grid[i, j-1, 5] + e]), key = operator.itemgetter(1))
    if index == 1:
        index = 2
    return [index,value]

def M(i,j):
    if (i, j) == (0, 0):
        return [3, 0]
    if i == 0 or j == 0:
        return [3,-999999]
    index, value = max(enumerate([grid[i-1, j-1, 1] + s(i, j), grid[i-1, j-1, 3] + s(i,j), grid[i-1, j-1, 5] + s(i,j)]), key = operator.itemgetter(1))
    return [index,value]

for i in range(len(x)+1):
    for j in range(len(y)+1):
        a = M(i,j)
        b = Ix(i,j)
        c = Iy(i,j)
        grid[i,j] = [a[0], a[1], b[0], b[1], c[0], c[1]]


arrows = []

i = len(x)
j = len(y)

index, value = max(enumerate([grid[i,j,1], grid[i,j,3], grid[i,j,5]]), key = operator.itemgetter(1))

while(i > 0 or j > 0):
    arrows.append(index)
    new_index = grid[i,j,index*2]
    if index == 0:
        i -= 1
        j -= 1
    elif index == 1:
        i -= 1
    elif index == 2:
        j -= 1
    index = new_index

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
print value
for x in xout:
    print x,
print " "
for y in yout:
    print y,
print " "
