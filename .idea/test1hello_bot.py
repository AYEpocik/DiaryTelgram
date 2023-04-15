# Импортируем необходимые библиотеки
import telebot # Библиотека для работы с телеграм API
import os # Библиотека для работы с переменными окружения


# Определяем путь к файлу с токеном
TOKEN_PATH = "../tokens/token_test1hello_bot.txt"

# Открываем файл в режиме чтения
with open(TOKEN_PATH, "r") as f:
    # Читаем токен из файла и удаляем лишние пробелы и символы переноса строки
    TOKEN = f.read().strip()

# Создаем объект бота
bot = telebot.TeleBot(TOKEN)

# Определяем обработчик всех текстовых сообщений
@bot.message_handler(content_types=["text"])
def reply_hello(message):
    # Отправляем ответ "привет" в чат с пользователем
    bot.send_message(message.chat.id, "Привет")

# Запускаем бота
bot.polling()