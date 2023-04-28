from aiogram import Router, types, F # Импортируем объект роутера, типы и MagicFilter
from aiogram.filters import Text # Импортируем фильтр текста
from aiogram.fsm.context import FSMContext # Импортируем конечные автоматы

from keyboards.reply_kb import main_menu_keyboard, main_menu_buttons # Импортируем обычные клавиатуры
from keyboards.inline_kb import get_subject_kb # Импортируем Inline клавиатуру для выбора предмета
from data.bot_states import ConvertingPoints # Импортируем класс с состояниями
from data.consts_and_vars import TOKEN, DB_PATH, all_surnames, school_subjects, school_subjects_in_dp, get_second_scores, first_to_second # Импортируем константы и переменные


router = Router()


@router.message(Text('Перевод баллов ЕГЭ💯'))
async def get_subject(message: types.Message, state: FSMContext) -> None:
    global max_points, subject
    max_points = 0
    subject = ''
    await message.answer('Выберите предмет: ', reply_markup=get_subject_kb())
    await state.set_state(ConvertingPoints.chose_a_subject)

@router.callback_query(ConvertingPoints.chose_a_subject)
async def get_primary_points(callback: types.callback_query, state: FSMContext) -> None:
    global max_points, subject
    max_points = len(get_second_scores(callback.data))
    subject = callback.data
    await callback.message.answer(f'Введите количество первичных баллов {school_subjects_in_dp[subject]} от 0 до {max_points}.')
    await callback.answer()
    await state.set_state(ConvertingPoints.waiting_points)

@router.message(
    ConvertingPoints.waiting_points,
    F.text,
    ~(F.text.in_(main_menu_buttons))
)
async def send_sec_points(message: types.Message, state: FSMContext) -> None:
    try:
        points = int(message.text)
        if points == 0:
            await message.answer('0 → 0')
        elif points in range(max_points):
            await message.answer(f'{points} → {first_to_second(subject, points)}')
        elif points == max_points:
            await message.answer(f'{points} → 100')
        else:
            await message.answer('Введите допустимое значение.')
    except ValueError:
        await message.answer('Можно цифирками?')
