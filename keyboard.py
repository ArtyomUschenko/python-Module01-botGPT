from aiogram import types

def keyboard_start(start_keyboard=None):
    start_keyboard = types.InlineKeyboardMarkup(row_width=2) # row_width=2 - Дизайн клавиатуры
    start_button1 = types.InlineKeyboardButton(text ='О нас', callback_data='start_about')
    start_button2 = types.InlineKeyboardButton(text ='Помощь от ИИ', callback_data='start_II')
    start_button3 = types.InlineKeyboardButton(text='Задачи на сегодня', callback_data='start_today')
    start_button4 = types.InlineKeyboardButton(text='Сайт', url='https://platform-eadsc.voskhod.ru/')
    start_keyboard.add(start_button1, start_button2, start_button3, start_button4)
    return start_keyboard

keyboard_start = keyboard_start()