#Мини-задание 1: Создай список строк с названиями файлов, найди все, где есть .log, и выведи их в верхнем регистре.

list_name_file = ["file.log", "test.txt", "danil.ps1", "copy.fxf", "error.log"]

list_result = []


print(f"List -> {list_name_file}")

for item in list_name_file:
    if item.find(".log") != -1:
        list_result.append(item.upper())

print(list_result)





