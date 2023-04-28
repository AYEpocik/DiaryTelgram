import sqlite3 # Библиотека для работы с базами данных SQLite
import datetime # Библиотека для работы с датами
import string # Библиотека для работы со строками
import asyncio # Библиотека "асинхронности"

from aiogram import Bot, Dispatcher # Импортируем объекты бота, диспетчера
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder # Импортируем объекты создания обычных и inline клавиатур

from handlers import common, schedule, menu, scores, jokes, calc, echo_gif_or_sticker # Импортируем модули с хэндлерами
from data.consts_and_vars import TOKEN #DB_PATH Импортируем константы и переменные '''all_surnames, get_second_scores, school_subjects, first_to_second,'''
from data.bot_states import ConvertingPoints # Импортируем класс с состояниями


bot = Bot(token=TOKEN) # Создаем объект бота
dp = Dispatcher() # Создаем объект диспетчера

# Подключаем роутеры хендлеров по убыванию значимости
dp.include_routers(common.router,
                   schedule.router,
                   scores.router,
                   menu.router,
                   jokes.router,
                   calc.router,
                   echo_gif_or_sticker.router,
)


async def main():
    await bot.delete_webhook(drop_pending_updates=True) # Пропускаем все накопленные входящие
    print('Бот запущен!')
    await dp.start_polling(bot) # Запускаем бота

if __name__ == "__main__":
    asyncio.run(main())
