import yaml
import fa_json_module
import time
def main():

    with open("tt.yml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)
    all_tt_dict = data_loaded
    for key in all_tt_dict:
        if all_tt_dict[key] != {}:

            obj = fa_json_module.JSONProcessingClass("ТЕСТ",all_tt_dict[key])
            all_list = obj.outstring.split("\a")
            for e in all_list:
                print("-"*50)
                print(e)
            print("*"*50)
            time.sleep(1)
        else:
            print("Неть пар у "+key)


if __name__ == "__main__":
    main()