f = open('make_seq.out')
data = f.read().split('\n')[:-1]

reads = set(data[1:])
answer = data[1]

vertices = set()
n = 17 
for read in reads:
    for i in range(n):
        vertices.add(read[i:-(n-i)])
    vertices.add(read[n:])
#one of the reads isn't 25 in length (probably because it goes over hte end of the seqence and doesn't loop

graph = {}
print len(vertices)
for start in vertices:
    ends = []
    for end in vertices:
        if end.startswith(start[1:]):
            ends.append(end)
    graph[start] = ends
    if ends == []:
        print start
v = 'TCCGCACC'
cycles = []
for v in graph:
    if len(graph[v]) % 2 != 0:
        print 'not euler'
def graph_not_empty():
    for v in graph:
        if graph[v] != []:
            return True
    return False
while graph_not_empty():
    c = []
    for v_i in graph:
        if graph[v_i] != []:
            v = v_i
            break
    while graph[v] != []:
        c.append(v)
        old_v = v
        v = graph[v][0]
        del graph[old_v][0]
    cycles.append(c)

cycle = cycles[0]
del cycles[0]
while cycles != []:
    for i, v in enumerate(cycle):
        for c in cycles:
            if v in c:
                p = c.index(v)
                cycle[i:i] = c[p:] + c[:p]
                cycles.remove(c)
s = ''
print cycles
