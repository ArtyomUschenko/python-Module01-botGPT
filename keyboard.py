from aiogram import types

def keyboard_start(start_keyboard=None):
    start_keyboard = types.InlineKeyboardMarkup(row_width=1) # row_width=2 - Дизайн клавиатуры
    start_button1 = types.InlineKeyboardButton(text ='О нас', callback_data='start_about')
    start_button2 = types.InlineKeyboardButton(text ='Помощь от ИИ', callback_data='start_II')
    start_button3 = types.InlineKeyboardButton(text='Задачи на сегодня', callback_data='start_today')
    start_button4 = types.InlineKeyboardButton(text='Сайт', url='https://platform-eadsc.voskhod.ru/')
    start_button5 = types.InlineKeyboardButton(text='Отметиться', callback_data='start_inwork')
    start_button6 = types.InlineKeyboardButton(text='Внести пожелания по работе', callback_data='start_sendsome')
    start_button7 = types.InlineKeyboardButton(text='Отправить отчет', callback_data='start_document')
    start_keyboard.add(start_button1, start_button2, start_button3, start_button4, start_button5, start_button6, start_button7)
    return start_keyboard

def keyboard_inwork():
    inwork_keyboard = types.InlineKeyboardMarkup(row_width=2)
    inwork_button1 = types.InlineKeyboardButton(text='Пришел', callback_data='inwork_in')
    inwork_button2 = types.InlineKeyboardButton(text='Ушел', callback_data='inwork_out')
    inwork_keyboard.add(inwork_button1, inwork_button2)
    return inwork_keyboard

def keyboard_admin():
    admin_start = types.InlineKeyboardMarkup(row_width=1)
    admin_button1 = types.InlineKeyboardButton(text='внести информацию', callback_data='admin_insertTask')
    admin_button2 = types.InlineKeyboardButton(text='Отправить сообщения всем', callback_data='admin_allmess')
    admin_button3 = types.InlineKeyboardButton(text='Отправить сообщения выбранному', callback_data='admin_onemess')
    admin_button4 = types.InlineKeyboardButton(text='Отправить пожелания', callback_data='admin_look')
    admin_button5 = types.InlineKeyboardButton(text='Просмотреть отчет', callback_data='admin_checkdoc')
    admin_start.add(admin_button1, admin_button2, admin_button3, admin_button4, admin_button5)
    return admin_start


keyboard_start = keyboard_start()
keyboard_inwork = keyboard_inwork()
keyboard_admin = keyboard_admin()