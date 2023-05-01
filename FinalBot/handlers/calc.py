from aiogram import Router, types, F  # Импортируем диспетчер, типы и магический фильтр
import string  # Библиотека для работы со строками

from data.bot_states import Default

router = Router()  # Определяем роутер


@router.message(
    Default.main,
    F.text
)
async def calculate(message: types.Message):
    # Пытаемся вычислить выражение, используя функцию eval()
    try:
        decide = True
        for i in message.text:
            if i not in string.digits + string.punctuation:
                decide = False
        if decide:
            result = eval(message.text)
            # Отправляем результат в чат с пользователем
            await message.answer(result)
    # Если произошла ошибка, например, неверный синтаксис или деление на ноль
    except:
        pass
