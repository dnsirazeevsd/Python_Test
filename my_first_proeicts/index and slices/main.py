fruits = ["apple", "banana", "cherry"]

fruits[0], fruits[2] = fruits[2], fruits[0]

print(fruits)


number = [0,1,2,3,4,5,6,7,8,9,10]
print(number[0:len(number):2])

#3 способа развернуть список наооборот

numbers = [1,2,3,4,5,6,7,8,9]

#1
#new_numbers = numbers[::-1]

#2
#numbers.reverse()

#3
#new_numbers = list(reversed(numbers))

print()