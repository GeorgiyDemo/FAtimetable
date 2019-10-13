from sympy.utilities.iterables import multiset_permutations
import numpy as np

d = {
    "е": "e",
    "о": "o", 
    "а": "a",
    "с": "c",
    "А": "A",
    "О": "O",
    "Е" : "E",
    "С" : "C",
}

string_dict = {}
all_symbols = np.array([])
string = "4. Алгоритмы и структуры данных .. 17:20-18:50 Петросов Д.А., 508(кк)"

all_combs_list = []
for i in range(len(string)):
    if string[i] in d:
        all_symbols = np.append(all_symbols,i)

for p in multiset_permutations(all_symbols.astype(int)):
    buf_string = list(string)
    for element in p:
        buf_string[element] = d[buf_string[element]]
        string_dict["".join(buf_string)] = None

print(string_dict)
#for key in string_dict:
#   print(key)