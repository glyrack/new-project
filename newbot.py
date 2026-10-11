import telebot
from telebot import types
import requests


#Ключи для бота и API погоды
api_key = '********************************************'
weather_key = '****************************************'


#Бот и переменные
bot = telebot.TeleBot(api_key)
waiting_city = set()
back_to = []
idmessage = False


#Функция для получения погоды
def get_weather(city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": weather_key, "units": "metric", "lang": "ru"}
    response = requests.get(url, params=params, timeout=10)
    if response.status_code == 404:
        return None
    if response.status_code == 400:
        return None
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
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("⬅️Back", callback_data="back"))
    bot.send_message(chat_id, f"Weather in <b>{city.title()}</b>:\n\n" +
                f"🌍 <b>{data['name']}, {data['sys']['country']}</b>\n"
                f"☁️ Погода: <b>{data['weather'][0]['description'].capitalize()}</b>\n"
                f"🌡 Температура: <b>{data['main']['temp']:.0f}°C</b>\n"
                f"🔎 Ощущается как: <b>{data['main']['feels_like']:.0f}°C</b>\n"
                f"💧 Влажность: <b>{data['main']['humidity']}%</b>\n"
                f"🧭 Давление: <b>{data['main']['pressure']} гПа</b>\n"
                f"💨 Ветер: <b>{data['wind']['speed']} м/с</b> ({weather_speed})\n", 
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
    markup = types.InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
    inf_button = types.InlineKeyboardButton("ℹ️ Info", callback_data="info")
    option = types.InlineKeyboardButton("⚙️ Options", callback_data="options")
    markup.add(option, inf_button)
    weaTher_button = types.InlineKeyboardButton("🌤 Weather in the city", callback_data="weather")
    markup.add(weaTher_button)
    bot.send_chat_action(message.chat.id, "typing")
    bot.send_message(message.chat.id, "Hello 👋, i'm a weather bot! 🤖\n\nSend me the <b>name of the city</b> and i will give you the current weather information.\n\nWrite the name of the city in English or Russian language.\n\nFor example: London, New York, Paris, etc.", parse_mode="HTML", reply_markup=markup)
    idmessage = False
    back_to.clear()


@bot.callback_query_handler(func=lambda call: call.data == "options")
def parametr(call):
    back_undo(call.data)
    markup = types.InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
    markup.add(types.InlineKeyboardButton("🌐 Change language", callback_data="change_language"))
    markup.add(types.InlineKeyboardButton("💨 wind speed", callback_data="wind"), types.InlineKeyboardButton("🌡️ degree", callback_data="degree"))
    markup.add(types.InlineKeyboardButton("⬅️Back", callback_data="back"))
    bot.edit_message_text("Configuration options:", call.message.chat.id, call.message.message_id, reply_markup=markup)
    
    
#Обработчик кнопки смены языка
@bot.callback_query_handler(func=lambda call: call.data == "change_language")
def change_language(call):
    global back_to
    back_to.append("change_language")
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("🇷🇺 Русский", callback_data="ru"), types.InlineKeyboardButton("🇬🇧 English", callback_data="en"))
    markup.add(types.InlineKeyboardButton("⬅️Back", callback_data="back"))
    bot.edit_message_text("Choose a language:", call.message.chat.id, call.message.message_id, reply_markup=markup)


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
            markup = types.InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
            inf_button = types.InlineKeyboardButton("ℹ️ Info", callback_data="info")
            option = types.InlineKeyboardButton("⚙️ Options", callback_data="options")
            markup.add(option, inf_button)
            weaTher_button = types.InlineKeyboardButton("🌤 Weather in the city", callback_data="weather")
            markup.add(weaTher_button)
            bot.edit_message_text("Hello 👋, i'm a weather bot! 🤖\n\nSend me the <b>name of the city</b> and i will give you the current weather information.\n\nWrite the name of the city in English or Russian language.\n\nFor example: London, New York, Paris, etc.", call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=markup)
            idmessage = False
    else:
        if back_to[-1] == "options":
            parametr(call)
            back_to.pop()
    waiting_city.discard(call.message.chat.id)
    print(list(back_to))

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
bot.polling(none_stop=True)