import requests
import datetime
from config import  tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    user = message.from_user
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_start = KeyboardButton('/start')
    markup.add(btn_start)
    await message.reply("Приветствую в WeatherBot! 🌦️\nПросто укажите свой город, и я предоставлю вам текущий прогноз погоды!",
                        reply_markup=markup)

@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    code_temperature = "\U00002103"
    code_wind = "\U0001F32C"
    code_sunrise = "\U0001F305"
    code_sunset = "\U0001F304"

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data['name']

        weather_main = data['weather'][0]['main']

        if weather_main in code_to_smile:
            wd = code_to_smile[weather_main]
        else:
            wd = 'Посмотри в окно, не пойму какая сейчас погода!'

        cur_weather = data['main']['temp']
        feels_like_temp = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        length_of_the_day = datetime.datetime.fromtimestamp(data['sys']['sunset']) - datetime.datetime.fromtimestamp(data['sys']['sunrise'])

        await message.reply(
            f'▶{datetime.datetime.now().strftime("%Y-%m-%d, %H:%M")}◀\n'
            f'Погода в городе {city}:\n• Описание: {wd}\n• Температура: {round(cur_weather)} {code_temperature}\n• Ощущается как {round(feels_like_temp)} {code_temperature}\n'
            f'• Влажность: {humidity}% \U0001F4A7\n• Скорость ветра: {round(wind_speed)} м/c {code_wind}\n'
            f'• Восход солнца: {sunrise_timestamp.strftime("%H:%M:%S")} {code_sunrise}\n• Закат солнца: {sunset_timestamp.strftime("%H:%M:%S")} {code_sunset}\n'
            f'• Продолжительность дня: {length_of_the_day}\n'
            f'☀️ Всего доброго! ☀️'
        )

    except:
        await message.reply('\U00002716 Проверьте название города \U00002716')

if __name__ == '__main__':
    executor.start_polling(dp)