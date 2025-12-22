import json

#Загрузка информации из JSON
def load_info_json(file_name) -> list:
    with open(file_name, "r", encoding="utf-8") as file:
        return(json.load(file))

#Запись информации в JSON
def record_info_json(data, file_name):
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

#From LIST to DICT
def from_list_to_dict(info : list) -> dict:
    return {user["name"] : user["age"] for user in info}

#From DICT to LIST
def from_dict_to_list(info : dict) -> list:
    return [f"{key}: {value}" for key, value in info.items()]

#Вывод информации из LIST
def print_info_list(info):
    for item in info:
        print(item)

#Вывод информации из DICT
def print_info_dict(info):
    print(info)



