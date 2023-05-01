import sqlite3 # Библиотека для работы с базами данных SQLite

from aiogram import Router, types # Импортируем объект роутера и типы
from aiogram.filters import CommandStart, Text # Импортируем считывание комманд
from aiogram.fsm.state import StatesGroup, State # Импортируем объект состояния для бота FSM
from aiogram.fsm.context import FSMContext # Импортируем конечные автоматы

from keyboards.reply_kb import main_menu_keyboard # Импортируем обычные клавиатуры
from data.consts_and_vars import all_surnames, get_second_scores, school_subjects, first_to_second, TOKEN, DB_PATH # Импортируем константы и переменные
from data.bot_states import Default


router = Router() # Определяем роутер

# Определяем асинхронную функцию для обработки команды /start
@router.message(CommandStart())
async def start_message(message: types.Message, state: FSMContext):
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
    #await
    await state.set_state(Default.main)

@router.message(Text("Главное меню🏠"))
async def get_main_menu(message: types.Message, state: FSMContext):
    # Отправляем сообщение с клавиатурой с функциями бота
    await message.answer("Выберите одну из функций бота.", reply_markup=main_menu_keyboard())
    await state.set_state(Default.main)
