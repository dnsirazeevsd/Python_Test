list_ref = []
index_total_ref = 0
index = 1

# Чтение и фильтрация строк
with open("logs.txt", "r", encoding="utf-8") as file:
    for item in file:
        if ".m3u8" in item:
            list_ref.append(item.lower().strip())  # убираем лишние пробелы
            index_total_ref += 1

with open("result.txt", "w", encoding="utf=8") as file:
    for item in list_ref:
        file.write(f"{index} -> {item}\n")
        index += 1

print(f"Total -> {index_total_ref}")

