
result_list = []

with open("logs.txt", "r", encoding="utf-8") as file:
    for line in file:
        if line.find("ERROR") != -1:
            result_list.append(line.upper().strip())

index = 1

for item in result_list:
    print(f"{index} -> {item}")
    index += 1

# "r" Только чтение, файл должен существовать
# "w" Запись, стирает содержимое, создаёт файл если его нет
# "a" Добавление в файл: без стирания
# "a+" Чтение и добавление, курсор в конец файла