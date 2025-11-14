import json

count_tasks = 0
count_true_tasks = 0
count_false_tasks = 0

with open("users.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Вывод текущих задач и подсчёт
for item in data["tasks"]:
    count_tasks += 1
    if item["done"]:
        count_true_tasks += 1
    else:
        count_false_tasks += 1
    print(f"{item}")

print(f"\nTotal tasks -> {count_tasks}")
print(f"Total false tasks -> {count_false_tasks}")
print(f"Total true tasks -> {count_true_tasks}\n")

# Обновление задачи по ID
user_index_task = int(input("Enter id task -> "))
task_found = False

for item in data["tasks"]:
    if item["id"] == user_index_task:
        item["done"] = True
        task_found = True
        break

if task_found:
    print(f"Task id {user_index_task} -> True")
else:
    print(f"Task id {user_index_task} not found!")

# Сохраняем обновлённый JSON
with open("users.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2, ensure_ascii=False)
