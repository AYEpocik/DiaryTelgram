import sqlite3 # Библиотека для работы с базами данных SQLite
from aiogram import Bot, Dispatcher, executor, types # Библиотека для работы с телеграм API
from apscheduler.schedulers.asyncio import AsyncIOScheduler # Библиотека для планирования задач
import datetime # Библиотека для работы с датами
import string # Библиотека для работы со строками
import calc # Импортируем handler пассивного калькулятора
from config_reader import config # Импортируем конфиг с токеном бота


# Определяем токен бота
TOKEN = config.bot_token.get_secret_value()

# Определяем путь к файлу с базой данных
DB_PATH = "../Database/school.db"

# Создаем объект бота
bot = Bot(token=TOKEN)
# Создаем объект диспетчера
dp = Dispatcher(bot)
# Создаем объект планировщика
scheduler = AsyncIOScheduler()

# Создаем клавиатуру с кнопками
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2) # Указываем количество кнопок в ряду
# Добавляем кнопки с текстом
keyboard.add("Что в столовой?🍲", "Перевод баллов ЕГЭ💯", "Расскажи анекдот😂", "Расписание📅")

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
    cur.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
    # Сохраняем изменения в базе данных
    conn.commit()
    # Закрываем подключение и курсор
    cur.close()
    conn.close()

@dp.message_handler(lambda message: message.text == "Что в столовой?🍲")
async def start(message: types.Message):
	# Создаем клавиатуру с тремя кнопками: Завтрак, Обед и Команды
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	keyboard.add("Завтрак", "Обед", "Главное меню")
	# Отправляем сообщение с выбором типа питания и клавиатурой
	await message.answer("Вас интересует завтрак или обед?", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Главное меню")
async def commands(message: types.Message):
	# Отправляем сообщение с клавиатурой с функциями бота
	await message.answer("Выберите одну из функций бота.", reply_markup=keyboard)

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
    query = f"SELECT {food_type}1 || ', или ' || {food_type}2 FROM menu WHERE weekday = '{weekday}'"
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
        bot_message = f"Завтра на {user_message.lower()} в столовой {menu}"
    elif (real_weekday == "Saturday") and (message.text == "Обед"):
        bot_message = "Сегодня обедов нет"
    else:
        bot_message = f"Сегодня на {user_message.lower()} в столовой {menu}"
    # Отправляем сообщение пользователю
    await message.answer(bot_message)



#@dp.message_handler(lambda message: message.text == "Расписание📅")

async def create_week_schedule(surname, DB_PATH=DB_PATH):
    # Создаем подключение к базе данных
    conn = sqlite3.connect(DB_PATH)
    # Задаем путь для сохранения изображения расписания
    output_path = f'../Schedules/{surname}.jpg'
    # Создаем пустой датафрейм для хранения расписания
    schedule = pd.DataFrame()
    # Список дней недели
    days = {"monday": "Понедельник",
            "tuesday": "Вторник",
            "wednesday": "Среда",
            "thursday": "Четверг",
            "friday": "Пятница"}
    # Цикл по дням недели
    for day in days:
        # Запрос к базе данных для выбора уроков ученика по фамилии
        query = f"SELECT * FROM {day} WHERE surname = '{surname}'"
        # Выполняем запрос и получаем результат в виде датафрейма
        df = pd.read_sql_query(query, conn)
        # Удаляем столбцы с индексом и фамилией
        df.drop(["index", "surname"], axis=1, inplace=True)
        # Транспонируем датафрейм, чтобы строки соответствовали номерам уроков
        df = df.T
        # Переименовываем столбец с уроками в название дня недели
        df.rename(columns={0: days[day]}, inplace=True)
        # Добавляем датафрейм к общему расписанию без параметра fill_value
        schedule = pd.concat([schedule, df], axis=1)
    # Сохраняем расписание в jpg-файл
    plt.figure(figsize=(13, 2), dpi=1000)
    plt.table(cellText=schedule.values, colLabels=schedule.columns, cellLoc="left", loc='upper left')
    plt.axis("off")
    plt.savefig(output_path, dpi=1000)
    # Закрываем соединение с базой данных
    conn.close()
    return output_path

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

def main():
    # Добавляем функцию send_message_to_all в расписание с помощью метода scheduler.add_job()
    scheduler.add_job(send_message_to_all, "cron", hour=18, minute=50)

    # Запускаем планировщик
    scheduler.start()

    # Запускаем бота с помощью метода executor.start_polling()
    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    main()
