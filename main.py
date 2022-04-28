import datetime

import requests
from aiogram import types

from weather_telegram_bot import dp


@dp.message_handler(content_types=types.ContentTypes.TEXT, commands=['weather'])
async def answer_to_messages(message: types.Message):
    await message.reply("Введите город")

    @dp.message_handler()
    async def answer_to_messages_1(town: types.Message):

        try:
            r = requests.get(
                f"http://api.openweathermap.org/data/2.5/weather?q={town.text}&appid={open_weather_token}&units=metric"
            )
            data = r.json()
            city = data["name"]
            cur_weather = data["main"]["temp"]

            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            wind = data["wind"]["speed"]
            max_temperature = data['main']['temp_max']
            min_temperature = data['main']['temp_min']

            await message.reply((f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                                 f"Погода в городе: {city}\nТемпература: {cur_weather} C°\n"
                                 f"Максимальная температра достигнет {max_temperature} C°\n"
                                 f"Минимальная температура достинет {min_temperature} C°\n"
                                 f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                                 f"Хорошего дня!"
                                 ))

        except:
            await message.reply("Такой города существует???")
