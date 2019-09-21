"""
Утилита для добавления значений в Redis с yaml через requests
"""
import yaml
import requests
import time

YAML_FILE = "groups.yml"
class YamlClass(object):
    def __init__(self, d):
        self.d = d
        self.y_get()
        #self.y_set()
    
    def y_get(self):
        #Чтение из файла
        with open(YAML_FILE, 'r') as stream:
            data_loaded = yaml.safe_load(stream)
        self.result = data_loaded
    
    def y_set(self):
        #Запись в файл
        with open(YAML_FILE, 'w') as outfile:
            yaml.safe_dump(self.d, outfile, default_flow_style=False, allow_unicode=True)

def main():
    obj = YamlClass("")
    d = obj.result

    for e in d:
        r = requests.post("http://127.0.0.1:5000/add_group",data={"group":e,"id":d[e]}).json()
        if r["status"] == "ok":
            print("Успешно добавили "+e+" ["+d[e]+"]")

if __name__ == "__main__":
    main()