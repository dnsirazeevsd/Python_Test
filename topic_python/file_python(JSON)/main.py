data_info = []
count_error = 0

with open("app.log", "r", encoding="utf-8") as file:
    for item in file:
        if (item.find("INFO") or item.find("ERROR")) == -1:
            data_info.append(item.strip())
            count_error += 1

with open("error.logs", "w", encoding="utf-8") as file:
    for item in data_info:
        file.write(item.strip() + "\n")
    file.write(f"Total ERROR or WARNING -> {count_error}")


#list (users) -> dict(["name" : "age"]) -> list(name + string)

# "r" Только чтение, файл должен существовать
# "w" Запись, стирает содержимое, создаёт файл если его нет
# "a" Добавление в файл: без стирания
# "a+" Чтение и добавление, курсор в конец файла