import random
import sqlite3
import telebot
import config
from db_create_new_check import is_new
from filters_func import project_name
from filters_func import poject_cat
from filters_func import summ_under
from filters_func import summ_up
from telebot import types


bot = telebot.TeleBot(config.TOKEN)

conn = sqlite3.connect('data_invest.db', check_same_thread=False)
cursor = conn.cursor()

id_mass = []

def db_table_val(id: int, user_id: int, name_pr: str, main_info: str, money: int, category: str, user_name:str):
    """В аргументах функции создаем переменную, чтобы в последствии добавить ее в соответствующий столбец в таблице project нашей бд

        :param id: id проекта, которые будет генерироваться случайныи образом и является уникальным значением для каждой строки в бд
        :type id: int, optional
        :param user_id: id пользователя в telegram, уникально для каждого пользователя
        :type user_id: int, optional
        :param name_pr: название проекта, уникальное значние
        :type name_pr: str, optional
        :param main_info: основная информация о проекте
        :type main_info: str, optional
        :param money: ожидаемое количество привлеченных инвестиций в проект
        :type money: int, optional
        :param category: категория проекта, потказывает его направленность и сферу
        :type category: str, optional
        :param user_name: индефикатор пользователя в telegram
        :type user_name: str, optional"""

    cursor.execute('INSERT INTO project (id, user_id, name_pr, main_info, money, category, user_name) VALUES (?, ?, ?, ?, ?, ?, ?)', (id, user_id, name_pr, main_info, money, category, user_name))
    conn.commit()


@bot.message_handler(commands=["start"])
def start_message(message):
    """Функция которая после стартового сообщения "/start" создает 4 кнопки для дальнешего взаимодекйствия пользователя с ботом"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    info = types.KeyboardButton("/create_a_request")
    search_startups = types.KeyboardButton('Показать все проекты')
    show_my_reqest = types.KeyboardButton('Показать мои анкеты')
    search_by_fitlers = types.KeyboardButton('Фильтры')


    markup.add(info, search_startups, show_my_reqest, search_by_fitlers)

    bot.send_message(message.chat.id, "<b>Добро пожаловать в telegram бота где вы сможете найти интересные стартапы или привлечь инвестиции в свой проект:</b>"
                                      "\n"
                                      "\n" "<i>•Привлекайте инвестиции</i>"
                                      "\n"
                                      "\n" "<i>•Покупайте готовый бизнес</i>"
                                      "\n"
                                      "\n" "<i>•Найдите партнеров по всей стране</i>", reply_markup=markup, parse_mode='html')


@bot.message_handler(commands=["create_a_request"])
def get_pr_name(message): #начало заимствования структуры из проекта pyTelegramBotAPI
    """Запрашиваем название проекта пользователя
        Проверяем сколько строк находится в базе данных, чтобы в последствии проверить получилось ли внести новые данные в бд
        Вызываем следующую функцию с помощью "register_next_step_handler" """
    global database_len

    cursor.execute('SELECT * FROM project')

    database_len = len(cursor.fetchall())

    """Запрашиваем название проекта пользователя
        Вызываем следующую функцию с помощью "register_next_step_handler" """
    msg = bot.send_message(message.chat.id, "Пожалуйста, введите название вашего проекта")
    bot.register_next_step_handler(msg, user_ans_pr_name)

def user_ans_pr_name(message):
    """Присваиваем переменной данные о названии проекта
        Отправляем пользователю запрос на получение основной информации о проекте
        Вызываем следующую функцию с помощью "register_next_step_handler" """
    global nm_pr,  usr_id
    nm_pr = message.text
    usr_id = message.from_user.id
    msg = bot.send_message(message.chat.id, "Пожалуйста, напишите основную информацию о вашем проекте")
    bot.register_next_step_handler(msg, user_ans_main_info)


def user_ans_main_info(message):
    """Присваеваем переменной данные содержащие основную информацию о проекте
        Отправляем пользователю запрос на получение информации о сфере проекта
        Вызываем следующую функцию с помощью "register_next_step_handler" """
    global mn_info
    mn_info = message.text
    msg = bot.send_message(message.chat.id, "Пожалуйста, напишите сферу вашего прпоекта из предложенных(it,education, finance)")
    bot.register_next_step_handler(msg, user_ans_category)


def user_ans_category(message):
    """Присваеваем переменной данные о сфере проекта
        Отправляем пользователю запрос на получание контактов для связи
        Вызываем следующую функцию с помощью "register_next_step_handler" """
    global cat
    cat = message.text
    msg = bot.send_message(message.chat.id, "Пожалуйста, введите контакты для связи с вами в telegram")
    bot.register_next_step_handler(msg, user_ans_use_name)

def user_ans_use_name(message):
    """Присваеваем переменной контакты для связи
        Отправляем пользователю запрос на получение желаемой суммы инвестиций
        Вызываем следующую функцию с помощью "register_next_step_handler" """
    global name_us
    name_us = message.text
    msg = bot.send_message(message.chat.id, "Пожалуйста, обозначьте желаемую сумму инвестиций(в руб)")
    bot.register_next_step_handler(msg, user_ans_money)


def user_ans_money(message):
    """Присваеваем переменной желаеммую сумму инвестиций и заносим все полученные данные в нашу бд.
    Оповещаем пользователя о том, что анкета создана."""
    global mon, new_database_len
    mon = message.text
    rnd_id = random.randint(10000000, 100000000)
    if rnd_id not in id_mass:
        db_table_val(id=rnd_id, user_id=usr_id, name_pr=nm_pr, main_info=mn_info, category=cat, money=mon, user_name=name_us)
        id_mass.append(rnd_id)  #конец заимствования структуры из проекта pyTelegramBotAPI
    else:
        while rnd_id in id_mass:
            rnd_id = random.randint(10000000, 100000000)
            db_table_val(id=rnd_id, user_id=usr_id, name_pr=nm_pr, main_info=mn_info, category=cat, money=mon, user_name=name_us)
            id_mass.append(rnd_id)


    cursor.execute('SELECT * FROM project')
    new_database_len = len(cursor.fetchall())

    if is_new:
        msg = bot.send_message(message.chat.id, "Анкета создана!")
    else:
        msg = bot.send_message(message.chat.id, "Возникла ошибка, попробуйте создать анкету еще раз")



@bot.message_handler(content_types=['text'])
def bot_message(message):
    """Функция для обработки сообщений поступающих от пользователя"""
    if message.chat.type == 'private':
        if message.text == 'Показать все проекты':
            cursor.execute('SELECT * FROM project')
            Mass_cort = cursor.fetchall()
            for i in range(len(Mass_cort)):
                Res_all_pr = "<b>id проекта</b> - " + str(Mass_cort[i][0]) + \
                    "\n" +\
                    "\n" "<b>Название проекта</b> - " + str(Mass_cort[i][3]) + \
                    "\n" + \
                    "\n" "<b>Категория проекта</b> - " + str(Mass_cort[i][4]) + \
                    "\n" + \
                    "\n" "<b>Предпологаяемые инвестиции(руб)</b> - " + str(Mass_cort[i][5]) + \
                    "\n" + \
                    "\n" "<b>Описание проекта:</b>   " + str(Mass_cort[i][2]) + \
                    "\n" + \
                    "\n" "<i>Контакты для связи</i> " + str((Mass_cort[i][6]))

                bot.send_message(message.chat.id, Res_all_pr,  parse_mode='html')

        elif message.text == 'Показать мои анкеты':
            cursor.execute('SELECT * FROM project')
            Mass_my_cort = cursor.fetchall()
            users_id = message.from_user.id
            for j in range(len(Mass_my_cort)):
                if Mass_my_cort[j][1] == users_id:
                    All_my_req = "<b>id проекта</b> - " + str(Mass_my_cort[j][0]) + \
                        "\n" + \
                        "\n" "<b>Название проекта</b> - " + str(Mass_my_cort[j][3]) + \
                        "\n" + \
                        "\n" "<b>Категория проекта</b> - " + str(Mass_my_cort[j][4]) + \
                        "\n" + \
                        "\n" "<b>Предпологаяемые инвестиции(руб)</b> - " + str(Mass_my_cort[j][5]) + \
                        "\n" + \
                        "\n" "<b>Описание проекта:</b>   " + str(Mass_my_cort[j][2]) + \
                        "\n" + \
                        "\n" "<i>Контакты для связи</i> " + str((Mass_my_cort[j][6]))
                    bot.send_message(message.chat.id, All_my_req, parse_mode='html')

        elif message.text == "Фильтры":
            bot.send_message(message.chat.id, "<b>Выберите необходимый фильтр из предложенного списка и напишите в чат:</b>"
                                              "\n"
                                              "\n" "<i>Название проекта X</i> - показывает проект с заджанным вами названием(X)" 
                                              "\n"
                                              "\n" "<i>Категория проекта</i> - показывает толлько проекты из выбранной вами категории()" 
                                              "\n"
                                              "\n" "<i>Сумма меньше X</i> - показывает проекты с предпологаемой суммой инвестиций менее заданного вами числа(X)"
                                              "\n"
                                              "\n" "<i>Сумма больше X</i> - показывает проекты с предпологаемой суммой инвестиций менее заданного вами числа(X)", parse_mode='html')

        elif project_name:
            cursor.execute('SELECT * FROM project')
            Mass_my_cort = cursor.fetchall()
            coun_ret = 0
            for ind in range(len(Mass_my_cort)):
                if Mass_my_cort[ind][3] in message.text:
                    coun_ret += 1
                    All_my_req = "<b>id проекта</b> - " + str(Mass_my_cort[ind][0]) + \
                                 "\n" + \
                                 "\n" "<b>Название проекта</b> - " + str(Mass_my_cort[ind][3]) + \
                                 "\n" + \
                                 "\n" "<b>Категория проекта</b> - " + str(Mass_my_cort[ind][4]) + \
                                 "\n" + \
                                 "\n" "<b>Предпологаяемые инвестиции(руб)</b> - " + str(Mass_my_cort[ind][5]) + \
                                 "\n" + \
                                 "\n" "<b>Описание проекта:</b>   " + str(Mass_my_cort[ind][2]) + \
                                 "\n" + \
                                 "\n" "<i>Контакты для связи</i> " + str((Mass_my_cort[ind][6]))


                    bot.send_message(message.chat.id, All_my_req, parse_mode='html')
            if coun_ret == 0:
                bot.send_message(message.chat.id, "К сожалению нам не удалось найти результаты удовлетворяющие вашим критериям. Попробуйте поменять значения или использовать другой фильтр.")

        elif poject_cat:
            cursor.execute('SELECT * FROM project')
            Mass_my_cort = cursor.fetchall()
            coun_ret = 0
            for ind in range(len(Mass_my_cort)):
                if Mass_my_cort[ind][4] in message.text:
                    coun_ret += 1
                    All_my_req = "<b>id проекта</b> - " + str(Mass_my_cort[ind][0]) + \
                                 "\n" + \
                                 "\n" "<b>Название проекта</b> - " + str(Mass_my_cort[ind][3]) + \
                                 "\n" + \
                                 "\n" "<b>Категория проекта</b> - " + str(Mass_my_cort[ind][4]) + \
                                 "\n" + \
                                 "\n" "<b>Предпологаяемые инвестиции(руб)</b> - " + str(Mass_my_cort[ind][5]) + \
                                 "\n" + \
                                 "\n" "<b>Описание проекта:</b>   " + str(Mass_my_cort[ind][2]) + \
                                 "\n" + \
                                 "\n" "<i>Контакты для связи</i> " + str((Mass_my_cort[ind][6]))

                    bot.send_message(message.chat.id, All_my_req, parse_mode='html')
            if coun_ret == 0:
                bot.send_message(message.chat.id, "К сожалению нам не удалось найти результаты удовлетворяющие вашим критериям. Попробуйте поменять значения или использовать другой фильтр.")

        elif summ_under:
            cursor.execute('SELECT * FROM project')
            Mass_my_cort = cursor.fetchall()
            money_lock = int(message.text.split()[-1])
            coun_ret = 0
            for ind in range(len(Mass_my_cort)):
                if int(Mass_my_cort[ind][5]) <= money_lock:
                    coun_ret += 1
                    All_my_req = "<b>id проекта</b> - " + str(Mass_my_cort[ind][0]) + \
                                 "\n" + \
                                 "\n" "<b>Название проекта</b> - " + str(Mass_my_cort[ind][3]) + \
                                 "\n" + \
                                 "\n" "<b>Категория проекта</b> - " + str(Mass_my_cort[ind][4]) + \
                                 "\n" + \
                                 "\n" "<b>Предпологаяемые инвестиции(руб)</b> - " + str(Mass_my_cort[ind][5]) + \
                                 "\n" + \
                                 "\n" "<b>Описание проекта:</b>   " + str(Mass_my_cort[ind][2]) + \
                                 "\n" + \
                                 "\n" "<i>Контакты для связи</i> " + str((Mass_my_cort[ind][6]))

                    bot.send_message(message.chat.id, All_my_req, parse_mode='html')
            if coun_ret == 0:
                bot.send_message(message.chat.id, "К сожалению нам не удалось найти результаты удовлетворяющие вашим критериям. Попробуйте поменять значения или использовать другой фильтр.")

        elif summ_up:
            cursor.execute('SELECT * FROM project')
            Mass_my_cort = cursor.fetchall()
            money_lock = int(message.text.split()[-1])
            coun_ret = 0
            for ind in range(len(Mass_my_cort)):
                if int(Mass_my_cort[ind][5])>= money_lock:
                    coun_ret += 1
                    All_my_req = "<b>id проекта</b> - " + str(Mass_my_cort[ind][0]) + \
                                 "\n" + \
                                 "\n" "<b>Название проекта</b> - " + str(Mass_my_cort[ind][3]) + \
                                 "\n" + \
                                 "\n" "<b>Категория проекта</b> - " + str(Mass_my_cort[ind][4]) + \
                                 "\n" + \
                                 "\n" "<b>Предпологаяемые инвестиции(руб)</b> - " + str(Mass_my_cort[ind][5]) + \
                                 "\n" + \
                                 "\n" "<b>Описание проекта:</b>   " + str(Mass_my_cort[ind][2]) + \
                                 "\n" + \
                                 "\n" "<i>Контакты для связи</i> " + str((Mass_my_cort[ind][6]))

                    bot.send_message(message.chat.id, All_my_req, parse_mode='html')
            if coun_ret == 0:
                bot.send_message(message.chat.id, "К сожалению нам не удалось найти результаты удовлетворяющие вашим критериям. Попробуйте поменять значения или использовать другой фильтр..")
        else:
            bot.send_message(message.chat.id, "Сообщение не распознано, пожалуйста, проверьте правильность введенной команды")


bot.polling(none_stop=True)