value = [1,2,3,4,5]

def multiply_all(*args) -> int:
    result = 1
    for x in args:
        result *= x
    return result

print(multiply_all(*value))  # 24
