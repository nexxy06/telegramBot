import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from bs4 import BeautifulSoup
from translate import Translator

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    privet = open('кот.jpg', 'rb')
    await bot.send_photo(chat_id=message.chat.id, photo=privet)
    await message.reply("Привет!\nЯ самый крутой бот на свете!\nнапиши команду /help, чтобы узнать мои возмоности")


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    sos = open('помощь.jpg', 'rb')
    await bot.send_photo(chat_id=message.chat.id, photo=sos)
    await message.reply(
        'Это может почти всё!\n1 команда:/start - ты начнешь сначала\n2 команда /weather - ты сможешь узанть про погду в любои городе\n'
        '3 команда /news - ты можешь узнать про самые посление новости в мире')


@dp.message_handler(commands=["news"])
async def get_news(message: types.Message):
    URL = "https://quote.rbc.ru/?target_type=posts&q=python&order_by=date"

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    post = soup.find("a", class_="q-item__link")

    title = post.find("span", class_="q-item__title").text.strip()
    description = post.find("span", class_="q-item__description").text.strip()
    rt = soup.find("a", class_="q-item__link", href=True)["href"].strip()

    await message.reply(title)
    await message.reply(description)
    await message.reply(rt)


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


@dp.message_handler(content_types=types.ContentTypes.TEXT, commands=["translator"])
async def echo_message(message: types.Message):
    await message.reply("Введите слово")

    @dp.message_handler(content_types=types.ContentTypes.TEXT)
    async def answer_to_messages_1(word: types.Message):
        translator = Translator(from_lang='ru', to_lang='en')
        perevod_1 = translator.translate(word)
        print(perevod_1)
        await message.reply(perevod_1)


@dp.message_handler(commands=["music"])
async def echo_message(message: types.Message):
    await message.reply("https://music.yandex.ru/home\nhttps://vk.com/vkmusic")


@dp.message_handler(commands=['curs'])
async def kurs(message: types.Message):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    DOLLAR_RUB = 'https://www.google.com/search?sxsrf=ALeKk01NWm6viYijAo3HXYOEQUyDEDtFEw%3A1584716087546&source=hp&ei=N9l0XtDXHs716QTcuaXoAg&q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+&gs_l=psy-ab.3.0.35i39i70i258j0i131l4j0j0i131l4.3044.4178..5294...1.0..0.83.544.7......0....1..gws-wiz.......35i39.5QL6Ev1Kfk4'
    EURO = 'https://www.google.com/search?q=евро+к+рублю&sxsrf=ALiCzsahlwOCAnwVjMKdcEFlfaO7cczsBw%3A1651144380273&ei=vHZqYpukEIaCi-gPiZmC0A8&ved=0ahUKEwib8oiS0Lb3AhUGwQIHHYmMAPoQ4dUDCA4&uact=5&oq=евро+к+рублю&gs_lcp=Cgdnd3Mtd2l6EAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAEEcQsAMyBwgAELADEEMyBwgAELADEENKBAhBGABKBAhGGABQAFgAYMMEaAFwAXgAgAEAiAEAkgEAmAEAyAEKwAEB&sclient=gws-wiz'
    page_d = requests.get(DOLLAR_RUB, headers=headers)
    page_e = requests.get(EURO, headers=headers)
    # Разбираем через BeautifulSoup
    soup_d = BeautifulSoup(page_d.content, 'html.parser')
    soup_e = BeautifulSoup(page_e.content, 'html.parser')

    # Получаем нужное для нас значение и возвращаем его
    convert_d = soup_d.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
    convert_e = soup_e.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
    await message.reply(convert_e, convert_d)


if __name__ == '__main__':
    executor.start_polling(dp)
