f = open('make_seq.out.self')
data = f.read().split('\n')[:-1] #read in file, split on new lines and remove the new line character at the end
l = 25 #length of each read (assumed to be all equal length)
k = 18 #vertices of length k-1
#TODO: could write code to optimatize the value of k depending on l.

reads = set(data[1:]) #making it a set just to eliminate repeats
answer = data[0] #first line of file is the original sequence for comparison

#split reads up into vertices of length k-1
vertices = set()
for read in reads:
    for i in range(1 - (k-1) + l):
        vertices.add(read[i: (k-1) + i])
#one of the reads isn't 25 in length (probably because it goes over the end of the seqence and doesn't loop

print len(vertices)
graph = {}
#construct graph
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

v = data[1][:k-1] #starting point
#find an initial (probably incomplete) cycle
cycle = []
def find_cycle(v):
    c = []
    while(graph[v] != []):
        c.append(v)
        old_v = v
        v = graph[v][-1]
        del graph[old_v][-1]
    return c

cycle = find_cycle(v) #first cycle using starting point v
def graph_not_empty():
    for v in graph:
        if graph[v] != []:
            return True
    return False

#loop over initial cycle and find other partial cycles at free vertices
while graph_not_empty():
    for i, v in enumerate(cycle):
        if graph[v] != []:
            partial_cycle = find_cycle(v)
            cycle[i:i] = partial_cycle
            break

def cyclically_equal(s1, s2):
    for i in range(len(s1)):
        tmp = s1[i:] + s1[:i]
        if tmp == s2:
            return (True, i)
    s1 = s1[::-1]
    for i in range(len(s1)):
        tmp = s1[i:] + s1[:i]
        if tmp == s2:
            print i
            return (True, i)
    return False

#construct sequence by taking first nucleotide of each vertice in the euler cycle
assembled = ''
for v in cycle:
    assembled += v[0]
worked, i = cyclically_equal(assembled,answer)
if worked:
    print 'successful assembly'
else:
    print 'something went differently and it didn\'t work. try adjusting the value of k or generate different random reads'
print assembled[i:] + assembled[:i] #shift assembled seqence cyclically to put it in the same form as the original
print answer
