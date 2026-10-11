import telebot
from telebot import types
import requests


#Ключи для бота и API погоды
api_key = ''
weather_key = ''


#Бот и переменные
bot = telebot.TeleBot(api_key)
waiting_city = set()
error_count = False


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
    if int(data['wind']['speed']) >= 0 and int(data['wind']['speed']) <= 0.2:
            weather_speed = "Штиль"
    elif int(data['wind']['speed']) >= 0.3 and int(data['wind']['speed']) <= 7.9:
            weather_speed = "Ветер слабый"
    elif int(data['wind']['speed']) >= 8 and int(data['wind']['speed']) <= 20.7:
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


#Функция для отправки погоды
def send_weather(chat_id, city):
    try:
       data = get_weather(city)
    except requests.RequestException:
        bot.send_message(chat_id, "Error, please try again later.")
    if data is None:
        bot.send_message(chat_id, "City not found!")
        return
    bot.send_message(chat_id, format_weather(chat_id, city, data), parse_mode="HTML")

    
#Обработчик стартовых команд
@bot.message_handler(commands=['start', 'hello', 'привет'])
def main(message):
    markup = types.InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)
    inf_button = types.InlineKeyboardButton("ℹ️ Info", callback_data="info")
    lang_button = types.InlineKeyboardButton("🌐 Change language", callback_data="change_language")
    markup.add(lang_button, inf_button)
    weaTher_button = types.InlineKeyboardButton("🌤 Weather in the city", callback_data="weather")
    markup.add(weaTher_button)
    bot.send_chat_action(message.chat.id, "typing")
    bot.send_message(message.chat.id, "Hello, i'm a weather bot!\n\nSend me the <b>name of the city</b> and i will give you the current weather information.\n\nWrite the name of the city in English.\n\nFor example: London, New York, Paris, etc.", parse_mode="HTML", reply_markup=markup)
 
    
#Обработчик кнопки смены языка
@bot.callback_query_handler(func=lambda call: call.data == "change_language")
def change_language(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("🇷🇺 Русский", callback_data="ru"), types.InlineKeyboardButton("🇬🇧 English", callback_data="en"))
    markup.add(types.InlineKeyboardButton("⬅️Back", callback_data="back"))
    bot.send_message(call.message.chat.id, "Choose a language:", reply_markup=markup)


#Обработчик кнопки возврата в главное меню
@bot.callback_query_handler(func=lambda call: call.data == "back")
def back_to_menu(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    main(call.message)

    
#Обработчик кнопки информации о боте
@bot.callback_query_handler(func=lambda call: call.data == "info")
def info_bot(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("⬅️Back", callback_data="back"))
    bot.send_message(call.message.chat.id, "This bot was created by @FLLNKNG.\n\nIt provides weather information for cities around the world.\n\nYou can send the name of the city in English and get the current weather data.\n\nFor example: London, New York, Paris, etc.", parse_mode="HTML", reply_markup=markup)


""" ------ Комманды на получение погоды и проверку кнопки на активность ------ """
#Обработчик кнопки получения погоды
@bot.callback_query_handler(func=lambda call: call.data == "weather")
def weather_info(call):
    waiting_city.add(call.message.chat.id)
    bot.send_message(call.message.chat.id, "Please send me the name of the city in English to get the current weather information:", parse_mode="HTML")

#Обработчик получения города от пользователя
@bot.message_handler(func=lambda m: m.chat.id in waiting_city)
def info(message):
    waiting_city.discard(message.chat.id)
    bot.send_chat_action(message.chat.id, "typing")
    bot.send_message(message.chat.id, send_weather(message.chat.id, message.text), parse_mode="HTML")

#Обработчик, нажата ли кнопка погоды, прежде, чем осуществлять ввод
@bot.message_handler(func=lambda m: m.chat.id not in waiting_city)
def notinfo(message):
    bot.send_message(message.chat.id, "Please click the <b>button</b> to get weather information.", parse_mode="HTML")


#Запуска бота
bot.polling(non_stop=True)
