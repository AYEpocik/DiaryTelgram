from aiogram import Router, types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

from data.bot_states import ScheduleStates
from data.consts_and_vars import get_values_of_row, weekdays
from keyboards.inline_kb import get_surnames_kb, get_weekday_kb


router = Router()

@router.message(Text('Расписание📅'))
async def ask_for_surname(message: types.Message, state: FSMContext) -> None:
    global surname, weekday
    surname = ''
    weekday = ''
    await message.answer('Выберите фамилию ученика', reply_markup=get_surnames_kb())
    await state.set_state(ScheduleStates.waiting_for_surname)

@router.callback_query(ScheduleStates.waiting_for_surname)
async def ask_for_weekday(callback: types.callback_query, state: FSMContext) -> None:
    global surname
    surname = callback.data
    await callback.message.answer('Выберите день недели', reply_markup=get_weekday_kb())
    await callback.answer()
    await state.set_state(ScheduleStates.waiting_for_weekday)

@router.callback_query(ScheduleStates.waiting_for_weekday)
async def schedule(callback: types.callback_query, state: FSMContext) -> None:
    try:
        global weekday
        weekday = callback.data
        text = f'<u>{weekdays[weekday].capitalize()}</u>:\n\n'
        if weekday == 'saturday':
            text += '<i>Выходной день</i>'
        elif surname == 'тагирова':
            text += '<i>Домашнее обучение</i>'
        else:
            lessons_of_weekday = get_values_of_row(table=weekday, field='surname', row_value=surname)
            i = 1
            for lesson in lessons_of_weekday:
                text += f'{i}. {lesson}\n'
                i += 1
        await callback.message.answer(text, parse_mode='HTML')
        await callback.answer()
    except KeyError:
        await state.set_state(ScheduleStates.waiting_for_surname)
        await ask_for_weekday(callback, state)
        await callback.answer()