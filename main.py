import logging
import os
import glob

import aiogram.types
from icrawler.builtin import GoogleImageCrawler

from aiogram import Bot, Dispatcher, executor, types
from constants import TOKEN

API_TOKEN = TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm Bot!\nPowered by aiogram.")


@dp.message_handler(commands=['answer'])
async def echo_answer(message: types.Message):
    await message.answer_poll('How many?', ['42', '0'], correct_option_id=0,
                              type='quiz', explanation='42')


@dp.message_handler(commands=['test'])
async def handle_command_adminwindow(message: types.Message):
    button1 = types.KeyboardButton('/test')
    button2 = types.KeyboardButton('/start')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                         one_time_keyboard=True)
    keyboard.add(button1).add(button2).add(button1).add('d')
    await message.answer("hi", reply_markup=keyboard)


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
