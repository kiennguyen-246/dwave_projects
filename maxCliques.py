import networkx as nx
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
from collections import defaultdict
from itertools import combinations
import math

numRead = 1000

g = nx.gnp_random_graph(40, 0.2)
print("Graph on {} nodes created with {} out of {} possible edges.".format(len(g.nodes), len(g.edges), len(g.nodes) * (len(g.nodes)-1) / 2))

n = len(g.nodes)
m = len(g.edges)
lg = math.log2(n)
deg = [0] * n
for u, v in g.edges:
    deg[u] += 1
    deg[v] += 1
maxDeg = n
for u in g.nodes:
    maxDeg = max(deg[u], deg[v])
print(maxDeg)

b = 1
a = (maxDeg + 2) * b

q = defaultdict(int)

for i in range(n, n + lg):
    q[(i, i)] += -a
    for j in range(i + 1, n + lg):
        q[(i, j)] += 2 * a
for i in range(n, n + lg):
    q[(i, i)] += 2 ** (2 * i) * a
    for j in range(i + 1, n + lg):
        q[(i, j)] += 2 ** (i + j) * a
q[(n + lg, n + lg)] += (n + 1 - 2 ** lg) ** 2 * a 
for (u, v) in combinations(g.nodes, 2):
    q[(u, v)] += a
for i in range(n, n + lg) q[(i, i)] += a