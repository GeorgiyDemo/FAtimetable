from itertools import permutations
# Использовать numpy
### https://stackoverflow.com/questions/41210142/get-all-permutations-of-a-numpy-array

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

string_list = []
chars_dict = {}
all_symbols = []
string = "4. Алгоритмы и структуры данных .. 17:20-18:50 Петросов Д.А., 508(кк)"

all_combs_list = []
for i in range(len(string)):
    if string[i] in d:
        all_symbols.append([string[i],i])

print(all_symbols)
for e in permutations(all_symbols, len(all_symbols)):
    buf_string = list(string)
    for element in e:
        buf_string[element[1]] = d[element[0]]
        string_list.append("".join(buf_string))

string_list = list(set(string_list))
print(len(string_list))
#print(string_list)

