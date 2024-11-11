import logging
import datetime

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage


import sqlite3 as sq

from keyboard import keyboard_start, keyboard_inwork, keyboard_admin
from states_groups import AdminInserTask


# Объект бота
storage = MemoryStorage()
bot = Bot(token='7301540230:AAEWyxaVCNqSZ0mqg5oxpbeMEiFGVBQJUdA')
# Диспетчер для бота
dp = Dispatcher(bot, storage=storage) # Диспетчер
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

    base.execute('CREATE TABLE IF NOT EXISTS inwork (id INTEGER, Datatime REAL, Callback INTEGER, Link TEXT, Hour INTEGER, Minute INTEGER, PRIMARY KEY("ID" AUTOINCREMENT))')
    base.commit()

    base.execute(
        'CREATE TABLE IF NOT EXISTS outwork (id INTEGER, Datatime REAL, Callback INTEGER, Link TEXT, Hour INTEGER, Minute INTEGER, PRIMARY KEY("ID" AUTOINCREMENT))')
    base.commit()

    base.execute(
        'CREATE TABLE IF NOT EXISTS tasks (id INTEGER, Datatime REAL, Name TEXT, Describe TEXT, Img TEXT, PRIMARY KEY("ID" AUTOINCREMENT))')
    base.commit()



    date = datetime.datetime.now()
    hour = date.hour
    minute = date.minute
    print(hour, minute)


async def inser_task(state):
    async with state.proxy() as data: # Передаем данные в функцию
        cur.execute(f"INSERT INTO tasks (Datatime, Name, Describe, Img) VALUES (?,?,?,?)", tuple(data.values()))
    base.commit()

# Хэндлер на команду /start
async def start(message: types.Message, state: FSMContext):
    user = cur.execute(f'SELECT Callback FROM users WHERE Callback == ?', (message.chat.id,)).fetchone()
    if user == None:
        dates = datetime.datetime.today()
        sql_insert ="""INSERT INTO users (Datatime,Callback, Link) VALUES (?,?,?)"""
        data_insert = (dates, message.chat.id, message.from_user.username)
        cur.execute(sql_insert, data_insert)
        base.commit()

    await bot.send_message(message.from_user.id,
                               f"Добрый день, {message.from_user.first_name}!\n\n Я - твой личный помощник по ГИС \"ЦХЭД\" ",
                               reply_markup=keyboard_start)

async def start_keyboard(callback: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback.id)
    print(callback)
    str = callback.data.split("_")[1]
    print(str)
    if str == 'II':
        pass
    if str == 'today':
        link = cur.execute(f"SELECT Link FROM users WHERE Callback = ?", (callback.from_user.id,)).fetchone()
        base.commit()
        await bot.send_message(callback.from_user.id, f"Ссылка на твою страницу: {link}")
    if str == 'inwork':
        await bot.send_message(callback.from_user.id, f"Выберете:", reply_markup=keyboard_inwork)

async def inwork_function(callback: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback.id)
    str = callback.data.split("_")[1]
    if str == "in":
        dates = datetime.datetime.today()
        date = datetime.datetime.now()
        hour = date.hour
        minute = date.minute
        sql_insert = """INSERT INTO inwork (Datatime,Callback, Link, Hour, Minute) VALUES (?,?,?,?,?)"""
        data_insert = (dates, callback.from_user.id, callback.from_user.username, hour, minute)
        cur.execute(sql_insert, data_insert)
        base.commit()
        await bot.send_message(callback.from_user.id, f"Вы на работе", reply_markup=keyboard_start)
    if str == "out":
        dates = datetime.datetime.today()
        date = datetime.datetime.now()
        hour = date.hour
        minute = date.minute
        sql_insert = """INSERT INTO outwork (Datatime,Callback, Link, Hour, Minute) VALUES (?,?,?,?,?)"""
        data_insert = (dates, callback.from_user.id, callback.from_user.username, hour, minute)
        cur.execute(sql_insert, data_insert)
        base.commit()
        await bot.send_message(callback.from_user.id, f"До Скорых встреч", reply_markup=keyboard_start)


async def admin(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, f"Ты в админке!\n\nВыбирай функцию", reply_markup=keyboard_admin)

async def admin_choose_option(callback: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback.id)
    str = callback.data.split("_")[1]
    if str == "insertTask":
        await bot.send_message(callback.from_user.id, f"Внесите наименование задачи:")
        await AdminInserTask.name.set()


async def admin_nameTask_insert(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['datatime'] = datetime.datetime.today()
        data['name'] = message.text
    await bot.send_message(message.chat.id, f"Введите описание задачи")
    await AdminInserTask.describe.set()

async def admin_describeTask_insert(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['describe'] = message.text
    await bot.send_message(message.chat.id, f"Прикрепите картинку")
    await AdminInserTask.img.set()

async def admin_imgTask_insert(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['img'] = message.photo[0].file_id
    await inser_task(state)
    await state.finish()
    await bot.send_message(message.chat.id, f"Задача добавлена", reply_markup=keyboard_admin)


if __name__ == '__main__':
    dp.register_message_handler(start, commands=['start'], state = None)
    dp.register_message_handler(admin, commands=['admin'], state = None) # В дальнейшем необходимо изменить команду админа на более сложную
    dp.register_message_handler(admin_nameTask_insert, content_types= "text", state = AdminInserTask.name)
    dp.register_message_handler(admin_describeTask_insert, content_types= "text", state=AdminInserTask.describe)
    dp.register_message_handler(admin_imgTask_insert, content_types= "photo", state=AdminInserTask.img)


    dp.register_callback_query_handler(start_keyboard, Text(startswith ='start_'), state = None)
    dp.register_callback_query_handler(inwork_function, Text(startswith='inwork_'), state = None)
    dp.register_callback_query_handler(admin_choose_option, Text(startswith='admin_'), state= None)

    # Запуск бота
    executor.start_polling(dp,skip_updates=True, on_startup=on_startup)
