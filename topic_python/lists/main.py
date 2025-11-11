fruits = ["apple", "test", "banana", "sada", "test", "Danil", "test"]

nums = [1,2,3,4,5,6,7,8,9]

#Сортировка + .lower()
def sort_by_max(items : list) -> list: #от большего к меньшему
    for index in range(len(items)):
        items[index] = items[index].lower()
    
    items.sort()
    return items

#Сортировка + .lower()
def sort_by_min(items : list) -> list: #от меньшего к большему
    for index in range(len(items)):
        items[index] =  items[index].lower()
    
    items.sort(reverse=True)

    return items

#Удаление повторяющего слова в списке
def delete_repeate_words(item : list, del_str : str) -> list:
    count = item.count(del_str)

    for _ in range(count):
        item.remove(del_str)
    
    return item

#Возвращает срез списка от i до j
def get_new_section(item : list, i : int, j : int) -> list:
    return item[i:j]

print(get_new_section(fruits, 1, 4))


#Суммирует все числа в списке кроме первого и последнего
def sum_nums(item : list) -> int:
    total = 0
    num_begin = item[0]
    num_end = item[len(item) - 1]

    for num in range(len(item)):
        total += item[num]

    return total - num_begin - num_end

    #return sum(item[1:-1]) упрощенный вариант с использованием среза




print(sum_nums(nums))

#append()
#insert()
#remove()
#pop()
#sort()
#reverse()
#copy()
#count()

