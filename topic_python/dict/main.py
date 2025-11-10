person_1 = {}

person_1["name"] = "Danil"
person_1["age"] = 25
person_1["city"] = "SPB"
person_1["surname"] = "Sirazeev"
person_1["job"] = "Forsite"

person_2 = {
    "name" : "Emil",
    "age" : 34,
    "city" : "Aby",
    "surname" : "Sirazeev",
    "job" : "programmer"
}

for item in person_1.keys():
    print(person_1[item])

print()

for item in person_2.values():
    print(item)