from aiogram import Router, types, F # Импортируем объект роутера, типы и MagicFilter


router = Router()

@router.message(F.sticker)
async def echo_sticker(message: types.Message) -> None:
    await message.answer_sticker(message.sticker.file_id)

@router.message(F.animation)
async def echo_animation(message: types.Message) -> None:
    await message.answer_animation(message.animation.file_id)