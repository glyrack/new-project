#Импортируемые библиотеки
import telebot
from telebot import types
import requests
import logging

#Ключи для бота, API погоды и логгирование
api_key = '' #Токен телеграм бота
weather_key = '' #API от сайта для получения погоды, по миру
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
logging.info("Бот запущен") #Вывод в консоль соо о запуске бота 


#Бот и переменные
bot = telebot.TeleBot(api_key)
waiting_city = set()
back_to = []
idmessage = False
speed = True
degre = True
lang = True
mess = None

#Меню для помощи по коммандам
bot.set_my_commands([types.BotCommand("start", "Запустить бота"),
    types.BotCommand("weather", "Узнать погоду"), 
    types.BotCommand("info", "Информация по боту")])



""" ------ Запуск бота и меню ------ """
#Обработчик стартовых команд
@bot.message_handler(commands=['start'])
def language(message):
    global mess
    mess = message
    logger.info("Пользователь %s (%s) вызвал /start", message.from_user.username, message.chat.id)
    waiting_city.discard(message.chat.id)
    if lang == True:
        ru = "🇷🇺 Russian"
        en = "🇬🇧 English"
        la = "Choose a language:"
    else:
        ru = "🇷🇺 Русский"
        en = "🇬🇧 Английский"
        la = "Выберите язык:"
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton(ru, callback_data="ru"), types.InlineKeyboardButton(en, callback_data="en"))
    bot.send_message(message.chat.id, la, parse_mode="HTML", reply_markup=markup)

#Главное меню
def main(message):
    logger.info("Пользователь %s (%s) вошёл в меню", message.from_user.username, message.chat.id)
    global idmessage, back_to
    if lang == True: 
        l = "Hello 👋, i'm a weather bot! 🤖\n\nSend me the <b>name of the city</b> and i will give you the current weather information.\n\nWrite the name of the city in English or Russian language.\n\nFor example: London, New York, Paris, etc."
        i = "ℹ️ Info"
        o = "⚙️ Options"
        w = "🌤 Weather in the city"
    else: 
        l = "Привет 👋, я — погодный бот! 🤖\n\nПришли мне <b>название города</b>, и я сообщу тебе актуальную информацию по погоде.\n\nНазвание города можно написать на английском или русском языке.\n\nНапример: Лондон, Нью-Йорк, Париж и т. д."
        i = "ℹ️ Информация"
        o = "⚙️ Настройки"
        w = "🌤 Погода в городе"
    markup = types.InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
    inf_button = types.InlineKeyboardButton(i, callback_data="info")
    option = types.InlineKeyboardButton(o, callback_data="options")
    markup.add(option, inf_button)
    weaTher_button = types.InlineKeyboardButton(w, callback_data="weather")
    markup.add(weaTher_button)
    bot.send_chat_action(message.chat.id, "typing")
    bot.send_message(message.chat.id, l, parse_mode="HTML", reply_markup=markup)
    idmessage = False
    back_to.clear()
    #print(list(back_to))



""" ------ Вкладка информации о боте ------ """
#Обработчик комманды информации о боте
@bot.message_handler(commands=["info"])
def inf(message):
    logger.info("Пользователь %s (%s) перешёл в 'Информацию'", message.from_user.username, message.chat.id)
    if lang == True:
        m = "☰ Menu"
        information = "This bot was created by @FLLNKNG.\n\nIt provides weather information for cities around the world.\n\nYou can send the name of the city in English and get the current weather data.\n\nFor example: London, New York, Paris, etc."
    else:
        m = "☰ Меню"
        information = "Данный бот создан @FLLNKNG.\n\nОн предоставляет информацию по погоде для городов по всему миру.\n\nВы можете отправить название города на Русском и получить информацию по погоде на нынешнюю дату.\n\nНапример: Лондон, Нью Йорк, Париж и т.д."
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton(m, callback_data="menu"))
    bot.send_message(message.chat.id, information,  parse_mode="HTML", reply_markup=markup)

#Обработчик кнопки информации о боте
@bot.callback_query_handler(func=lambda call: call.data == "info")
def info_bot(call):
    bot.answer_callback_query(call.id)
    logger.info("Пользователь %s (%s) перешёл в 'Информацию'", call.message.from_user.username, call.message.chat.id)
    back_undo(call.data)
    if lang == True:
        b = "⬅️Back"
        information = "This bot was created by @FLLNKNG.\n\nIt provides weather information for cities around the world.\n\nYou can send the name of the city in English and get the current weather data.\n\nFor example: London, New York, Paris, etc."
    else:
        b = "⬅️Назад"
        information = "Данный бот создан @FLLNKNG.\n\nОн предоставляет информацию по погоде для городов по всему миру.\n\nВы можете отправить название города на Русском и получить информацию по погоде на нынешнюю дату.\n\nНапример: Лондон, Нью Йорк, Париж и т.д."
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton(b, callback_data="back"))
    bot.edit_message_text(information, call.message.chat.id, call.message.message_id,  parse_mode="HTML", reply_markup=markup)



""" ------ Плашка настроек ------ """
#Обработка вызова меню настроек
@bot.callback_query_handler(func=lambda call: call.data == "options")
def parametr(call):
    bot.answer_callback_query(call.id)
    logger.info("Пользователь %s (%s) зашёл в Настройки", call.message.from_user.username, call.message.chat.id)
    back_undo("options")
    if lang == True: 
        c = "🌐 Change language"
        w = "💨 Wind speed"
        d = "🌡️ Degrees"
        b = "⬅️Back"
        op = "Configuration options: "
        cus = "🔧 Customize"
    else: 
        c = "🌐 Изменить язык"
        w = "💨 скорость ветра"
        d = "🌡️ градусы"
        b = "⬅️Назад"
        op = "Конфигурации настроек:"
        cus = "🔧 Настройка"
    markup = types.InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
    markup.add(types.InlineKeyboardButton(c, callback_data="change_language"), types.InlineKeyboardButton(cus, callback_data="customize"))
    markup.add(types.InlineKeyboardButton(w, callback_data="wind"), types.InlineKeyboardButton(d, callback_data="degree"))
    markup.add(types.InlineKeyboardButton(b, callback_data="back"))
    bot.edit_message_text(op, call.message.chat.id, call.message.message_id, reply_markup=markup)
    #print(list(back_to))
    
we_sos = True
temp_sos = True
fel_sos = True
hum_sos = True
pres_sos = True
wind_sos = True

def sostoyanie(name, state):
    return f"{name} - {"✅" if state else "❌"}"

@bot.callback_query_handler(func=lambda call: call.data == "customize")
def custom(call):
    bot.answer_callback_query(call.id)
    global back_to
    b = "⬅️Назад"
    c = "Configuration:"
    markup = types.InlineKeyboardMarkup(row_width=7)
    markup.add(types.InlineKeyboardButton(sostoyanie("Погодные условия", we_sos), callback_data="wetr"))
    markup.add(types.InlineKeyboardButton(sostoyanie("Температура", temp_sos), callback_data="temptr"))
    markup.add(types.InlineKeyboardButton(sostoyanie("Ощущение погоды", fel_sos), callback_data="feltr"))
    markup.add(types.InlineKeyboardButton(sostoyanie("Влажность", hum_sos), callback_data="humtr"))
    markup.add(types.InlineKeyboardButton(sostoyanie("Давление", pres_sos), callback_data="prestr"))
    markup.add(types.InlineKeyboardButton(sostoyanie("Скорость ветра", wind_sos), callback_data="windtr"))
    markup.add(types.InlineKeyboardButton(b, callback_data="back"))
    bot.edit_message_text(c, call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "wetr")
def wetr(call):
    global we_sos
    we_sos = (not we_sos)
    custom(call)
@bot.callback_query_handler(func=lambda call: call.data == "temptr")
def temptr(call):
    global temp_sos
    temp_sos = (not temp_sos)
    custom(call)
@bot.callback_query_handler(func=lambda call: call.data == "feltr")
def feltr(call):
    global fel_sos
    fel_sos = (not fel_sos)
    custom(call)
@bot.callback_query_handler(func=lambda call: call.data == "humtr")
def humtr(call):
    global hum_sos
    hum_sos = (not hum_sos)
    custom(call)
@bot.callback_query_handler(func=lambda call: call.data == "prestr")
def prestr(call):
    global pres_sos
    pres_sos = (not pres_sos)
    custom(call)
@bot.callback_query_handler(func=lambda call: call.data == "windtr")
def windtr(call):
    global wind_sos
    wind_sos = (not wind_sos)
    custom(call)

#Обработка вызова меню отображения скорости ветра 
@bot.callback_query_handler(func=lambda call: call.data == "wind")
def wind_speed(call):
    bot.answer_callback_query(call.id)
    logger.info("Пользователь %s (%s) зашёл в настройки Скорости ветра", call.message.from_user.username, call.message.chat.id)
    global back_to
    back_to.append("wind")
    if lang == True:
        k = "km/h"
        m = "m/s"
        b = "⬅️Back"
        s = "Show concept speed:"
    else:
        m = "м/с"
        k = "км/ч"
        b = "⬅️Назад"
        s = "Отображение скорости:"
    markup = types.InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
    markup.add(types.InlineKeyboardButton(m, callback_data="metr"))
    markup.add(types.InlineKeyboardButton(k, callback_data="kilometr"))
    markup.add(types.InlineKeyboardButton(b, callback_data="back"))
    bot.edit_message_text(s, call.message.chat.id, call.message.message_id, reply_markup=markup)
    #print(list(back_to))    

#Обработчик кнопки смены отобркежения в м/с
@bot.callback_query_handler(func=lambda call: call.data == "metr")
def metres(call):
    bot.answer_callback_query(call.id)
    logger.info("Пользователь %s (%s) выбрал отображение в м/с", call.message.from_user.username, call.message.chat.id)
    global speed
    speed = True
    if lang == True: 
        m = "Wind speed will be displayed in meters per second."
    else: 
        m = "Скорость ветра будет отображаться в метрах в секунду."
    bot.edit_message_text(m, call.message.chat.id, call.message.message_id, parse_mode="HTML")
    main(call.message)

#Обработчик кнопки смены отображения в км/ч
@bot.callback_query_handler(func=lambda call: call.data == "kilometr")
def kilo(call):
    bot.answer_callback_query(call.id)
    logger.info("Пользователь %s (%s) выбрал отображение в км/ч", call.message.from_user.username, call.message.chat.id)
    global speed
    speed = False
    if lang == True: 
        k = "Wind speed will be displayed in kilometers per hour."
    else: 
        k = "Скорость ветра будет отображаться в километрах в час."
    bot.edit_message_text(k, call.message.chat.id, call.message.message_id, parse_mode="HTML")
    main(call.message)
    

#Обработчик кнопки смены отображения температуры
@bot.callback_query_handler(func=lambda call: call.data == "degree")
def degree(call):
    bot.answer_callback_query(call.id)
    logger.info("Пользователь %s (%s) зашёл в настройки Температуры", call.message.from_user.username, call.message.chat.id)
    global back_to
    back_to.append("degree")
    if lang == True:
        b = "⬅️Back"
        s = "Show concept degree:"
    else:
        b = "⬅️Назад"
        s = "Отображение температуры:"
    markup = types.InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
    markup.add(types.InlineKeyboardButton("°C", callback_data="calls"))
    markup.add(types.InlineKeyboardButton("°F", callback_data="fareng"))
    markup.add(types.InlineKeyboardButton(b, callback_data="back"))
    bot.edit_message_text(s, call.message.chat.id, call.message.message_id, reply_markup=markup)
    #print(list(back_to))

#Обработчик кнопки смены отображения в цельсиях
@bot.callback_query_handler(func=lambda call: call.data == "calls")
def cal(call):
    bot.answer_callback_query(call.id)
    logger.info("Пользователь %s (%s) выбрал отображение Цельсиях", call.message.from_user.username, call.message.chat.id)
    global degre
    degre = True
    if lang == True:
        text = "Temperature readings will be displayed in Celsius."
    else:
        text = "Показатели температуры будут отображаться в Цельсиях."
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="HTML")
    main(call.message)

#Обработчик кнопки смены отображения в фаренгейтах
@bot.callback_query_handler(func=lambda call: call.data == "fareng")
def cal(call):
    bot.answer_callback_query(call.id)
    logger.info("Пользователь %s (%s) выбрал отображение в Фаренгейтах", call.message.from_user.username, call.message.chat.id)
    global degre
    degre = False
    if lang == True:
        text = "Temperature readings will be displayed in Fahrenheit."
    else:
        text = "Показатели температуры будут отображаться в Фаренгейтах."
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="HTML")
    main(call.message)
    
#Обработчик кнопки смены языка
@bot.callback_query_handler(func=lambda call: call.data == "change_language")
def change_language(call):
    bot.answer_callback_query(call.id)
    logger.info("Пользователь %s (%s) зашёл в 'настройки языка интерфейса'", call.message.from_user.username, call.message.chat.id)
    global back_to
    back_to.append("change_language")
    if lang == True:
        b = "⬅️Back"
        ru = "🇷🇺 Russian"
        en = "🇬🇧 English"
        la = "Choose a language:"
    else:
        b = "⬅️Назад"
        ru = "🇷🇺 Русский"
        en = "🇬🇧 Английский"
        la = "Выберите язык:"
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(ru, callback_data="ru"), types.InlineKeyboardButton(en, callback_data="en"))
    markup.add(types.InlineKeyboardButton(b, callback_data="back"))
    bot.edit_message_text(la, call.message.chat.id, call.message.message_id, reply_markup=markup)
    #print(list(back_to))

#Обработчик кнопки русского языка в меню настроек
@bot.callback_query_handler(func=lambda call: call.data == "ru")
def russian(call):
    logger.info("Пользователь %s (%s) выбрал отображение интерфейса на 'Русском языке'", call.message.from_user.username, call.message.chat.id)
    global lang
    lang = False
    bot.edit_message_text("Выбран <b>Русский</b> язык.", call.message.chat.id, call.message.message_id, parse_mode="HTML")
    main(call.message)

#Обработчик кнопки английского языка в меню настроек
@bot.callback_query_handler(func=lambda call: call.data == "en")
def english(call):
    logger.info("Пользователь %s (%s) выбрал отображение интерфейса на 'Английском языке'", call.message.from_user.username, call.message.chat.id)
    global lang
    lang = True
    bot.edit_message_text("<b>English</b> language selected", call.message.chat.id, call.message.message_id, parse_mode="HTML")
    main(call.message)



""" ------ Комманды на возвращение в меню и отмену действий ------ """
#Обработчик кнопки возврата в главное меню
@bot.callback_query_handler(func=lambda call: call.data == "back")
def back_to_menu(call):
    bot.answer_callback_query(call.id)
    logger.info("Пользователь %s (%s) нажал кнопку 'Назад'", call.message.from_user.username, call.message.chat.id)
    global back_to, idmessage
    if back_to:
        back_to.pop()
    if not back_to:
        if idmessage == True:
            main(call.message)
        else:
            if lang == True: 
                l = "Hello 👋, i'm a weather bot! 🤖\n\nSend me the <b>name of the city</b> and i will give you the current weather information.\n\nWrite the name of the city in English or Russian language.\n\nFor example: London, New York, Paris, etc."
                i = "ℹ️ Info"
                o = "⚙️ Options"
                w = "🌤 Weather in the city"
            else:
                l = "Привет 👋, я — погодный бот! 🤖\n\nПришли мне <b>название города</b>, и я сообщу тебе актуальную информацию по погоде.\n\nНазвание города можно написать на английском или русском языке.\n\nНапример: Лондон, Нью-Йорк, Париж и т. д."
                i = "ℹ️ Информация"
                o = "⚙️ Настройки"
                w = "🌤 Погода в городе"
            markup = types.InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
            inf_button = types.InlineKeyboardButton(i, callback_data="info")
            option = types.InlineKeyboardButton(o, callback_data="options")
            markup.add(option, inf_button)
            weaTher_button = types.InlineKeyboardButton(w, callback_data="weather")
            markup.add(weaTher_button)
            bot.edit_message_text(l, call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=markup)
            idmessage = False
    else:
        if back_to[-1] == "options":
            parametr(call)
    waiting_city.discard(call.message.chat.id)

#Вспомогательная функция для работы кнопки "назад"
def back_undo(call):
    global back_to
    back_to.clear()
    back_to.append(call)

#Вызов главного меню
@bot.callback_query_handler(func=lambda call: call.data == "menu")
def men(call):
    bot.answer_callback_query(call.id)
    main(call.message)


""" ------ Комманды на получение погоды и проверку кнопки на активность ------ """
#Обработчик кнопки получения погоды
@bot.callback_query_handler(func=lambda call: call.data == "weather")
def weather_info(call):
    bot.answer_callback_query(call.id)
    back_undo(call.data)
    if lang == True:
        b = "⬅️Back"
        text = "Please send me the name of the city in English to get the current weather information:"
    else:
        b = "⬅️Назад"
        text = "Пожалуйста отправь мне название города на Русском для выдачи информации по погоде:"
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton(b, callback_data="back"))
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=markup)
    waiting_city.add(call.message.chat.id)

#Обработка запроса на получение погоды
@bot.message_handler(commands=['weather'])
def weather_inf(message):
    if lang == True:
        text = "Please send me the name of the city in English to get the current weather information:"
    else:
        text = "Пожалуйста отправь мне название города на Русском для выдачи информации по погоде:"
    bot.send_message(message.chat.id, text, parse_mode="HTML")
    waiting_city.add(message.chat.id)

#Обработчик получения города от пользователя
@bot.message_handler(func=lambda m: m.chat.id in waiting_city)
def info(message):
    logger.info(f"Пользователь %s (%s) написал в чат бота {message.text}", message.from_user.username, message.chat.id)
    global mess
    mess = message
    waiting_city.discard(message.chat.id)
    bot.send_chat_action(message.chat.id, "typing")
    send_weather(message.chat.id, message.text)

#Обработчик, нажата ли кнопка погоды, прежде, чем осуществлять ввод
@bot.message_handler(func=lambda m: m.chat.id not in waiting_city)
def notinfo(message):
    if message.text == "67": #Пасхалке
        bot.send_animation(message.chat.id, "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExaGVqd3p0b2N6cXJzdWliN216bzFlYjRjeXl2Mzhja3liem51cjZ0cyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/u4tXnIkMYNI1zKlbrW/giphy.gif")
        logger.info("Пользователь %s (%s) тиктокерский деградант", message.from_user.username, message.chat.id)
        return
    markup = types.InlineKeyboardMarkup(row_width=1)
    if lang == True:
        weather = "🌤 Weather in the city"
        warn = "Please click the <b>button</b> to get weather information."
    else:
        weather = "🌤 Погода в городе"
        warn = "Пожалуйста нажмите <b>кнопку</b> для получения информации по погоде."
    markup.add(types.InlineKeyboardButton(weather, callback_data="weather"))
    bot.send_message(message.chat.id, warn, parse_mode="HTML", reply_markup=markup)

#Функция для получения погоды
def get_weather(city):
    if lang == True:
        lan = "en"
    else:
        lan = "ru"
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": weather_key, "units": "metric", "lang": lan}
    response = requests.get(url, params=params, timeout=10)
    if response.status_code == 404:
        return
    if response.status_code == 400:
        return
    response.raise_for_status()
    return response.json()
         
#Функция форматирования-вывода погоды
def format_weather(chat_id, city, data):
    if data['wind']['speed'] >= 0 and data['wind']['speed'] <= 0.2:
        if lang == True:
            weather_speed = "Calm"
        else:
            weather_speed = "Штиль"
    elif data['wind']['speed'] >= 0.3 and data['wind']['speed'] <= 7.9:
        if lang == True:
            weather_speed = "Light wind"
        else:
            weather_speed = "Слабый ветер"
    elif data['wind']['speed'] >= 8 and data['wind']['speed'] <= 20.7:
        if lang == True:
            weather_speed = "Strong wind"
        else:
            weather_speed = "Сильный ветер"
    else:
        if lang == True:
            weather_speed = "Storm"
        else:
            weather_speed = "Шторм"
    if speed == True:
        if lang == True:
            wind_sp = f"{round((data['wind']['speed']), 2)} m/s"
        else:
            wind_sp = f"{round((data['wind']['speed']), 2)} м/с"
    elif speed == False:
        form = round((data['wind']['speed'] * 3.6), 2)
        if lang == True:
            wind_sp = f"{form} km/h"
        else:
            wind_sp = f"{form} км/ч"
    if degre == True:
        temper = f"{data['main']['temp']:.0f}°C"
        feels = f"{data['main']['feels_like']:.0f}°C"
    elif degre == False:
        znach1 = (data['main']['temp']) * 1.8 + 32
        temper = f"{znach1:.0f}°F"
        znach2 = (data['main']['feels_like']) * 1.8 + 32
        feels = f"{znach2:.0f}°F"
    if lang == True:
        we = "Weather in"
        w = "Weather:"
        t = "Temperature:"
        f = "Feels like:"
        h = "Humidity:"
        p = "Pressure:"
        wi = "Wind:"
        hp = "hPa"
        m = "☰ Menu"
    else:
        we = "Погода в"
        w = "Погода:"
        t = "Температура:"
        f = "Ощущается как:"
        h = "Влажность:"
        p = "Давление:"
        wi = "Ветер:"
        hp = "гПа"
        m = "☰ Меню"
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton(m, callback_data="back"))
    bot.send_message(chat_id, f"{we} <b>{city.title()}</b>:\n\n" +
                f"🌍 <b>{data['name']}, {data['sys']['country']}</b>\n"
                f"☁️ {w} <b>{data['weather'][0]['description'].capitalize()}</b>\n"
                f"🌡 {t} <b>{temper}</b>\n"
                f"🔎 {f} <b>{feels}</b>\n"
                f"💧 {h} <b>{data['main']['humidity']}%</b>\n"
                f"🧭 {p} <b>{data['main']['pressure']} {hp}</b>\n"
                f"💨 {wi} <b>{wind_sp}</b> ({weather_speed})\n", 
                parse_mode="HTML", reply_markup=markup)
    global idmessage
    idmessage = True
    logger.info(f"Пользователь %s (%s) получил погоду города {data['name']}, страны {data['sys']['country']}", mess.from_user.username, chat_id)

#Функция для отправки погоды
def send_weather(chat_id, city):
    try:
       data = get_weather(city)
    except requests.RequestException:
        if lang == True: 
            err = "Error, please try again later."
        else:
            err = "Ошибка, пожалуйста попробуйте позже."
        bot.send_message(chat_id, err)
        waiting_city.add(chat_id)
    if data is None:
        if lang == True:
             err = "City not found!"
        else:
            err = "Город не найден!"
        bot.send_message(chat_id, err)
        waiting_city.add(chat_id)
        return
    format_weather(chat_id, city, data)

#Запуска бота
bot.polling(non_stop=True)