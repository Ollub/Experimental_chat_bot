from glob import glob

IMAGES = glob('planets_fotos/*.jp*g')

# функция подсчета слов в фразе


def wordcount_func(phrase):
    if len(phrase) == 0:
        return 'no text'
    elif '"' == phrase[0] == phrase[-1]:
        return len(phrase.strip('"').split())
    else:
        return 'Что то не так... Может ковычки забыли ?'


if __name__ == '__main__':
    print(IMAGES)
