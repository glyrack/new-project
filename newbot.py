import telebot
import requests

api_key = '8539189640:AAHH7F8jGhiuoshr62dX6qNnZYYTjl8KJpw'
weather_key = '1b7bc2a2896f2b23bf8f95065f852812'

bot = telebot.TeleBot(api_key)

def weather(chat_id, city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": weather_key, "units": "metric", "lang": "ru"}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    if response.status_code == 200:
        data = response.json()
        bot.send_message(chat_id, f"You live in <em><b>{city}</b></em> and the weather is: \n", parse_mode="HTML")
        return (
            ("Город:        ", f"{data['name']}"),
            ("Погода:       ", f"{data['weather'][0]['description']}"),
            ("Температура:  ", f"{data['main']['temp']}°C"),
            ("Ощущается как:", f"{data['main']['feels_like']}°C"),
            ("Влажность:    ", f"{data['main']['humidity']}%"),
            ("Ветер:        ", f"{data['wind']['speed']} м/с"))
    elif response.status_code == 404:
        bot.send_message(chat_id, "City not found!")
        return
    elif response.status_code == 401:
        bot.send_message(chat_id, "Invalid API key!")
        return
    else: 
        bot.send_message(chat_id, "Error", response.status_code)
        
@bot.message_handler(commands=['start', 'hello', 'привет'])
def main(message):
    bot.send_chat_action(message.chat.id, "typing")
    bot.send_message(message.chat.id, "Hello, i'm a weather bot!\nSend me the <b>name of the city</b> and i will give you the current weather information.\nWrite the name of the city in English.\nFor example: London, New York, Paris, etc.", parse_mode="HTML")

@bot.message_handler()
def info(message):
    city = message.text
    bot.send_chat_action(message.chat.id, "typing")
    for label, value in weather(message.chat.id, city):
        bot.send_message(message.chat.id, f"{label} {value}")

bot.polling(non_stop=True)