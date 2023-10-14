import networkx as nx
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
from collections import defaultdict
from itertools import combinations
import math
from random import randint
from functools import reduce

numReads = 1000

m = 10
n = 12

c = [[((-1) ** randint(1, 2)) * randint(1, m) for j in range(0, 3)] for i in range(0, n)]
print("c = {}".format(c))
# c = [[1, -2, 3], [1, -3, 4], [-3, -4, -2], [-1, -3, -2], [2, -1, -4]]

A = 3 * n + 2
B = 1

q = defaultdict(int)
for i in range(0, 3 * n):
    for j in range(i + 1, 3 * n):
        if (i // 3 == j // 3):
            q[(i, j)] += A
            # print("({}, {})".format(i, j))
        if (c[i // 3][i % 3] == -1 * c[j // 3][j % 3]):
            q[(i, j)] += A
            # print("({}, {})".format(i, j))
for i in range(0, 3 * n):
    q[(i, i)] -= B

chainStrength = 6 * A
sampler = EmbeddingComposite(DWaveSampler())
response = sampler.sample_qubo(q,
                               chain_strength=chainStrength,
                               num_reads=numReads,
                               label='3-sat Solution')

sample = response.record.sample[0]
if (reduce(lambda a, b: a + b, sample) >= m):
    print("Satisfied. Chosen/left out items are: ")
    ans = [0] * (m + 1)
    for i in range(0, 3 * n):
        if (sample[i] != 0):
            ans[abs(c[i // 3][i % 3])] = c[i // 3][i % 3]
    for i in range(1, m + 1):
        if (ans[i] == 0): 
            print(i, end = " ")
        else:
            print(ans[i], end = " ")
    print()
else:
    print("Not satisfied.")