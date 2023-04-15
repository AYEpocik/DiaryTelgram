# Импортируем необходимые библиотеки
import asyncio # Библиотека для асинхронного программирования
import sqlite3 # Библиотека для работы с базами данных SQLite
from aiogram import Bot, Dispatcher, executor, types # Библиотека для работы с телеграм API
from apscheduler.schedulers.asyncio import AsyncIOScheduler # Библиотека для планирования задач
import datetime # Библиотека для работы с датами


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

@dp.message_handler(lambda message: message.text == "Меню")
async def start(message: types.Message):
    # Отправляем сообщение с выбором типа питания
    await message.answer("Выберите тип питания:")
    # Создаем клавиатуру с двумя кнопками: Завтрак и Обед
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Завтрак", "Обед")
    # Отправляем клавиатуру пользователю
    await message.answer("Выберите тип питания:", reply_markup=keyboard)

# Определяем асинхронную функцию для обработки сообщений с текстом "Завтрак" или "Обед"
@dp.message_handler(lambda message: message.text in ["Завтрак", "Обед"])
async def menu(message: types.Message):
    # Получаем текущую дату
    date = datetime.date.today()
    # Получаем день недели в виде строки (например, Monday)
    real_weekday = date.strftime("%A")
    # Если день недели - воскресенье, то добавляем один день к дате и получаем понедельник
    if real_weekday == "Sunday":
        date += datetime.timedelta(days=1)
        weekday = date.strftime("%A")
    else: weekday = real_weekday
    # Формируем запрос к базе данных для получения меню по дню недели и типу питания
    # Конкатенируем два блюда с разделителем /
    # Используем английские слова для типов питания
    if message.text == "Завтрак":
        food_type = "breakfast"
    else:
        food_type = "lunch"
    query = f"SELECT {food_type}1 || '/' || {food_type}2 FROM menu WHERE weekday = '{weekday}'"
    # Подключаемся к базе данных SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Выполняем запрос
    cursor.execute(query)
    # Получаем результат запроса в виде строки (например, "гречка/макароны")
    menu = cursor.fetchone()[0]
    # Закрываем соединение с базой данных
    conn.close()
    # Получаем текст сообщения от пользователя
    user_message = message.text
    # Формируем текст сообщения бота с днем недели и меню
    # Если день недели - воскресенье, то пишем "Завтра на...", иначе пишем "Сегодня на..."
    if real_weekday == "Sunday":
        bot_message = "Завтра на {} в вашей школе: {}".format(user_message.lower(), menu)
    else:
        bot_message = "Сегодня на {} в вашей школе: {}".format(user_message.lower(), menu)
    # Отправляем сообщение пользователю
    await message.answer(bot_message)

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
        await bot.send_message(user_id[0], "Привет! Сделал ли ты уроки на завтра?")
# Добавляем функцию send_message_to_all в расписание с помощью метода scheduler.add_job()
scheduler.add_job(send_message_to_all, "cron", hour=18, minute=50)

# Запускаем планировщик
scheduler.start()

# Запускаем бота с помощью метода executor.start_polling()
executor.start_polling(dp, skip_updates=True)

