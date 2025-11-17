import json


#Загрузка из файла 
def load_data(path):
    with open(path, "r",encoding="utf-8") as file:
        return json.load(file)
    
#Загрузка в файл
def save_file(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

#Изменение данных 
def changing_data(data : dict):
    user_index = int(input("Enter id user -> "))

    if user_index > 10:
        print("ERROR -> id not found :( ")
        return
    else:
        user_age = int(input("Enter age -> "))
        
        for item in data:
            if item["id"] == user_index:
                item["age"] = user_age
 
    return data

#Вывод записей из словарей
def print_info(data):
    index = 1
    for item in data:
        print(f"{index} [INFO] -> {item}")
        index += 1