import sqlite3 # Библиотека для работы с базами данных SQLite
import datetime # Библиотека для работы с датами
import string # Библиотека для работы со строками
import asyncio # Библиотека "асинхронности"
from aiogram import Bot, Dispatcher, executor, types # Библиотека для работы с телеграм API
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder # Импортируем объекты создания обычных и inline клавиатур

from handlers import common, schedule, menu, jokes, calc   # импортируем модули с хэндлерами
from config_reader import config # импортируем конфиг с токеном бота
from keyboards import reply_kb, inline_kb #импортируем модули с клавиатурами


TOKEN = config.bot_token.get_secret_value() # Определяем токен бота из файла конфига
DB_PATH = "../../Database/school.db" # Определяем путь к файлу с базой данных


bot = Bot(token=TOKEN) # Создаем объект бота
dp = Dispatcher(bot) # Создаем объект диспетчера
dp.include_routers(common.router, schedule.router, menu.router, jokes.router, calc.router) # Подключаем роутеры хендлеров по убыванию значимости

def main():
    executor.start_polling(dp, skip_updates=True) # Запускаем бота

if __name__ == "__main__":
    asyncio.run(main())
