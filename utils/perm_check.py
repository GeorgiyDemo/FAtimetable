from sympy.utilities.iterables import multiset_permutations
import numpy as np

a = np.array([0, 1, 0, 2])
listm = []
for p in multiset_permutations(a):
    listm.append(p)

print(len(listm))
print(listm)