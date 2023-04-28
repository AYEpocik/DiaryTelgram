from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from data.consts_and_vars import all_surnames, get_second_scores, school_subjects, first_to_second, TOKEN, DB_PATH # Импортируем константы и переменные


def get_subject_kb() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for school_subject in school_subjects:
        builder.add(types.InlineKeyboardButton(
        text=school_subject,
        callback_data=school_subjects[school_subject])
        )
    builder.adjust(3)
    return builder.as_markup()