usr_values = input("Enter your values ->")

list_values = usr_values.split()

print(list_values)

new_list_ch = []
new_list_nch = []


for value in list_values:
    value = int(value)
    if value % 2 == 0:
        new_list_ch.append(value)
    else:
        new_list_nch.append(value)




print(new_list_ch, "cумма: ", sum(new_list_ch))
print(new_list_nch, "cумма: ", sum(new_list_nch))