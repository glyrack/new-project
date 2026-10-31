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
TEXT = {"en":{"ru":"🇷🇺 Russian", "en":"🇬🇧 English", "la":"Choose a language:", "hello":"Hello 👋, i'm a weather bot! 🤖\n\nSend me the <b>name of the city</b> and i will give you the current weather information.\n\nWrite the name of the city in English or Russian language.\n\nFor example: London, New York, Paris, etc.",
              "inf":"ℹ️ Info", "opt":"⚙️ Options", "witc":"🌤 Weather in the city", "menu":"☰ Menu", "information":"This bot was created by @FLLNKNG.\n\nIt provides weather information for cities around the world.\n\nYou can send the name of the city in English and get the current weather data.\n\nFor example: London, New York, Paris, etc.",
              "b":"⬅️ Back", "Cl":"🌐 Change language", "ws":"💨 Wind speed", "dgrs":"🌡️ Degrees", "op":"Configuration options:", "cus":"🔧 Customize", "conf":"Configuration:", "kh":"km/h", "ms":"m/s",
              "scs":"Show concept speed:", "wswms":"Wind speed will be displayed in meters per second.", "wswkh": "Wind speed will be displayed in kilometers per hour.", "scd":"Show concept degree:", 
              "trc":"Temperature readings will be displayed in Celsius.", "trf":"Temperature readings will be displayed in Fahrenheit.", "psm":"Please send me the name of the city in English to get the current weather information:",
              "pctb":"Please click the <b>button</b> to get weather information.", "lan":"en", "wi":"Weather in", "weat":"Weather:", "temper":"Temperature:", "fl":"Feels like:", "hum":"Humidity", "pres":"Pressure",
              "wind":"Wind:", "hp":"hPa", "err1":"Error, please try again later.", "err2":"City not found!",
              "calm":"Calm", "lw":"Light wind", "sw":"Strong wind", "storm":"Storm"},
        "ru":{"ru":"🇷🇺 Русский", "en":"🇬🇧 Английский", "la":"Выберите язык:", "hello":"Привет 👋, я — погодный бот! 🤖\n\nПришли мне <b>название города</b>, и я сообщу тебе актуальную информацию по погоде.\n\nНазвание города можно написать на английском или русском языке.\n\nНапример: Лондон, Нью-Йорк, Париж и т. д.", 
              "inf":"ℹ️ Информация", "opt":"⚙️ Настройки", "witc":"🌤 Погода в городе", "menu":"☰ Меню", "information":"Этот бот создан пользователем @FLLNKNG.\n\nОн предоставляет информацию о погоде в городах по всему миру.\n\nВы можете отправить название города на английском языке и получить актуальные данные о погоде.\n\nНапример: London, New York, Paris и т. д.",
              "b":"⬅️ Назад", "Cl":"🌐 Изменить язык", "ws":"💨 Скорость ветра", "dgrs":"🌡️ Градусы", "op":"Конфигурации настроек:", "cus":"🔧 Настройка", "conf":"Конфигурация:", "kh":"Км/ч", "ms":"М/с",
              "scs":"Отображение скорости:", "wswms":"Скорость ветра будет отображаться в метрах в секунду.", "wswkh": "Скорость ветра будет отображаться в километрах в час.", "scd":"Отображение температуры:",
              "trc":"Показатели температуры будут отображаться в Цельсиях.", "trf":"Показатели температуры будут отображаться в Фаренгейтах.", "psm":"Пожалуйста отправь мне название города на Русском для выдачи информации по погоде:",
              "pctb":"Пожалуйста нажмите <b>кнопку</b> для получения информации по погоде.", "lan":"ru", "wi":"Погода в", "weat":"Погода:", "temper":"Температура:", "fl":"Ощущается как:", "hum":"Влажность:", "pres":"Давление:",
              "wind":"Ветер:", "hp":"гПа", "err1":"Ошибка, пожалуйста попробуйте позже.", "err2":"Город не найден!", 
              "calm":"Штиль", "lw":"Слабый ветер", "sw":"Сильный ветер", "storm":"Шторм"}}
waiting_city = set()
back_to = []
idmessage = False
speed = True
degre = True
mess = None
lang = True
lg = TEXT["en" if lang else "ru"]

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
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton(lg["ru"], callback_data="ru"), types.InlineKeyboardButton(lg["en"], callback_data="en"))
    bot.send_message(message.chat.id, lg["la"], parse_mode="HTML", reply_markup=markup)

#Главное меню
def main(message):
    logger.info("Пользователь %s (%s) вошёл в меню", message.from_user.username, message.chat.id)
    global idmessage, back_to
    markup = types.InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
    inf_button = types.InlineKeyboardButton(lg["inf"], callback_data="info")
    option = types.InlineKeyboardButton(lg["opt"], callback_data="options")
    markup.add(option, inf_button)
    weaTher_button = types.InlineKeyboardButton(lg["witc"], callback_data="weather")
    markup.add(weaTher_button)
    bot.send_chat_action(message.chat.id, "typing")
    bot.send_message(message.chat.id, lg["hello"], parse_mode="HTML", reply_markup=markup)
    idmessage = False
    back_to.clear()



""" ------ Вкладка информации о боте ------ """
#Обработчик комманды информации о боте
@bot.message_handler(commands=["info"])
def inf(message):
    logger.info("Пользователь %s (%s) перешёл в 'Информацию'", message.from_user.username, message.chat.id)
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton(lg["menu"], callback_data="menu"))
    bot.send_message(message.chat.id, lg["information"],  parse_mode="HTML", reply_markup=markup)

#Обработчик кнопки информации о боте
@bot.callback_query_handler(func=lambda call: call.data == "info")
def info_bot(call):
    bot.answer_callback_query(call.id)
    logger.info("Пользователь %s (%s) перешёл в 'Информацию'", call.message.from_user.username, call.message.chat.id)
    back_undo(call.data)
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton(lg["b"], callback_data="back"))
    bot.edit_message_text(lg["information"], call.message.chat.id, call.message.message_id,  parse_mode="HTML", reply_markup=markup)



""" ------ Плашка настроек ------ """
#Обработка вызова меню настроек
@bot.callback_query_handler(func=lambda call: call.data == "options")
def parametr(call):
    bot.answer_callback_query(call.id)
    logger.info("Пользователь %s (%s) зашёл в Настройки", call.message.from_user.username, call.message.chat.id)
    back_undo("options")
    markup = types.InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
    markup.add(types.InlineKeyboardButton(lg["Cl"], callback_data="change_language"), types.InlineKeyboardButton(lg["cus"], callback_data="customize"))
    markup.add(types.InlineKeyboardButton(lg["ws"], callback_data="wind"), types.InlineKeyboardButton(lg["dgrs"], callback_data="degree"))
    markup.add(types.InlineKeyboardButton(lg["b"], callback_data="back"))
    bot.edit_message_text(lg["op"], call.message.chat.id, call.message.message_id, reply_markup=markup)
    
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
    back_to.append("customize")
    markup = types.InlineKeyboardMarkup(row_width=7)
    markup.add(types.InlineKeyboardButton(sostoyanie("Погодные условия", we_sos), callback_data="wetr"))
    markup.add(types.InlineKeyboardButton(sostoyanie("Температура", temp_sos), callback_data="temptr"))
    markup.add(types.InlineKeyboardButton(sostoyanie("Ощущение погоды", fel_sos), callback_data="feltr"))
    markup.add(types.InlineKeyboardButton(sostoyanie("Влажность", hum_sos), callback_data="humtr"))
    markup.add(types.InlineKeyboardButton(sostoyanie("Давление", pres_sos), callback_data="prestr"))
    markup.add(types.InlineKeyboardButton(sostoyanie("Скорость ветра", wind_sos), callback_data="windtr"))
    markup.add(types.InlineKeyboardButton(lg["b"], callback_data="back"))
    bot.edit_message_text(lg["conf"], call.message.chat.id, call.message.message_id, reply_markup=markup)

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
    markup = types.InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
    markup.add(types.InlineKeyboardButton(lg["ms"], callback_data="metr"))
    markup.add(types.InlineKeyboardButton(lg["kh"], callback_data="kilometr"))
    markup.add(types.InlineKeyboardButton(lg["b"], callback_data="back"))
    bot.edit_message_text(lg["scs"], call.message.chat.id, call.message.message_id, reply_markup=markup) 

#Обработчик кнопки смены отобркежения в м/с
@bot.callback_query_handler(func=lambda call: call.data == "metr")
def metres(call):
    bot.answer_callback_query(call.id)
    logger.info("Пользователь %s (%s) выбрал отображение в м/с", call.message.from_user.username, call.message.chat.id)
    global speed
    speed = True
    bot.edit_message_text(lg["wswms"], call.message.chat.id, call.message.message_id, parse_mode="HTML")
    main(call.message)

#Обработчик кнопки смены отображения в км/ч
@bot.callback_query_handler(func=lambda call: call.data == "kilometr")
def kilo(call):
    bot.answer_callback_query(call.id)
    logger.info("Пользователь %s (%s) выбрал отображение в км/ч", call.message.from_user.username, call.message.chat.id)
    global speed
    speed = False
    bot.edit_message_text(lg["wswkh"], call.message.chat.id, call.message.message_id, parse_mode="HTML")
    main(call.message)
    

#Обработчик кнопки смены отображения температуры
@bot.callback_query_handler(func=lambda call: call.data == "degree")
def degree(call):
    bot.answer_callback_query(call.id)
    logger.info("Пользователь %s (%s) зашёл в настройки Температуры", call.message.from_user.username, call.message.chat.id)
    global back_to
    back_to.append("degree")
    markup = types.InlineKeyboardMarkup(row_width=3, one_time_keyboard=True)
    markup.add(types.InlineKeyboardButton("°C", callback_data="calls"))
    markup.add(types.InlineKeyboardButton("°F", callback_data="fareng"))
    markup.add(types.InlineKeyboardButton(lg["b"], callback_data="back"))
    bot.edit_message_text(lg["scd"], call.message.chat.id, call.message.message_id, reply_markup=markup)

#Обработчик кнопки смены отображения в цельсиях
@bot.callback_query_handler(func=lambda call: call.data == "calls")
def cal(call):
    bot.answer_callback_query(call.id)
    logger.info("Пользователь %s (%s) выбрал отображение Цельсиях", call.message.from_user.username, call.message.chat.id)
    global degre
    degre = True
    bot.edit_message_text(lg["trc"], call.message.chat.id, call.message.message_id, parse_mode="HTML")
    main(call.message)

#Обработчик кнопки смены отображения в фаренгейтах
@bot.callback_query_handler(func=lambda call: call.data == "fareng")
def cal(call):
    bot.answer_callback_query(call.id)
    logger.info("Пользователь %s (%s) выбрал отображение в Фаренгейтах", call.message.from_user.username, call.message.chat.id)
    global degre
    degre = False
    bot.edit_message_text(lg["trf"], call.message.chat.id, call.message.message_id, parse_mode="HTML")
    main(call.message)
    
#Обработчик кнопки смены языка
@bot.callback_query_handler(func=lambda call: call.data == "change_language")
def change_language(call):
    bot.answer_callback_query(call.id)
    logger.info("Пользователь %s (%s) зашёл в 'настройки языка интерфейса'", call.message.from_user.username, call.message.chat.id)
    global back_to
    back_to.append("change_language")
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(lg["ru"], callback_data="ru"), types.InlineKeyboardButton(lg["en"], callback_data="en"))
    markup.add(types.InlineKeyboardButton(lg["b"], callback_data="back"))
    bot.edit_message_text(lg["la"], call.message.chat.id, call.message.message_id, reply_markup=markup)

#Обработчик кнопки русского языка в меню настроек
@bot.callback_query_handler(func=lambda call: call.data == "ru")
def russian(call):
    logger.info("Пользователь %s (%s) выбрал отображение интерфейса на 'Русском языке'", call.message.from_user.username, call.message.chat.id)
    global lg
    lang = False
    lg = TEXT["en" if lang else "ru"]
    bot.edit_message_text("Выбран <b>Русский</b> язык.", call.message.chat.id, call.message.message_id, parse_mode="HTML")
    main(call.message)

#Обработчик кнопки английского языка в меню настроек
@bot.callback_query_handler(func=lambda call: call.data == "en")
def english(call):
    logger.info("Пользователь %s (%s) выбрал отображение интерфейса на 'Английском языке'", call.message.from_user.username, call.message.chat.id)
    global lg
    lang = True
    lg = TEXT["en" if lang else "ru"]
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
            markup = types.InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
            inf_button = types.InlineKeyboardButton(lg["inf"], callback_data="info")
            option = types.InlineKeyboardButton(lg["opt"], callback_data="options")
            markup.add(option, inf_button)
            weaTher_button = types.InlineKeyboardButton(lg["witc"], callback_data="weather")
            markup.add(weaTher_button)
            bot.edit_message_text(lg["hello"], call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=markup)
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
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton(lg["b"], callback_data="back"))
    bot.edit_message_text(lg["psm"], call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=markup)
    waiting_city.add(call.message.chat.id)

#Обработка запроса на получение погоды
@bot.message_handler(commands=['weather'])
def weather_inf(message):
    bot.send_message(message.chat.id, lg["psm"], parse_mode="HTML")
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
    markup.add(types.InlineKeyboardButton(lg["witc"], callback_data="weather"))
    bot.send_message(message.chat.id, lg["pctb"], parse_mode="HTML", reply_markup=markup)

#Функция для получения погоды
def get_weather(city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": weather_key, "units": "metric", "lang": lg["lan"]}
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
        weather_speed = lg["calm"]
    elif data['wind']['speed'] >= 0.3 and data['wind']['speed'] <= 7.9: 
        weather_speed = lg["lw"]
    elif data['wind']['speed'] >= 8 and data['wind']['speed'] <= 20.7: 
        weather_speed = "sw"
    else: weather_speed = lg["storm"]
    if speed == True: 
        wind_sp = f"{round((data['wind']['speed']), 2), lg["ms"]}"
    elif speed == False: 
        wind_sp = f"{round((data['wind']['speed'] * 3.6), 2), lg["kh"]}"
    if degre == True:
        temper = f"{data['main']['temp']:.0f}°C"
        feels = f"{data['main']['feels_like']:.0f}°C"
    elif degre == False:
        znach1 = (data['main']['temp']) * 1.8 + 32
        temper = f"{znach1:.0f}°F"
        znach2 = (data['main']['feels_like']) * 1.8 + 32
        feels = f"{znach2:.0f}°F"
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton(lg["menu"], callback_data="back"))
    vivod = (f"{lg["wi"]} <b>{city.title()}</b>:\n\n" + f"🌍 <b>{data['name']}, {data['sys']['country']}</b>\n" +
                output(f"☁️ {lg["weat"]} <b>{data['weather'][0]['description'].capitalize()}</b>\n", we_sos) +
                output(f"🌡 {lg["temper"]} <b>{temper}</b>\n", temp_sos) +
                output(f"🔎 {lg["fl"]} <b>{feels}</b>\n", fel_sos) +
                output(f"💧 {lg["hum"]} <b>{data['main']['humidity']}%</b>\n", hum_sos) +
                output(f"🧭 {lg["pres"]} <b>{data['main']['pressure']} {lg["hp"]}</b>\n", pres_sos) +
                output(f"💨 {lg["wind"]} <b>{wind_sp}</b> ({weather_speed})\n", wind_sos))
    bot.send_message(chat_id, vivod, parse_mode="HTML", reply_markup=markup)
    global idmessage
    idmessage = True
    logger.info(f"Пользователь %s (%s) получил погоду города {data['name']}, страны {data['sys']['country']}", mess.from_user.username, chat_id)

def output(text, status):
    return text if status else ""

#Функция для отправки погоды
def send_weather(chat_id, city):
    try:
       data = get_weather(city)
    except requests.RequestException:
        bot.send_message(chat_id, lg["err1"])
        waiting_city.add(chat_id)
    if data is None:
        bot.send_message(chat_id, lg["err2"])
        waiting_city.add(chat_id)
        return
    format_weather(chat_id, city, data)

#Запуска бота
bot.polling(non_stop=True)