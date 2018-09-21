# КАЛЬКУЛЯТОР 
# приоритезация скобками не реализована
# матрешка из 4х функций
# сначала включается функция форматирования строки в список
# затем отдельные операции в порядке приоритета обрабатываются в соответвующей функции и вносятся корректировки в список
# функция нижнего уровня производит вычисления

operation_priority = [['*', '/'], ['+', '-']]

def calc_operation(a,operand, b):
    a, b = float(a), float(b)

    try:
        if operand == '+':
            c =  a + b
        elif operand == '-':
            c = a - b
        elif operand == '/':
            c =  a / b
        elif operand == '*':
            c = a * b
    except NameError:
        return 'Упс, ошибочка вышла. Вводить нужно только числа'
    except ZeroDivisionError:
        return 'Разве в школе не учили, что на ноль делить нельзя?!'
    if c % 1 == 0:
        c = int(c)
    return c

def element_calc(list, index):
    calc_element = calc_operation(list.pop(index-1), list[index-1], list.pop(index))
    list[index - 1] = calc_element
    return list
 
# функция перевода строки с выражением в список
def string_to_mathlist(my_string):
    operation_list = []
    temp_value = ''
    for i in my_string:
        try:
            if i.isdigit():
                temp_value += i
            elif i == ' ':
                continue
            else:
                operation_list.append(temp_value)
                operation_list.append(i)
                temp_value = ''
        except (ValueError, NameError):
            print('Проверьте вводимое значение')
    operation_list.append(temp_value)
    return operation_list


def calc_main(expression, operators = operation_priority):
    expression = string_to_mathlist(expression)
    for priority in operators:
        i = 0
        while i < len(expression):
            if expression[i] in priority:
                expression = element_calc(expression, i)
                i = 0
            i += 1
    return expression[0]


if __name__ == "__main__":
    math = input('Enter math expression: ')
    print(calc_main(math, operation_priority))

