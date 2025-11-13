count_total = 0
count_error = 0

result_list = []

with open("logs.txt", "r", encoding="utf=8") as file:
    for line in file:
        count_total += 1
        if line.find("ERROR") != -1:
            result_list.append(line.upper().strip())
            count_error += 1

with open("report.txt", "w", encoding="utf-8") as file:
    file.write(f"Всего строк: {count_total} \nСтрок с ошибками:{count_error}")