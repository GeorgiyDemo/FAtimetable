import yaml
import fa_json_module

def main():

    with open("tt.yml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)
    all_tt_dict = data_loaded
    for key in all_tt_dict:
        #print(all_tt_dict[key])
        obj = fa_json_module.JSONProcessingClass("ТЕСТ",all_tt_dict[key])
        print(obj.outstring)

if __name__ == "__main__":
    main()