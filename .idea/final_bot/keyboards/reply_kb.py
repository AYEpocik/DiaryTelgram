from aiogram import types # Импортируем типы
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder # Импортируем объекты создания обычных и inline клавиатур


main_menu_buttons = {
    "Что в столовой?🍲",
    "Перевод баллов ЕГЭ💯",
    "Расскажи анекдот😂",
    "Расписание📅",
}

def main_menu_keyboard():
    kb = [
        [
        types.KeyboardButton(text="Что в столовой?🍲"),
        types.KeyboardButton(text="Перевод баллов ЕГЭ💯"),
        ],
        [
        types.KeyboardButton(text="Расскажи анекдот😂"),
        types.KeyboardButton(text="Расписание📅"),
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Чего пожелаете?)",
    )
    return keyboard