import random

pc_value = random.randint(1, 10)

while True:
    my_answer = int(input("Enter value -> "))
    if (my_answer == pc_value):
        break
    else:
        if my_answer > pc_value:
            print("PC_VALUE < ")
        else:
            print("PC_VALUE > ")

print(my_answer)


