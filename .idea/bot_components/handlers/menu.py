from aiogram import Router, types # Импортируем объект роутера и типы
from aiogram.filters import Text # Импортируем фильтр текста
from aiogram.utils.keyboard import ReplyKeyboardBuilder # Импортируем объект конструктора клавиатуры

router = Router() # Определяем роутер

@router.message(Text("Что в столовой?🍲"))
async def start(message: types.Message) -> None:
	# Создаем клавиатуру с тремя кнопками: Завтрак, Обед и Команды
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	keyboard.add("Завтрак", "Обед", "Главное меню")
	# Отправляем сообщение с выбором типа питания и клавиатурой
	await message.answer("Вас интересует завтрак или обед?", reply_markup=keyboard)


# Определяем асинхронную функцию для обработки сообщений с текстом "Завтрак" или "Обед"
@router.message(lambda message: message.text in ["Завтрак", "Обед"])
async def menu(message: types.Message) -> None:
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
    # Конкатенируем два блюда с разделителем ', или '
    # Используем английские слова для типов питания
    if message.text == "Завтрак":
        food_type = "breakfast"
    else:
        food_type = "lunch"
    query = f"SELECT {food_type}1 || ', или ' || {food_type}2 FROM menu WHERE weekday = '{weekday}'"
    # Создаем подключение к базе данных в том же потоке
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(query) # Выполняем запрос
        menu = cursor.fetchone()[0] # Получаем результат запроса в виде строки
    user_message = message.text # Получаем текст сообщения от пользователя
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