from aiogram.fsm.state import State, StatesGroup

class GenState(StatesGroup):
    waiting_prompt = State()
