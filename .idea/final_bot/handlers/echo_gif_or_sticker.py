from aiogram import Router, types, F # Импортируем объект роутера, типы и MagicFilter

from data.bot_states import Default


router = Router()

@router.message(Default.main, F.sticker)
async def echo_sticker(message: types.Message) -> None:
    await message.answer_sticker(message.sticker.file_id)

@router.message(Default.main, F.animation)
async def echo_animation(message: types.Message) -> None:
    await message.answer_animation(message.animation.file_id)