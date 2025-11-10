def add(x: int, y: int) -> int:
    return x + y

print(add(10,10))

def add_all(*args):
    sum = 0
    for val in args:
        sum += val
    return sum

print(add_all(1,2,3,4,5))

values_1 = [1,2,3,4,5,6]
values_2 = [10,11,12,13,14,15]

print(add_all(*values_1, *values_2))