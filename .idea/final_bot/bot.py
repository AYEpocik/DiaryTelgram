import sqlite3 # Библиотека для работы с базами данных SQLite
import datetime # Библиотека для работы с датами
import string # Библиотека для работы со строками
import asyncio # Библиотека "асинхронности"

from aiogram import Bot, Dispatcher, types, F # Импортируем объекты бота, диспетчера, типы и магический фильтр
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder # Импортируем объекты создания обычных и inline клавиатур

from handlers import common, schedule, menu, jokes, calc # Импортируем модули с хэндлерами
from keyboards.reply_kb import main_menu_keyboard, breakfast_or_lunch # Импортируем обычные клавиатуры
from data.constants import TOKEN, DB_PATH # Импортируем токен бота и путь к базе данных


bot = Bot(token=TOKEN) # Создаем объект бота
dp = Dispatcher() # Создаем объект диспетчера
dp.include_routers(common.router, schedule.router, menu.router, jokes.router, calc.router) # Подключаем роутеры хендлеров по убыванию значимости

async def main():
    await bot.delete_webhook(drop_pending_updates=True) # Пропускаем все накопленные входящие
    print('Бот запущен!')
    await dp.start_polling(bot) # Запускаем бота


if __name__ == "__main__":
    asyncio.run(main())
