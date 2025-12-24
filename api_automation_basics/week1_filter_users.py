data_users = [
    {"id": 1, "name": "Алиса Иванова", "email": "alice@example.com", "is_active": True},
    {"id": 2, "name": "Борис Петров", "email": "boris.p@example.com", "is_active": True},
    {"id": 3, "name": "Вера Сидорова", "email": "vera_s@test.ru", "is_active": False},
    {"id": 4, "name": "Глеб Кузнецов", "email": "gleb.kuz@domain.com", "is_active": True},
    {"id": 5, "name": "Дарья Морозова", "email": "darya.m@test.ru", "is_active": False},
    {"id": 6, "name": "Евгений Волков", "email": "evg.volkov@example.com", "is_active": True},
    {"id": 7, "name": "Зоя Николаева", "email": "zoya.n@domain.com", "is_active": True},
    {"id": 8, "name": "Илья Орлов", "email": "ilya.orlov@test.ru", "is_active": False},
    {"id": 9, "name": "Ксения Федорова", "email": "ksenia.f@example.com", "is_active": True},
    {"id": 10, "name": "Михаил Лебедев", "email": "m.lebedev@domain.com", "is_active": False}
]

#Функция выводит список по строчкам
def print_data_list(data: list):
    for node in data:
        print(node)

#Функция делает поиск user по id
def find_user_by_id(users: list, id: int):
    
    for user in users:
        if user["id"] == id:
           return user
    
    return None
        
   

#Функция возращается словарь статистики users
def get_user_stats(users: list) -> dict:
    total = 0
    active = 0
    inactive = 0
    status = {}

    for user in users:
        if user["is_active"]:
            active += 1
        else:
            inactive += 1
    
    status["total"] = active + inactive
    status["active"] = active
    status["inactive"] = inactive

    return status

#Функция возвращает список пользователей у которых email заканчивается на @domain
def get_users_by_email_domain(users: list, domain : str) -> list:
    list_users = []

    for user in users:
        if user["email"].endswith(domain):
            list_users.append(user)

    return list_users


#Функция возвращает активных пользователей
def filter_active_user(users: list) -> list:
    active_users = []

    for user in users:
        if user["is_active"]:
            active_users.append(user)
    return active_users

#Функция возвращает список имен активных пользователей
def get_active_user_names(users: list) -> list:
    name_users = []

    for user in users:
        if user["is_active"]:
            name_users.append(user["name"])

    return name_users

print(find_user_by_id(data_users, 4))
