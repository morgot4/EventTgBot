from aiogram.fsm.state import StatesGroup, State

class Form(StatesGroup):
    name = State()
    date =  State()
    info = State()
    link = State()
    photo = State()