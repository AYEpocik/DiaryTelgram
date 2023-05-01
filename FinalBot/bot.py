import asyncio  # Библиотека "асинхронности"

from aiogram import Bot, Dispatcher  # Импортируем объекты бота, диспетчера

from data.consts_and_vars import TOKEN, ADMIN_ID  # Импортируем константы и переменные
from handlers import common, schedule, menu, scores, jokes, calc, echo_gif_or_sticker  # Импортируем модули с хэндлерами

bot = Bot(token=TOKEN)  # Создаем объект бота
dp = Dispatcher()  # Создаем объект диспетчера

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
    await bot.delete_webhook(drop_pending_updates=True)  # Пропускаем все накопленные входящие
    await bot.send_message(ADMIN_ID, 'Бот запущен!')
    print('Бот запущен!')
    await dp.start_polling(bot)  # Запускаем бота


if __name__ == "__main__":
    asyncio.run(main())
