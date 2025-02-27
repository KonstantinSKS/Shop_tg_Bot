from aiogram.fsm.state import StatesGroup, State


class StateUser(StatesGroup):
    enter_token = State()
    get_imei = State()
