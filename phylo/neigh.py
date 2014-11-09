from itertools import combinations

#read in distance matrix from file named "input"
f = open('input')
lines = f.read().rstrip().split('\n')
nodes = lines[0].split(',')
D = [[float(s) for s in line.split(',')] for line in lines[1:]]
#create dictionary of values
d = {}
for i, n1 in enumerate(nodes):
    d[n1] = {}
    for j, n2 in enumerate(nodes):
        d[n1][n2] = D[i][j]

def find_min():
    min_d = float("inf")
    min_pair = (nodes[0], nodes[0])
    for n1, n2 in combinations(nodes, 2):
        dist = (len(nodes)-2)*d[n1][n2] - sum([d[n1][nk] for nk in nodes]) \
                - sum([d[n2][nk] for nk in nodes]) 
        if dist < min_d:
            min_d = dist
            min_pair = (n1, n2)
    return (min_d, min_pair)

def build():
    nodes.remove(min_pair[0])
    nodes.remove(min_pair[1])

    d[min_pair] = {}
    for node in nodes:
        if node not in min_pair:
            d[min_pair][node] = .5*(d[min_pair[0]][node] + d[min_pair[1]][node] - d[min_pair[0]][min_pair[1]])
            d[node][min_pair] = d[min_pair][node]
    d[min_pair][min_pair] = 0
    nodes.append(min_pair)

while len(nodes) > 1:
    min_d, min_pair = find_min()
    build()
print nodes[0]

