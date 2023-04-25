from aiogram import Dispatcher, types # Импортируем диспетчер и типы

async def calculate(message: types.Message):
    # Пытаемся вычислить выражение, используя функцию eval()
    try:
        decide = True
        for i in message.text:
            if i not in string.digits + string.punctuation:
                decide = False
        if decide == True:
            result = eval(message.text)
            # Отправляем результат в чат с пользователем
            await message.answer(result)
    # Если произошла ошибка, например, неверный синтаксис или деление на ноль
    except:
        pass

def register_handlers_calc(dp: Dispatcher):
    dp.register_message_handler(calculate, content_types=['text'])
