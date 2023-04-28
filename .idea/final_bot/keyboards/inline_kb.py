from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from data.consts_and_vars import all_surnames, school_subjects, weekdays # Импортируем константы и переменные


def get_subject_kb() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for school_subject in school_subjects:
        builder.add(types.InlineKeyboardButton(
        text=school_subject,
        callback_data=school_subjects[school_subject])
        )
    builder.adjust(3)
    return builder.as_markup()

def get_surnames_kb() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for surname in all_surnames():
        builder.add(types.InlineKeyboardButton(
            text=surname.capitalize(),
            callback_data=surname
        ))
    builder.adjust(2)
    return builder.as_markup()

def get_weekday_kb() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for weekday in weekdays:
        builder.add(types.InlineKeyboardButton(
            text=weekdays[weekday].capitalize(),
            callback_data=weekday
        ))
    builder.adjust(2)
    return builder.as_markup()

def breakfast_or_lunch() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder() # Создаем конструктор клавиатуры
    builder.row(
        types.InlineKeyboardButton(text='Завтрак', callback_data='завтрак'),
        types.InlineKeyboardButton(text='Обед', callback_data='обед')
    )
    return builder.as_markup()
