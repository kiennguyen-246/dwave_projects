import networkx as nx
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
from collections import defaultdict
from itertools import combinations
import math
import random
from functools import reduce

numReads = 1000

m = 30
n = 10
s = [[random.randint(0, 200) for j in range (0, n)] for i in range(0, m)]
x = [random.randint(0, 1) for i in range(0, n)]
b = [0 for i in range(0, m)]
for i in range(0, m):
    sum = 0
    for j in range(0, n):
        sum += s[i][j] * x[j]
    b[i] = sum
c = [random.randint(0, 200) for i in range (0, n)]

print("S = {}".format(s))
print("b = {}".format(b))
print("c = {}".format(c))
print("Sample x = {}".format(x))

q = defaultdict(int)
A = (n + 2) * max(c)
B = 1

for i in range(0, m):
    for j in range(0, n):
        q[(j, j)] += (-2 * b[i] * s[i][j] + s[i][j] ** 2) * A
    for j1 in range(0, n):
        for j2 in range(j1 + 1, n):
            q[(j1, j2)] += 2 * s[i][j1] * s[i][j2] * A

sum = 0
for i in range(0, n):
    for j in range(0, n):
        sum += q[(i, j)] * x[i] * x[j]
print(sum)

for i in range(0, n):
    q[(i, i)] -= c[i] * B

sumS = 0
for i in range(0, m):
    for j in range(0, n):
        sumS += s[i][j]
sumC = reduce(lambda a, b: a + b, c)
chainStrength = max(A * (sumS ** 2), B * sumC) + 1000

sampler = EmbeddingComposite(DWaveSampler())
response = sampler.sample_qubo(q,
                               chain_strength=chainStrength,
                               num_reads=numReads,
                               label='ILP Solution')

sample = response.record.sample[0]
print(sample)

noSolution = 0
for i in range(0, m):
    sum = 0
    for j in range(0, n):
        sum += s[i][j] * sample[j]
    if (sum != b[i]):
        print("No valid solution found.")
        noSolution = 1
        break
if (noSolution == 0):
    sum = 0
    for i in range(0, n):
        sum += c[i] * sample[i]
    print("Solution found with optimal value of {}: ".format(sum))
    print("x = {}".format(sample))
     