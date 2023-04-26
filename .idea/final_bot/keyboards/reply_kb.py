from aiogram import types # Импортируем типы
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder # Импортируем объекты создания обычных и inline клавиатур


def main_menu_keyboard() -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder() # Создаем конструктор клавиатуры
    builder.row(
        types.KeyboardButton(text="Что в столовой?🍲"),
        types.KeyboardButton(text="Перевод баллов ЕГЭ💯"),
        types.KeyboardButton(text="Расскажи анекдот😂"),
        types.KeyboardButton(text="Расписание📅")
    )
    builder.adjust(2) # Указываем количество кнопок в ряду
    return builder.as_markup(resize_keyboard=True)

def breakfast_or_lunch() -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder() # Создаем конструктор клавиатуры
    builder.row(
        types.KeyboardButton(text="Завтрак"),
        types.KeyboardButton(text="Обед"),
        types.KeyboardButton(text="Главное меню")
    )
    builder.adjust(2) # Указываем количество кнопок в ряду
    return builder.as_markup(resize_keyboard=True)