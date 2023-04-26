from aiogram import Router, types # Импортируем объект роутера и типы
from aiogram.filters import CommandStart, Text # Импортируем считывание комманд

from keyboards.reply_kb import main_menu_keyboard # Импортируем обычные клавиатуры


router = Router() # Определяем роутер

# Определяем асинхронную функцию для обработки команды /start
@router.message(CommandStart())
async def start_message(message: types.Message):
    # Отправляем приветственное сообщение с клавиатурой
    await message.answer("Привет! Я бот, который может помочь тебе с разными вещами. Выбери одну из кнопок ниже.", reply_markup=main_menu_keyboard())
    # Получаем ID и имя пользователя из сообщения
    user_id = message.from_user.id
    username = message.from_user.username
    # Создаем подключение к базе данных в том же потоке
    with sqlite3.connect(DB_PATH) as conn:
        # Добавляем ID и имя пользователя в таблицу users с помощью параметризованного запроса
        conn.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (:user_id, :username)", {"user_id": user_id, "username": username})
        # Сохраняем изменения в базе данных
        conn.commit()

@router.message(Text("Главное меню"))
async def get_main_menu(message: types.Message):
	# Отправляем сообщение с клавиатурой с функциями бота
	await message.answer("Выберите одну из функций бота.", reply_markup=main_menu_keyboard())