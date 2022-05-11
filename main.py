import logging
import os
import glob

import aiogram.types
from icrawler.builtin import GoogleImageCrawler

from aiogram import Bot, Dispatcher, executor, types
from constants import TOKEN, api_key
from aioyoutube import Api

API_TOKEN = TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    button1 = types.KeyboardButton('/help')
    button2 = types.KeyboardButton('/youtube')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                         one_time_keyboard=True)
    keyboard.add(button1).add(button2)
    await message.reply('''
    Привет!
    Этот бот написан на aiogram.
    Нажимай /start или /help для вызова помощи
    /youtube запускает основную функцию бота
    
    P.S.
    Если станет грустно от бесконечных верениц непросмотренных лекций, просто напечатай имя какой-нибудь знаменитости (in English)
    ''', reply_markup=keyboard)



@dp.message_handler(commands=['answer'])
async def echo_answer(message: types.Message):
    await message.answer_poll('How many?', ['42', '0'], correct_option_id=0,
                              type='quiz', explanation='42')


async def get_playlist(playlist_id):
    api = Api()
    lists = await api.playlistItems(key=api_key, part=['snippet', 'id'],
                                    playlist_id=playlist_id
                                    )
    lists = lists['items']
    return lists


currentId = 'PL4_hYwCyhAvYePPocxGQv8RsOnYepxCPY'

# keyboards.py

lists = [['Матан', 'PL4_hYwCyhAvYePPocxGQv8RsOnYepxCPY'],
         ['Алгем', 'PL4_hYwCyhAvYmJi6xJFMsb1lpcZ5zZo93'],
         ['ОКТЧ', 'PL4_hYwCyhAvbGZOQrBtdahOGy4QydyTAB'],
         ['Матлог', 'PL4_hYwCyhAvYLl1VsA8JGQkrxg0Ll2D9J'],
         ['C++', 'PL4_hYwCyhAvaWsj3-0gLH_yEZfKdTife0'],
         ['Рухович', 'PL4_hYwCyhAvYljQ1BQj1wQayqn79LL-1k']]

buttons = [types.InlineKeyboardButton(x[0], callback_data='list' + x[1]) for x
           in lists]

inline_kb1 = types.InlineKeyboardMarkup()
for button in buttons:
    inline_kb1.add(button)


# bot.py
@dp.message_handler(commands=['youtube'])
async def process_command_1(message: types.Message):
    await message.answer("Выбери курс", reply_markup=inline_kb1)


@dp.callback_query_handler(
    run_task=lambda c: c.data and c.data.startswith('list'))
async def greatprint(callback_query: types.CallbackQuery):
    code = callback_query.data[4:]
    lists = await get_playlist(code)

    for video in lists:
        await bot.send_message(callback_query.from_user.id,
                               video['snippet']['title'])
        await bot.send_message(callback_query.from_user.id,
                               'www.youtube.com/watch?v=' +
                               video['snippet']['resourceId'][
                                   'videoId'])


@dp.message_handler()
async def echo(message: types.Message):
    n = 3
    button = aiogram.types.KeyboardButton('3')
    google_crawler = GoogleImageCrawler(storage={'root_dir': './data'})
    google_crawler.crawl(keyword=message.text + ' smiling', max_num=n)
    files = glob.glob('./data/0*')
    for f in files:
        with open(f, 'rb') as photo:
            await message.answer_photo(photo)
    files = glob.glob('./data/0*')
    for f in files:
        os.remove(f)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
