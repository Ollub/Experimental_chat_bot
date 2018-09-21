import pandas as pd

#вводим функцию, считывающую csv- файл и возвращающую список
def csv_reader():
    df = pd.read_csv('city.csv', header = 0, sep=',', encoding = 'windows-1251', delimiter = ';')
    return  [i.lower() for i in df['name']]

user_inputs = []
last_city = ' '

#print(csv_reader())

'''   
while True:
    city = input('Ваш ход: ').lower()
    if user_inputs == []:
        last_city = city[::-1]
        
    if city == 'выход':
        break
    elif city in user_inputs:
        print('город уже был')
        continue
    elif city not in list_name:
        print('папу не обманешь! нет такого города')
        continue
    elif city[0] == last_city[-1]:
        user_inputs.append(city)
        n = 0
        letter = city[-1]
        if city[-1] in 'ъь':
            letter = city[-2]
            print('так не честно, выбираю букву {}'.format(letter))
        
        while n < len(list_name):
            if list_name[n][0] == letter:
                 print(list_name[n])
                 last_city = list_name[n]
                 list_name.remove(list_name[n])
                 break
            n += 1
        if n == len(list_name):
            print('Похоже вы избранный!!! С Победой!')
            break


    else:
        print('не правильный ввод')
        continue
'''