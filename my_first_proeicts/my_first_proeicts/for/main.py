numbers = []
sum = 0

for i in range(1,21):
    numbers.append(i)

for value in numbers:
    sum += (value ** 2)

print(sum)