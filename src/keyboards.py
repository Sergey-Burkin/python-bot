from aiogram import types
from constants import lists

# Create buttons first
buttons = []
for x in lists:
    buttons.append([types.InlineKeyboardButton(text=x[0], callback_data='list' + x[1])])

# Now create the markup with the buttons
inline_keyboard_menu = types.InlineKeyboardMarkup(inline_keyboard=buttons)
