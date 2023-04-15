# Импортируем необходимые библиотеки
import telebot # Библиотека для работы с телеграм API
import os # Библиотека для работы с переменными окружения

# Определяем путь к файлу с токеном
TOKEN_PATH = "../tokens/token_test2calc_bot.txt"

# Открываем файл в режиме чтения
with open(TOKEN_PATH, "r") as f:
    # Читаем токен из файла и удаляем лишние пробелы и символы переноса строки
    TOKEN = f.read().strip()

# Создаем объект бота
bot = telebot.TeleBot(TOKEN)

# Определяем обработчик команды /start
@bot.message_handler(commands=["start"])
def start(message):
    # Отправляем приветственное сообщение в чат с пользователем
    bot.send_message(message.chat.id, "Привет! Я бот-калькулятор. Я умею считать простые выражения. Просто напиши мне что-нибудь вроде 2+2 или 3*5 и я посчитаю для тебя.")

# Определяем обработчик всех текстовых сообщений
@bot.message_handler(content_types=["text"])
def calculate(message):
    # Пытаемся вычислить выражение, используя функцию eval()
    try:
        result = eval(message.text)
        # Отправляем результат в чат с пользователем
        bot.send_message(message.chat.id, result)
    # Если произошла ошибка, например, неверный синтаксис или деление на ноль
    except Exception as e:
        # Отправляем сообщение об ошибке в чат с пользователем
        bot.send_message(message.chat.id, f"Ошибка: {e}")

# Запускаем бота
bot.polling()