from sympy.utilities.iterables import multiset_permutations
import numpy as np

a = np.array([3, 6, 15, 26, 48, 51, 52, 53, 58])
string_list = []
i = 0
for p in multiset_permutations(a):
    #string_list.append(p)
    #print(p)