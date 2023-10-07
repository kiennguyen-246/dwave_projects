import networkx as nx
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
from collections import defaultdict
from itertools import combinations
import math
import random

numReads = 1000

g = nx.gnp_random_graph(20, 0.2)
print("Graph on {} nodes created with {} out of {} possible edges.".format(len(g.nodes), len(g.edges), len(g.nodes) * (len(g.nodes)-1) / 2))
n = len(g.nodes)
m = len(g.edges)
k = 2

print(g.edges)

b = 1
a = (k + 2) * b
q = defaultdict(int)

for i in g.nodes:
    q[(i, i)] += (1 - 2 * k) * a
for (i, j) in combinations(g.nodes, 2):
    q[(i, j)] += 2 * a
for (u, v) in g.edges:
    q[(u, v)] -= b

chainStrength = a * n
sampler = EmbeddingComposite(DWaveSampler())
response = sampler.sample_qubo(q,
                               chain_strength=chainStrength,
                               num_reads=numReads,
                               label='Cliques Check')

sample = response.record.sample[0]
# print(sample)

h = 0
s = 0
for i in g.nodes:
    s += sample[i]
h += a * ((k - s) ** 2)
s = 0
for (u, v) in g.edges:
    s += sample[u] * sample[v]
h += b * (k * (k - 1) / 2 - s)
if (h <= 0):
    print("A clique of size {} exists:".format(k))
    for u in g.nodes:
        if (sample[u] == 1):
            print(u, end=" ")
    print()
else:
    print("A clique of size {} does not exist.".format(k))
    

