import os
import logging

import ephem
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove



import bot_body
from game_cityes import csv_reader
from planet_ephem import current_planet_position
from simple_calc import calc_main


# конфигурируем логирование
# можно задать три уровня WARNING INFO DEBUG
# вывод логов - в терминал

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


#определеяем константы - состояния бота
START, PLANET, LENFRASE, CALC, CITYES = range(5)

# Настройки прокси помещаем в константу

PROXY = {'proxy_url': os.getenv('PROXY_URL', 'socks5://t1.learn.python.ru:1080'),
         'urllib3_proxy_kwargs': {'username': os.getenv('PROXY_USERNAME', 'learn'),
                                  'password': os.getenv('PROXY_PASSWORD', 'python')}}
API = os.getenv('API_KEY')

# передаем в переменную список планет, которые далее будут кнопками и списком для сранвения
planets = [i[2] for i in ephem._libastro.builtin_planets()[:8]]
# для городов записываем список городов
cityes_list = csv_reader()
last_city = ''


# стартовая функция
# возвращает в чат список кнопок с функциями
# а также переключает беседу в режим START
def greet_user(bot, update):
    user = update.message.from_user
    buttons = [['wordcount', 'planet'], ['game', 'calculator']]
    logging.info('user id{0}, {1} запустил нажал'.format(user.id, user.first_name))
    update.message.reply_text('Hi, {}! I am Oleg\'s Bot. Let\'s push the button!!!'.format(user.first_name),
        reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard = True))
    return START

# функция переключает беседу в выбранный режим
def conv_rullet(bot, update):
    user_text = update.message.text
    logging.info('Нажата кнопка %s', user_text)
    if user_text == 'planet':
        update.message.reply_text('Вызвана функция определения местоположения планеты в созвездии на текущую дату. \n'
                                'Для старта выберите планету. \n' 
                                'Для выхода напишите /cancel. \n'
                                'Для перехода в начало напишите /start', 
                                reply_markup=ReplyKeyboardMarkup(
                                    [
                                     planets[0:len(planets)//2],
                                     planets[len(planets)//2:]
                                    ] ))
        #[planets[0:len(planets)//2]]
        logging.info('Переключен в состояние PLANET')
        return PLANET
    elif user_text == 'wordcount':
        update.message.reply_text('Вызвана функция подсчета количества слов в введенном тексте. '
                                'Текст пишите обязательно в ковычках ""! '
                                'Для выхода напишите /cancel. \n'
                                'Для перехода в начало напишите /start')
        logging.info('Переключен в состояние LENFRASE')
        return LENFRASE

    elif user_text == 'game':
        update.message.reply_text('Давай поиграем в города! Ты начинай ;)'
                                'Для выхода напишите /cancel. \n'
                                'Для перехода в начало напишите /start')
        logging.info('Переключен в состояние CITYES')
        return CITYES 

    elif user_text == 'calculator':
        update.message.reply_text('Вы в калькуляторе. Введите выражение.\n'
                                'Не забудьте в конце добавить "="\n'
                                'Для выхода напишите /cancel. \n'
                                'Для перехода в начало напишите /start',
                                reply_markup=ReplyKeyboardMarkup(
                                    [
                                     ['1', '2', '3', '+'],
                                     ['4', '5', '6', '-'],
                                     ['7', '8', '9',' dev'],
                                     ['.', '0', '=', '*']
                                    ] ))
        logging.info('Переключен в состояние CALC')
        return CALC 

# Записываем функции работы с планетами

    
def planet_body(bot, update):
    current_planet = update.message.text
    for foto in bot_body.IMAGES:
        if current_planet in foto:
            picture = foto
            break
    if current_planet in planets:
        print('in planets')
        text = current_planet_position(current_planet)
        logging.info('запрошена информация о планете {}'.format(current_planet))
        bot.send_photo(chat_id = update.message.chat_id, photo = open(foto, 'rb'))
    else:
        logging.info('неизвестная команда: {}'.format(current_planet))
        text = 'Try another planet'

    update.message.reply_text(text)

    
def wordcount_body(bot, update):
    user = update.message.from_user
    text = update.message.text
    logging.info('%s что то написал...', user.first_name)
    update.message.reply_text(bot_body.wordcount_func(text))


# функция выхода

def cancel(bot, update):
    user = update.message.from_user
    logging.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def game_city(bot, update, user_data):
    city = update.message.text
    if 'last_city' not in user_data:
        user_data['last_city'] = city[::-1]
    if city not in cityes_list:
        answer = 'Город уже был, либо не существует'
    elif city[0] != user_data['last_city'][-1]:
        answer = 'Нарушаете правила. Назовите город на букву {}'.format(user_data['last_city'][-1])
    else:
        cityes_list.remove(city)
        n = 0
        letter = city[-1]
        if city[-1] in 'ъь':
            letter = city[-2]
            update.message.reply_text('так не честно, выбираю букву "{}"'.format(letter))
        
        while n < len(cityes_list):
            if cityes_list[n][0] == letter:
                 print(cityes_list[n])
                 last_city = cityes_list[n]
                 cityes_list.remove(last_city)
                 answer = last_city
                 user_data['last_city'] = last_city
                 break
            n += 1
        #if n == len(cityes_list):
         #   answer = 'You win!'
    #else:
     #   answer = 'не правильный ввод'
    update.message.reply_text(answer)

def calculator(bot, update, user_data):
    logging.info("Переход в тело калькулятора")
    symbol = update.message.text
    final_expression = ''

    if 'expression' not in user_data:
        user_data['expression'] = symbol
        logging.info("В выражение добавлен %s", symbol)
    else:
        user_data['expression'] += symbol
        logging.info("В выражение добавлен %s", symbol)
    if symbol == '=':
        
        final_expression = user_data['expression'].strip('=').replace('dev', '/')
        user_data['expression'] = ''
        logging.info("Переходим к подсчету выражения %s", final_expression)

        number = calc_main(final_expression)

        update.message.reply_text(number)



        




# первый шаг. Создаем функцию, являющуюся ТЕЛОМ БОТА
# Updater несколько раз в сек соед-ся с Botfather, передает ключ и принимает сообщения.
# в свою очередь на данные сообщения можно отреагировать

def main():
    # загружаем бот в переменную
    mybot = Updater(API, request_kwargs=PROXY)
    dp = mybot.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', greet_user),
                    MessageHandler(Filters.text, conv_rullet)],

        states={
            START: [MessageHandler(Filters.text, conv_rullet),
                   CommandHandler('start', greet_user)],

            PLANET: [MessageHandler(Filters.text, planet_body),
                    CommandHandler('start', greet_user)],

            LENFRASE: [MessageHandler(Filters.text, wordcount_body),
                    CommandHandler('start', greet_user)],

            CITYES: [MessageHandler(Filters.text, game_city, pass_user_data = True),
                    CommandHandler('start', greet_user)],        

            CALC: [MessageHandler(Filters.text, calculator, pass_user_data = True),
                    CommandHandler('start', greet_user)], 
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(conv_handler)
    '''
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler('wordcount', wordcounter))

    # добавляем команду \planet
    # dp.add_handler(CommandHandler("planet", planet_galaxy))
    dp.add_handler(MessageHandler(Filters.text, planet_constellation))
    # начинается клиент-серверный обмен сообщениями
    '''

    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':

    main()
    

