from json_helper import UserNotFound, get_user

data = [
    {"id" : 1, "name" : "Danil"}, 
    {"id" : 2, "name" : "Emil"}
]

try:
    print(get_user(data, 3))
except UserNotFound as e:
    print(e)