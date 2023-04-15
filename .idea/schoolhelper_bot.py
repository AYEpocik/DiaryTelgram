# Импортируем необходимые библиотеки
import asyncio # Библиотека для асинхронного программирования
import sqlite3 # Библиотека для работы с базами данных SQLite
from aiogram import Bot, Dispatcher, executor, types # Библиотека для работы с телеграм API
from apscheduler.schedulers.asyncio import AsyncIOScheduler # Библиотека для планирования задач

# Определяем путь к файлу с токеном
TOKEN_PATH = "../tokens/token_schoolhelper_bot.txt"
# Определяем путь к файлу с базой данных
DB_PATH = "../Database/school.db"

# Открываем файл в режиме чтения
with open(TOKEN_PATH, "r") as f:
    # Читаем токен из файла и удаляем лишние пробелы и символы переноса строки
    TOKEN = f.read().strip()

# Создаем объект бота
bot = Bot(token=TOKEN)
# Создаем объект диспетчера
dp = Dispatcher(bot)
# Создаем объект планировщика
scheduler = AsyncIOScheduler()

# Создаем клавиатуру с кнопками
keyboard = types.ReplyKeyboardMarkup(row_width=2) # Указываем количество кнопок в ряду
# Добавляем кнопки с текстом
keyboard.add("Калькулятор", "Меню", "Перевод баллов ЕГЭ", "Анекдоты", "Расписание")

# Определяем асинхронную функцию для обработки команды /start
@dp.message_handler(commands=["start"])
async def start_message(message: types.Message):
    # Отправляем приветственное сообщение с клавиатурой
    await message.answer("Привет! Я бот, который может помочь тебе с разными вещами. Выбери одну из кнопок ниже.", reply_markup=keyboard)
    # Получаем ID и имя пользователя из сообщения
    user_id = message.from_user.id
    username = message.from_user.username
    # Создаем подключение к базе данных в том же потоке
    conn = sqlite3.connect(DB_PATH)
    # Создаем курсор для работы с базой данных в том же потоке
    cur = conn.cursor()
    # Добавляем ID и имя пользователя в таблицу users
    cur.execute("INSERT INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
    # Сохраняем изменения в базе данных
    conn.commit()
    # Закрываем подключение и курсор
    cur.close()
    conn.close()

# Определяем асинхронную функцию для отправки сообщения всем пользователям
async def send_message_to_all():
    # Создаем подключение к базе данных в том же потоке
    conn = sqlite3.connect(DB_PATH)
    # Создаем курсор для работы с базой данных в том же потоке
    cur = conn.cursor()
    # Выполняем SQL-запрос для получения всех ID пользователей из таблицы users
    cur.execute("SELECT user_id FROM users")
    # Получаем список всех ID пользователей
    user_ids = cur.fetchall()
    # Закрываем подключение и курсор
    cur.close()
    conn.close()
    # Перебираем все ID пользователей
    for user_id in user_ids:
        # Отправляем сообщение пользователю с помощью метода bot.send_message
        await bot.send_message(user_id[0], "Привет! Сделал ли ты уроки на завтра на завтра?")
# Добавляем функцию send_message_to_all в расписание с помощью метода scheduler.add_job()
scheduler.add_job(send_message_to_all, "cron", hour=18, minute=11)

# Запускаем планировщик
scheduler.start()

# Запускаем бота с помощью метода executor.start_polling()
executor.start_polling(dp, skip_updates=True)