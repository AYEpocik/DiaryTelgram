import os
import random

from aiogram import Router, types  # Импортируем объект роутера и типы
from aiogram.filters import Text  # Импортируем фильтр текста
from aiogram.fsm.context import FSMContext  # Импортируем конечные автоматы
from data.bot_states import Default  # Импортируем класс с "обыкновенным" работы
from data.consts_and_vars import JOKES_PATH, abs_path


def get_joke_text(adult=False) -> str:
    file_names = []
    all_jokes_path = abs_path(JOKES_PATH)
    if adult:
        all_jokes_path += ' for adults'
    # Проходим по всем файлам и подпапкам в заданной папке с помощью функции os.walk()
    for root, dirs, files in os.walk(all_jokes_path):
        # Добавляем названия файлов в список file_names
        for file in files:
            if file.endswith(".txt"):
                file_names.append(file)
    rand_joke_path = f'{all_jokes_path}\\{file_names[random.randint(0, len(file_names) - 1)]}'
    with open(rand_joke_path, "r", encoding="utf-8") as file:
        return file.read()


# Читаем содержимое файла и сохраняем его и выводим пользователю


router = Router()


@router.message(Text(startswith='расскажи анекдот', ignore_case=True))
async def say_joke(message: types.Message, state: FSMContext) -> None:
    await message.answer(get_joke_text())
    await state.set_state(Default.main)


@router.message(Text(text='анек', ignore_case=True))
async def say_adult_joke(message: types.Message, state: FSMContext) -> None:
    await message.answer(get_joke_text(adult=True))
    await state.set_state(Default.main)
