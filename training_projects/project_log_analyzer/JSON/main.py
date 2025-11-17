from json_utils import load_data, save_file, print_info, changing_data

data = load_data("users.json")

data = changing_data(data)

print_info(data)

save_file("users.json", data)