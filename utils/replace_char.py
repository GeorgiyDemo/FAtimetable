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
string = "4. Алгоритмы и структуры данных .. 17:20-18:50 Петросов Д.А., 508(кк)"

all_combs_list = []
for i in range(len(string)):
    if string[i] in d:
        if string[i] in chars_dict:
            chars_dict[string[i]] += 1
        else:
            chars_dict[string[i]] = 1

print(chars_dict)
for k in chars_dict:
    buf_string = string
    for i in range(chars_dict[k]):
        buf_string = buf_string.replace(k,d[k],1)
        string_list.append(buf_string)

print(string_list)
