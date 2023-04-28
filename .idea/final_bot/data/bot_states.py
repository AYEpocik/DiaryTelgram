from aiogram.fsm.state import StatesGroup, State # Импортируем объект состояния для бота FSM


class ConvertingPoints(StatesGroup):
    chose_a_subject = State()
    waiting_points = State()

class Default(StatesGroup):
    main = State()

class FoodMenu(StatesGroup):
    ask_for_meal_times = State()

class ScheduleStates(StatesGroup):
    waiting_for_surname = State()
    waiting_for_weekday = State()