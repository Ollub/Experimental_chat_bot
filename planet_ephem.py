import ephem
import datetime

# определим функцию, которая на вход принимает название планеты
# на выходе - местоположение в созвездии на текущую дату


def current_planet_position(planet_name):
    today_date = datetime.date.today().strftime('%Y/%m/%d')
    current_planet = getattr(ephem, planet_name)(today_date)
    return ephem.constellation(current_planet)


if __name__ == '__main__':
    print(current_planet_position('Mars'))
