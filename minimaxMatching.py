import networkx as nx
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
from collections import defaultdict
from itertools import combinations
import math
from random import randint
from functools import reduce

numReads = 1000

g = nx.Graph([
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 5),
    (5, 6),
    (2, 4)
])
n = g.nodes
m = g.edges

for 