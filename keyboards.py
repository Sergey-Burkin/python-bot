from aiogram import types
from constants import lists

inline_keyboard_menu = types.InlineKeyboardMarkup()

for x in lists:
    inline_keyboard_menu.add(
        types.InlineKeyboardButton(x[0], callback_data='list' + x[1]))
