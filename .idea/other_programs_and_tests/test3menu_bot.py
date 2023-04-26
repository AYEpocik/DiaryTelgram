# Импортируем необходимые библиотеки
import telebot # Библиотека для работы с телеграм API
import sqlite3 # Библиотека для работы с SQLite
import datetime # Библиотека для работы с датами

# Определяем путь к файлу с токеном
TOKEN_PATH = "../../tokens/token_test3menu_bot.txt"

# Определяем путь к файлу базы данных
DB_PATH = "../../Database/school.db"

# Открываем файл в режиме чтения
with open(TOKEN_PATH, "r") as f:
    # Читаем токен из файла и удаляем лишние пробелы и символы переноса строки
    TOKEN = f.read().strip()

# Создаем объект бота
bot = telebot.TeleBot(TOKEN)

# Обрабатываем команду /start
@bot.message_handler(commands=["start"])
def start(message):
    # Отправляем приветственное сообщение
    bot.send_message(message.chat.id, "Привет! Я бот-меню вашей школы. Я могу сказать вам, что сегодня в меню на завтрак или обед. Выберите тип питания:")
    # Создаем клавиатуру с двумя кнопками: Завтрак и Обед
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Завтрак", "Обед")
    # Отправляем клавиатуру пользователю
    bot.send_message(message.chat.id, "Выберите тип питания:", reply_markup=keyboard)

# Обрабатываем сообщения Завтрак или Обед
@bot.message_handler(func=lambda message: message.text in ["Завтрак", "Обед"])
def menu(message):
    # Получаем текущую дату
    date = datetime.date.today()
    # Получаем день недели в виде строки (например, Monday)
    weekday = date.strftime("%A")
    # Если день недели - воскресенье, то добавляем один день к дате и получаем понедельник
    if weekday == "Sunday":
        date += datetime.timedelta(days=1)
        weekday = date.strftime("%A")
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
    if weekday == "Sunday":
        bot_message = "Завтра на {} в вашей школе: {}".format(user_message.lower(), menu)
    else:
        bot_message = "Сегодня на {} в вашей школе: {}".format(user_message.lower(), menu)
    # Отправляем сообщение пользователю
    bot.send_message(message.chat.id, bot_message)

# Запускаем бота
bot.polling()