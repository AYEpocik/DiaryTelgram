import sqlite3 # Библиотека для работы с базами данных SQLite
import datetime # Библиотека для работы с датами

from aiogram import Router, types, F # Импортируем объект роутера, типы и магический фильтр
from aiogram.filters import Text # Импортируем фильтр текста
from aiogram.utils.keyboard import ReplyKeyboardBuilder # Импортируем объект конструктора клавиатуры

from keyboards.reply_kb import main_menu_keyboard, breakfast_or_lunch # Импортируем обычные клавиатуры
from data.consts_and_vars import DB_PATH # Импортируем токен бота и путь к базе данных


router = Router() # Определяем роутер

@router.message(Text("Что в столовой?🍲"))
async def start(message: types.Message) -> None:
	# Отправляем сообщение с выбором типа питания и клавиатурой
	await message.answer("Вас интересует завтрак или обед?", reply_markup=breakfast_or_lunch())


# Определяем асинхронную функцию для обработки сообщений с текстом "Завтрак" или "Обед"
@router.message(F.text.lower().in_({"завтрак", "обед"}))
async def menu(message: types.Message) -> None:
    user_message = message.text.lower()  # Получаем текст сообщения от пользователя
    # Получаем текущую дату
    date = datetime.date.today()
    # Получаем день недели в виде строки (например, Monday)
    real_weekday = date.strftime("%A").lower()
    # Если день недели - воскресенье, то добавляем один день к дате и получаем понедельник
    if real_weekday == "sunday":
        date += datetime.timedelta(days=1)
        weekday = date.strftime("%a")
    else: weekday = real_weekday
    # Формируем запрос к базе данных для получения меню по дню недели и типу питания
    # Конкатенируем два блюда с разделителем ', или '
    # Используем английские слова для типов питания
    if user_message == "завтрак":
        food_type = "breakfast"
    else:
        food_type = "lunch"
    query = f"SELECT {food_type}1 || ', или ' || {food_type}2 FROM menu WHERE weekday = '{weekday}'"
    # Создаем подключение к базе данных в том же потоке
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(query) # Выполняем запрос
        menu = cursor.fetchone()[0] # Получаем результат запроса в виде строки

    # Формируем текст сообщения бота с днем недели и меню
    # Если день недели - воскресенье, то пишем "Завтра на...", иначе пишем "Сегодня на..."
    if real_weekday == "sunday":
        bot_message = f"Завтра на {user_message} {menu}"
    elif (real_weekday == "saturday") and (message.text == "Обед"):
        bot_message = "Сегодня обедов нет"
    else:
        bot_message = f"Сегодня на {user_message} {menu}"
    # Отправляем сообщение пользователю
    await message.answer(bot_message)