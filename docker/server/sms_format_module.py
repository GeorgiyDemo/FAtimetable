"""
Модуль для замены символов в SMS-сообщениях (чтоб не банила система)
"""

import json
from sympy.utilities.iterables import multiset_permutations
import numpy as np

class SMSFormaterClass(object):
    def __init__(self, sms_string):
        self.sms_string = sms_string
        self.outd = {}

        self.replaced = {
            "е": "e",
            "о": "o", 
            "а": "a",
            "с": "c",
            "А": "A",
            "О": "O",
            "Е" : "E",
            "С" : "C",
        }

        self.spliter()

        print(json.dumps(self.outd,ensure_ascii=False))
    
    def spliter(self):
        """
        Метод для формирования выходного словаря 
        со всеми возможными сочетаниями символов
        """
        outd = {}

        splited_list = self.sms_string
        splited_list = splited_list.split("\a")
        splited_list.pop(-1)

        for i in range(len(splited_list)):

            break_comb = -1
            
            for n in range(2,10):
                d, counter = self.replace_chars(splited_list[i], n)
                if counter == 0:
                    d = d_prev
                    counter = counter_prev
                    break_comb = n-1
                    break

                #TODO Вынести в конфиг
                if counter > 40:
                    break_comb = n
                    break

                counter_prev = counter
                d_prev = d
            
            outd[i] = {"data" : list(d.keys()), "counter": 0, "gen_info":{ "difficulty" : break_comb, "unic_val" : counter}}
        
        self.outd = {"sms_list": outd}
            

    def replace_chars(self, input_str, n):
        """
        Метод для замены символов в тексте
        """
        string = input_str
        string_dict = {}
        all_symbols = np.array([])

        for i in range(len(string)):
            if string[i] in self.replaced:
                all_symbols = np.append(all_symbols, i)

        for p in multiset_permutations(all_symbols.astype(int), n):
            buf_string = list(string)
            for element in p:
                buf_string[element] = self.replaced[buf_string[element]]
                string_dict["".join(buf_string)] = None
        
        return string_dict, len(string_dict)

if __name__ == "__main__":
    s = "Расписание группы ИБ19-2 09.10.2019\a1. Физические явления и процессы в об.. 11:50-13:20\nНизамов А.Ж., 303\a2. Физические явления и процессы в обл.. 14:00-15:30\nЕгоров Е.В., 708\a3. Иностранный язык (Иностранный язык) 15:40-17:10\n 511, 606\a"
    SMSFormaterClass(s)