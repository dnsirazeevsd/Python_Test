def sum_values(a: float, b: float) -> float:
    return a + b

def minus_values(a: float, b: float) -> float:
    return a - b

def multiplication_values(a: float, b: float) -> float:
    return a * b

def division_values(a: float, b: float) -> float | str:
    if b == 0:
        return "ERROR -> division by 0!"
    return a / b

def calculator():
    while True:
        print("\nВыберите операцию:")
        print("1 -> '+'")
        print("2 -> '-'")
        print("3 -> '/'")
        print("4 -> '*'")
        print("5 -> 'exit'")

        # Выбор действия с проверкой ввода
        try:
            user_action = int(input("Enter your action -> "))
        except ValueError:
            print("Invalid input! Enter a number from 1 to 5.")
            continue

        if user_action == 5:
            print("Exiting calculator. Goodbye!")
            break

        # Ввод чисел с проверкой
        try:
            value_1 = float(input("Enter your first number -> "))
            value_2 = float(input("Enter your second number -> "))
        except ValueError:
            print("Invalid input! Please enter numbers only.")
            continue

        # Выполнение операций
        if user_action == 1:
            result = sum_values(value_1, value_2)
            print(f"Result -> {value_1} + {value_2} = {result}")
        elif user_action == 2:
            result = minus_values(value_1, value_2)
            print(f"Result -> {value_1} - {value_2} = {result}")
        elif user_action == 3:
            result = division_values(value_1, value_2)
            print(f"Result -> {value_1} / {value_2} = {result}")
        elif user_action == 4:
            result = multiplication_values(value_1, value_2)
            print(f"Result -> {value_1} * {value_2} = {result}")
        else:
            print("NO VALID ACTION\n")

if __name__ == "__main__":
    calculator()
