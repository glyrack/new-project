import telebot
from telebot import types
import requests


#Ключи для бота и API погоды
api_key = '8860077362:AAE8jZT2dNKR8aLDNuVxaUNWqeffn-XSMUw'
weather_key = '1b7bc2a2896f2b23bf8f95065f852812'


#Бот и переменные
bot = telebot.TeleBot(api_key)
waiting_city = set()
back_to = []
idmessage = False
speed = True
degre = None
lang = True


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
            weather_speed = "Штиль"
    elif data['wind']['speed'] >= 0.3 and data['wind']['speed'] <= 7.9:
            weather_speed = "Ветер слабый"
    elif data['wind']['speed'] >= 8 and data['wind']['speed'] <= 20.7:
            weather_speed = "Сильный ветер"
    else:
            weather_speed = "Шторм"
    if speed == True:
        wind_sp = f"{data['wind']['speed']} м/с"
    elif speed == False:
        form = (data['wind']['speed']) * 3.6 
        wind_sp = f"{form} км/ч"
        
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("⬅️Back", callback_data="back"))
    if lang == True:
        we = "Weather in"
        w = "Weather:"
        t = "Temperature:"
        f = "Feels like:"
        h = "Humidity:"
        p = "Pressure:"
        wi = "Wind:"
    else:
        we = "Погода в"
        w = "Погода:"
        t = "Температура:"
        f = "Ощущается как:"
        h = "Влажность:"
        p = "Давление:"
        wi = "Ветер:"
    bot.send_message(chat_id, f"{we} <b>{city.title()}</b>:\n\n" +
                f"🌍 <b>{data['name']}, {data['sys']['country']}</b>\n"
                f"☁️ {w} <b>{data['weather'][0]['description'].capitalize()}</b>\n"
                f"🌡 {t} <b>{data['main']['temp']:.0f}°C</b>\n"
                f"🔎 {f} <b>{data['main']['feels_like']:.0f}°C</b>\n"
                f"💧 {h} <b>{data['main']['humidity']}%</b>\n"
                f"🧭 {p} <b>{data['main']['pressure']} гПа</b>\n"
                f"💨 {wi} <b>{wind_sp}</b> ({weather_speed})\n", 
                parse_mode="HTML", reply_markup=markup)
    global idmessage
    idmessage = True


#Функция для отправки погоды
def send_weather(chat_id, city):
    try:
       data = get_weather(city)
    except requests.RequestException:
        bot.send_message(chat_id, "Error, please try again later.")
        waiting_city.add(chat_id)
    if data is None:
        bot.send_message(chat_id, "City not found!")
        waiting_city.add(chat_id)
        return
    bot.send_message(chat_id, format_weather(chat_id, city, data), parse_mode="HTML")


#Обработчик стартовых команд
@bot.message_handler(commands=['start', 'hello', 'привет'])
def main(message):
    global idmessage, back_to
    if lang == True: 
        l = "Hello 👋, i'm a weather bot! 🤖\n\nSend me the <b>name of the city</b> and i will give you the current weather information.\n\nWrite the name of the city in English or Russian language.\n\nFor example: London, New York, Paris, etc."
        i = "ℹ️ Info"
        o = "⚙️ Options"
        w = "🌤 Weather in the city"
    else: 
        l = "Привет 👋, я — погодный бот! 🤖\n\nПришли мне <b>название города</b>, и я сообщу тебе актуальную информацию о погоде.\n\nНазвание города можно написать на английском или русском языке.\n\nНапример: Лондон, Нью-Йорк, Париж и т. д."
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
    print(list(back_to))


@bot.callback_query_handler(func=lambda call: call.data == "options")
def parametr(call):
    back_undo("options")
    if lang == True: 
        c = "🌐 Change language"
        w = "💨 wind speed"
        d = "🌡️ degrees"
        b = "⬅️Back"
        op = "Configuration options:"
    else: 
        c = "🌐 Изменить язык"
        w = "💨 скорость ветра"
        d = "🌡️ градусы"
        b = "⬅️Назад"
        op = "Конфигурации настроек:"
    markup = types.InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
    markup.add(types.InlineKeyboardButton(c, callback_data="change_language"))
    markup.add(types.InlineKeyboardButton(w, callback_data="wind"), types.InlineKeyboardButton(d, callback_data="degree"))
    markup.add(types.InlineKeyboardButton(b, callback_data="back"))
    bot.edit_message_text(op, call.message.chat.id, call.message.message_id, reply_markup=markup)
    print(list(back_to))
    
    
@bot.callback_query_handler(func=lambda call: call.data == "wind")
def wind_speed(call):
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
    print(list(back_to))    
    
@bot.callback_query_handler(func=lambda call: call.data == "metr")
def metres(call):
    global speed
    speed = True
    back_to_menu(call)
    if lang == True: 
        m = "Wind speed will be displayed in meters per second."
    else: 
        m = "Скорость ветра будет отображаться в метрах в секунду."
    bot.send_message(call.message.chat.id, m, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data == "kilometr")
def kilo(call):
    global speed
    speed = False
    back_to_menu(call)
    if lang == True: 
        k = "Wind speed will be displayed in kilometers per hour."
    else: 
        k = "Скорость ветра будет отображаться в километрах в час."
    bot.send_message(call.message.chat.id, k, parse_mode="HTML")
    
    
@bot.callback_query_handler(func=lambda call: call.data == "degree")
def degree(call):
    global back_to
    back_to.append("degree")
    if lang == True:
        b = "⬅️Назад"
        s = "Show concept degree:"
    else:
        b = "⬅️Back"
        s = "Отображение температуры:"
    markup = types.InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
    markup.add(types.InlineKeyboardButton("°C", callback_data="calls"))
    markup.add(types.InlineKeyboardButton("°F", callback_data="fareng"))
    markup.add(types.InlineKeyboardButton(b, callback_data="back"))
    bot.edit_message_text(s, call.message.chat.id, call.message.message_id, reply_markup=markup)
    print(list(back_to))
    
    
#Обработчик кнопки смены языка
@bot.callback_query_handler(func=lambda call: call.data == "change_language")
def change_language(call):
    global back_to
    back_to.append("change_language")
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("🇷🇺 Русский", callback_data="ru"), types.InlineKeyboardButton("🇬🇧 English", callback_data="en"))
    markup.add(types.InlineKeyboardButton("⬅️Back", callback_data="back"))
    bot.edit_message_text("Choose a language:", call.message.chat.id, call.message.message_id, reply_markup=markup)
    print(list(back_to))

@bot.callback_query_handler(func=lambda call: call.data == "ru")
def russian(call):
    global lang
    lang = False
    main(call.message)
    bot.send_message(call.message.chat.id, "Выбран <b>Русский</b> язык.", parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data == "en")
def russian(call):
    global lang
    lang = True
    main(call.message)
    bot.send_message(call.message.chat.id, "<b>English</b> language selected", parse_mode="HTML")

#Обработчик кнопки возврата в главное меню
@bot.callback_query_handler(func=lambda call: call.data == "back")
def back_to_menu(call):
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
                l = "Привет 👋, я — погодный бот! 🤖\n\nПришли мне <b>название города</b>, и я сообщу тебе актуальную информацию о погоде.\n\nНазвание города можно написать на английском или русском языке.\n\nНапример: Лондон, Нью-Йорк, Париж и т. д."
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


#Обработчик кнопки информации о боте
@bot.callback_query_handler(func=lambda call: call.data == "info")
def info_bot(call):
    back_undo(call.data)
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("⬅️Back", callback_data="back"))
    bot.edit_message_text("This bot was created by @FLLNKNG.\n\nIt provides weather information for cities around the world.\n\nYou can send the name of the city in English and get the current weather data.\n\nFor example: London, New York, Paris, etc.", call.message.chat.id, call.message.message_id,  parse_mode="HTML", reply_markup=markup)


""" ------ Комманды на получение погоды и проверку кнопки на активность ------ """
#Обработчик кнопки получения погоды
@bot.callback_query_handler(func=lambda call: call.data == "weather")
def weather_info(call):
    back_undo(call.data)
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("⬅️Back", callback_data="back"))
    bot.edit_message_text("Please send me the name of the city in English to get the current weather information:", call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=markup)
    waiting_city.add(call.message.chat.id)

#Обработчик получения города от пользователя
@bot.message_handler(func=lambda m: m.chat.id in waiting_city)
def info(message):
    waiting_city.discard(message.chat.id)
    bot.send_chat_action(message.chat.id, "typing")
    bot.send_message(message.chat.id, send_weather(message.chat.id, message.text), parse_mode="HTML")

#Обработчик, нажата ли кнопка погоды, прежде, чем осуществлять ввод
@bot.message_handler(func=lambda m: m.chat.id not in waiting_city)
def notinfo(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("🌤 Weather in the city", callback_data="weather"))
    bot.send_message(message.chat.id, "Please click the <b>button</b> to get weather information.", parse_mode="HTML", reply_markup=markup)


#Запуска бота
bot.polling(non_stop=True)