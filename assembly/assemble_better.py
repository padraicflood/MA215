import copy
f = open('make_seq.out')
data = f.read().split('\n')[:-1] #read in file, split on new lines and remove the new line character at the end
l = 25 #length of each read (assumed to be all equal length)
k = 12 #vertices of length k-1
#TODO: could write code to optimatize the value of k depending on l.

reads = set(data[1:]) #making it a set just to eliminate repeats
answer = data[0] #first line of file is the original sequence for comparison

#functions:

def cycle_not_empty(cycle, graph):
    for v in cycle:
        if graph[v] != []:
            return True
    return False

def find_cycle(v, graph):
    c = []
    while(graph[v] != []):
        c.append(v)
        old_v = v
        v = graph[v][-1]
        del graph[old_v][-1]
    return c
#called len(data) times
def find_sequence(graph, vertices, initial_v):
    cycle = find_cycle(initial_v, graph)
    while cycle_not_empty(cycle, graph):
        for i, v in enumerate(cycle):
            if graph[v] != []:
                partial_cycle = find_cycle(v, graph)
                cycle[i:i] = partial_cycle
                break
    assembled = initial_v[:-1]
    for v in cycle:
        assembled += v[-1]
    return assembled 

#split reads up into vertices of length k-1
def construct_vertices(reads, k, l):
    vertices = set()
    for read in reads:
        for i in range(1 - (k-1) + l):
            vertices.add(read[i: (k-1) + i])
    return vertices

#only called once
def construct_graph(vertices, reads):
    graph = {}
    for start in vertices:
        ends = []
        for end in vertices:
            if end.startswith(start[1:]):
                total = start + end[-1]
                for read in reads:
                    if total in read:
                        ends.append(end)
                        break
        graph[start] = ends
    return graph

vertices = construct_vertices(reads,k, l)
print len(vertices)

graph = construct_graph(vertices, reads)

longest = ''
length = 0

for i in range(1, len(data)):
        v = data[i][:k-1]
        graph_copy = copy.deepcopy(graph)
        assembled = find_sequence(graph_copy, vertices, v)
        if len(assembled) > length:
            longest = assembled
            length = len(assembled)
print longest, length 

