import csv


# вводим функцию, считывающую csv- файл и возвращающую список

def csv_reader(filepath):
    cities_names = []
    with open(filepath, encoding='windows-1251') as csvfile:
        filereader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for row in filereader:
            cities_names.append(row[-1])
    return cities_names


if __name__ == '__main__':
    print(csv_reader('city.csv'))
