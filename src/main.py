import logging
import os
import glob

from icrawler.builtin import GoogleImageCrawler
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.types import FSInputFile
import asyncio
from aioyoutube import Api
from constants import TOKEN as API_TOKEN, api_key, number_photos
from keyboards import inline_keyboard_menu

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.message(Command(commands=["start", "help"]))
async def send_welcome(message: types.Message):
    button1 = types.KeyboardButton(text='/help')
    button2 = types.KeyboardButton(text='/youtube')
    keyboard = types.ReplyKeyboardMarkup(keyboard=[[button1], [button2]], resize_keyboard=True, one_time_keyboard=True)
    await message.reply('''
    Привет!
    Этот бот написан на aiogram.
    Нажимай /start или /help для вызова помощи
    /youtube запускает основную функцию бота
    
    P.S.
    Если станет грустно от бесконечных верениц непросмотренных лекций, просто напечатай имя какой-нибудь знаменитости (in English)
    ''', reply_markup=keyboard)


@dp.message(Command(commands=["answer"]))
async def echo_answer(message: types.Message):
    await message.answer_poll('How many?', ['42', '0'], correct_option_id=0,
                              type='quiz', explanation='42')


async def get_playlist(playlist_id):
    try:
        api = Api()
        playlist = await api.playlistItems(key=api_key, part=['snippet', 'id'],
                                        playlist_id=playlist_id
                                        )
        if playlist and 'items' in playlist:
            return playlist['items']
        else:
            logging.warning(f"Empty playlist or missing 'items' key: {playlist}")
            return []
    except Exception as e:
        logging.error(f"Error fetching playlist {playlist_id}: {e}")
        return []


@dp.message(Command(commands=["youtube"]))
async def process_command_1(message: types.Message):
    await message.answer("Выбери курс", reply_markup=inline_keyboard_menu)


@dp.callback_query(F.data.startswith('list'))
async def great_print(callback_query: types.CallbackQuery):
    await callback_query.answer()  # Отвечаем на callback query чтобы убрать часы загрузки
    code = callback_query.data[4:]
    current_playlist = await get_playlist(code)
    
    if not current_playlist:
        await bot.send_message(callback_query.from_user.id, 
                               "Не удалось получить плейлист. Возможно, YouTube API ключ не настроен.")
        return
    
    for video in current_playlist:
        try:
            title = video['snippet']['title']
            video_id = video['snippet']['resourceId']['videoId']
            await bot.send_message(callback_query.from_user.id, title)
            await bot.send_message(callback_query.from_user.id, 
                                  f'www.youtube.com/watch?v={video_id}')
        except KeyError as e:
            logging.error(f"Missing key in video data: {e}")


@dp.message()
async def echo(message: types.Message):
    google_crawler = GoogleImageCrawler(storage={'root_dir': './data'})
    google_crawler.crawl(keyword=message.text + ' smiling',
                         max_num=number_photos)
    files = glob.glob('./data/0*')
    for f in files:
        try:
            # Используем FSInputFile для отправки файлов в aiogram v3
            photo = FSInputFile(f)
            await message.answer_photo(photo)
        except Exception as e:
            logging.error(f"Error sending photo: {e}")
    files = glob.glob('./data/0*')
    for f in files:
        os.remove(f)

async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())