from glob import glob

IMAGES = glob('planets_fotos/*.jp*g')



#функция подсчета слов в фразе
def wordcount_func(frase):
    if len(frase) ==0:
        return 'no text'
    elif '"' == frase[0] == frase[-1]:
        return len(frase.strip('"').split())
    else:
        return 'Что то не так... Может ковычки забыли ?'

# не используется
'''
def easy_calc(expression):
    if len(expression) == 0:
        return 'Пустое выражение'
    elif expression[-1] != '=':
        return 'забыли "=" на конце :('
    try:
        return eval(expression.strip('='))
    except NameError:
        return 'Упс, ошибочка вышла. Вводить нужно только числа'
    except ZeroDivisionError:
        return 'Разве в школе не учили, что на ноль делить нельзя?!'
'''

# не используется
'''
def word_calc(expression):
    operators = {'plus': '+', 'minus': '-', 'devide': '/', 'multiple': '*'}
    # тут тоже нужны проверки, но для экономии времени на них забъю... и так все понятно
    expression = expression.strip('!.,# ').split()
    new_expression = ''
    for i in expression:
        if i in operators:
            new_expression += operators[i]
        else: new_expression += i
        new_expression += ' '
    try:
        return eval(new_expression)
    except NameError:
        return 'Упс, ошибочка вышла. Вводить нужно только числа'
    except ZeroDivisionError:
        return 'Разве в школе не учили, что на ноль делить нельзя?!'

'''




if __name__ == '__main__':
    #print(wordcount_func(input('пиши что нибудь: ')))
    print(IMAGES)