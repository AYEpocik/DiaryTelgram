# Импортируем необходимые библиотеки
import telebot # Библиотека для работы с телеграм API
import sqlite3 # Библиотека для работы с базами данных SQLite
import schedule # Библиотека для планирования задач
import time # Библиотека для работы со временем

# Определяем токен бота
TOKEN = "токен"

# Создаем объект бота
bot = telebot.TeleBot(TOKEN)

# Определяем путь к файлу с базой данных
DB_PATH = "users.db"

# Создаем подключение к базе данных
conn = sqlite3.connect(DB_PATH)
# Создаем курсор для работы с базой данных
cur = conn.cursor()
# Создаем таблицу users, если она еще не существует
cur.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)")
# Сохраняем изменения в базе данных
conn.commit()

# Определяем хэндлер для команды /start
@bot.message_handler(commands=["start"])
def start_message(message):
    # Отправляем приветственное сообщение
    bot.send_message(message.chat.id, "Привет! Я бот, который будет напоминать тебе о домашнем задании.")
    # Получаем ID пользователя из сообщения
    user_id = message.from_user.id
    # Добавляем ID пользователя в таблицу users, если он еще не там
    cur.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    # Сохраняем изменения в базе данных
    conn.commit()

# Определяем функцию для отправки сообщения всем пользователям
def send_message_to_all():
    # Выполняем SQL-запрос для получения всех ID пользователей из таблицы users
    cur.execute("SELECT user_id FROM users")
    # Получаем список всех ID пользователей
    user_ids = cur.fetchall()
    # Перебираем все ID пользователей
    for user_id in user_ids:
        # Отправляем сообщение пользователю с помощью метода bot.send_message
        bot.send_message(user_id[0], "Привет! Сделал ли ты уроки на завтра?")

# Добавляем функцию send_message_to_all в расписание с помощью метода schedule.every().day.at()
schedule.every().day.at("18:00").do(send_message_to_all)

# Запускаем бота
bot.polling()

# Запускаем бесконечный цикл для выполнения расписания
while True:
    # Выполняем запланированные задачи с помощью метода schedule.run_pending()
    schedule.run_pending()
    # Ждем одну секунду с помощью метода time.sleep()
    time.sleep(1)