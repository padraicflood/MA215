vertices = []
n = 11
for i in range(2**n):
    vertices.append('{0:011b}'.format(i))
graph = {}
for start in vertices:
    ends = []
    for end in vertices:
        if end.startswith(start[1:]):
            ends.append(end)
    graph[start] = ends

cycles = []
def graph_not_empty():
    for v in graph:
        if graph[v] != []:
            return True
    return False
v = '0' * n
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
for v in cycle:
    s += v[0]
print s
print len(s)
for i in range(2**(n+1)):
    if '{0:012b}'.format(i) not in s and '{0:012b}'.format(i) not in s[n:] + s[:n]:
        print '{0:b}'.format(i)
