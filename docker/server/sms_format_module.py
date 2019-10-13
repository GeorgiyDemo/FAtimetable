"""
Модуль для замены символов в SMS-сообщениях (чтоб не банила система)
"""

from sympy.utilities.iterables import multiset_permutations
import numpy as np

class SMSFormaterClass(object):
    def __init__(self, sms_string):
        self.sms_string = sms_string
        self.outd = {"data":{}}

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
    
    def spliter(self):
        """
        Метод для формирования выходного словаря 
        со всеми возможными сочетаниями символов
        """
        
        splited_list = self.sms_string
        splited_list = splited_list.split("\a")
        splited_list.pop(-1)

        for string in splited_list:
            d = self.replace_chars(string)
            print(f)


    def replace_chars(self, input_str):
        """
        Метод для замены символов в тексте
        """
        string = input_str
        string_dict = {}
        all_symbols = np.array([])

        for i in range(len(string)):
            if string[i] in self.replaced:
                all_symbols = np.append(all_symbols, i)

        for p in multiset_permutations(all_symbols.astype(int)):
            buf_string = list(string)
            for element in p:
                buf_string[element] = self.replaced[buf_string[element]]
                string_dict["".join(buf_string)] = None

        return string_dict