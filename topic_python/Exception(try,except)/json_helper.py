class UserNotFound(Exception):
    pass

def get_user(list_users, id_user):
    for user in list_users:
        if user["id"] == id_user:
            return user
        
    raise UserNotFound(f"User id[{id_user}] not found")