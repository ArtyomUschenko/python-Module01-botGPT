import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

import sqlite3 as sq

from keyboard import keyboard_start

# Объект бота
bot = Bot(token='7301540230:AAEWyxaVCNqSZ0mqg5oxpbeMEiFGVBQJUdA')
# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

async def on_startup(_):
    global cur, base   # Объявляем глобальные переменные
    base = sq.connect('main.db') # Подключаемся к базе данных
    cur = base.cursor()
    if base:
        print('Connected to database')
    base.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER, Datatime REAL, Callback INTEGER, Link TEXT, PRIMARY KEY("ID" AUTOINCREMENT))')
    base.commit()

# Хэндлер на команду /start
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, f"Добрый день, {message.from_user.first_name}!\n\n Я - твой личный помощник по ГИС \"ЦХЭД\" ", reply_markup=keyboard_start )
    # print(message)
    # await bot.send_message(message.from_user.id, f"Привет {message.from_user.username}")
    # # pass

async def start_keyboard(callback: types.CallbackQuery):
    await bot.answer_callback_query(callback.id)
    print(callback)
    str = callback.data.split("_")[1]
    print(str)
    if str == 'II':
        pass
    if str == 'today':
        link = cur.execute(f"SELECT Link FROM users WHERE Callback = '{callback.from_user.id}'").fetchone()
        base.commit()
        await bot.send_message(callback.from_user.id, f"Ссылка на твою страницу: {link}")


if __name__ == '__main__':
    dp.register_message_handler(start, commands=['start'])
    dp.register_callback_query_handler(start_keyboard, Text(startswith ='start_'))
    # Запуск бота
    executor.start_polling(dp,skip_updates=True, on_startup=on_startup)
